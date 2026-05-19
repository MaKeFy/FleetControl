from database.maquinaria_dao import MaquinariaDAO
from views.vista_flota import VistaFlota

class FlotaController:
    def __init__(self, vista):
        self.vista = vista
        self.dao = MaquinariaDAO()

    def refrescar_dashboard(self, filtro=""):
        """Recupera unidades, calcula estados y actualiza la vista."""
        unidades = self.dao.obtener_todos_con_plan()
        print(f"DEBUG: El DAO devolvió {len(unidades)} unidades.")
        if not unidades:
            self.vista.actualizar_grid([])
            return

        for unidad in unidades:
            if not isinstance(unidad, dict):
                continue
            id_actual = unidad.get('id') or unidad.get('id_maquina')
            color_real = self.calcular_estado_mantenimiento(id_actual)
            
            # Sincronización con BD si el color cambió
            if unidad.get('estado_color') != color_real:
                # El DAO usa el alias 'id' o 'id_maquina' según tu SQL
                id_maq = unidad.get('id') or unidad.get('id_maquina')
                self.dao.actualizar_estado_color(id_maq, color_real)
                unidad['estado_color'] = color_real
                
        if filtro:
            unidades = [u for u in unidades if filtro.lower() in str(u.values()).lower()]
            
        self.vista.actualizar_grid(unidades)

    def calcular_estado_mantenimiento(self, id_maquina):
        # 1. Normalización del ID
        if isinstance(id_maquina, dict):
            id_maquina = id_maquina.get('id') or id_maquina.get('id_maquina')
        
        # 2. PRIORIDAD ABSOLUTA: Verificar Fallas Correctivas (Color Negro)
        # Consultamos directamente al DAO por órdenes 'correctivo' abiertas
        if self.dao.tiene_orden_correctiva_abierta(id_maquina):
            return "Negro"

        # 3. Obtener planes vinculados
        planes = self.dao.obtener_estado_detallado_planes(id_maquina)
        if not planes:
            return "Blanco"

        peor_color = "Verde"

        for plan in planes:
            actuales = float(plan.get('horas_motor_total', 0))
            ultima_ejecucion = float(plan.get('ultima_ejecucion_horas', 0))
            intervalo = float(plan.get('intervalo_horas', 0))
            id_plan = plan.get('id_plan')
            
            if intervalo <= 0: continue

            uso_desde_el_plan = actuales - ultima_ejecucion
            
            # RF05: Lógica de Alerta y Generación
            if uso_desde_el_plan >= (intervalo * 0.9):
                # Verificación de seguridad: ¿Realmente no existe ya una orden?
                nombre_plan = plan.get('nombre_plan', 'Plan sin nombre')
                if not self.dao.existe_orden_abierta(id_maquina, id_plan, nombre_plan):
                    descripcion = f"SISTEMA: Mantenimiento preventivo alcanzado para el plan '{nombre_plan}'."
                    # Ejecutamos la inserción
                    self.dao.crear_orden_automatica(id_maquina, id_plan, descripcion)
                
                # Determinación de severidad del color
                if uso_desde_el_plan >= intervalo:
                    peor_color = "Rojo"
                elif peor_color != "Rojo":
                    peor_color = "Amarillo"
                    
        return peor_color

    def modificar_unidad(self, id_maquina, nuevos_datos):
        """RF02: Modifica datos técnicos y recalcula color."""
        if self.dao.actualizar_maquinaria(id_maquina, nuevos_datos):
            # AQUÍ YA NO FALLARÁ porque el método está definido abajo
            self.actualizar_color_por_plan(id_maquina)
            self.refrescar_dashboard()
            return True
        return False

    def actualizar_color_por_plan(self, id_maquina):
        """Recalcula y persiste el color para una sola unidad específica."""
        maquina = self.dao.obtener_maquina_con_plan(id_maquina)
        if maquina and isinstance(maquina, dict):
            nuevo_color = self.calcular_estado_mantenimiento(maquina)
            if maquina.get('estado_color') != nuevo_color:
                self.dao.actualizar_estado_color(id_maquina, nuevo_color)

    def borrar_unidad(self, id_maquina):
        """RF02: Elimina físicamente la maquinaria."""
        if self.dao.eliminar_maquinaria(id_maquina):
            self.refrescar_dashboard()
            return True
        return False

    def sumar_uso(self, id_maq, horas_adicionales):
        """Registra jornada de trabajo y actualiza estado visual."""
        exito = self.dao.acumular_horas(id_maq, horas_adicionales)
        if exito:
            self.actualizar_color_por_plan(id_maq)
        return exito

    def registrar_unidad_automatica(self, datos):
        """Guarda nueva maquinaria e inicializa su color."""
        id_maquina = self.dao.registrar_nueva(datos)
        if id_maquina:
            self.actualizar_color_por_plan(id_maquina)
            self.refrescar_dashboard()
            return True
        return False

    def filtrar_busqueda(self, texto):
        self.refrescar_dashboard(filtro=texto)
        
    def reportar_falla(self, id_maquina, descripcion):
        if not descripcion.strip():
            return False
        return self.dao.registrar_incidencia_correctiva(id_maquina, descripcion)
    
    
