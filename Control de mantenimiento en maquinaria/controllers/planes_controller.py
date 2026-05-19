from database.planes_dao import PlanesDAO
from database.maquinaria_dao import MaquinariaDAO # Reutilizamos para el combo

class PlanesController:
    def __init__(self, vista_planes):
        self.vista = vista_planes
        self.dao = PlanesDAO()
        self.dao_maquina = MaquinariaDAO()

    def cargar_lista_maquinaria(self):
        """Devuelve las máquinas para llenar el ComboBox del diálogo"""
        return self.dao_maquina.obtener_todos()

    def crear_nuevo_plan(self, datos):
        """Coordina la creación del plan y refresca la vista"""
        exito = self.dao.guardar_plan_completo(
            datos['nombre'],
            datos['intervalo'],
            datos['id_maquina'], 
            datos['tareas']
        )
        if exito:
            self.refrescar_contenido()
        return exito

    def refrescar_contenido(self):
        """Limpia la vista y vuelve a cargar todos los planes desde la BD"""
        self.vista.limpiar_grid()
        planes = self.dao.obtener_todos_los_planes()
        
        columnas_max = 3
        for i, plan in enumerate(planes):
            fila = i // columnas_max
            columna = i % columnas_max
            self.vista.agregar_tarjeta_plan(plan, (fila, columna))

    def eliminar_plan(self, id_plan):
        """Maneja la eliminación de un plan"""
        if self.dao.eliminar_plan(id_plan):
            self.refrescar_contenido()
            return True
        return False
    
    def actualizar_plan(self, d):
        """Pide al DAO que ejecute la transacción de actualización"""
        exito = self.dao.actualizar_plan(d['id_plan'], d['nombre'], d['tareas'])
        if exito:
            self.refrescar_contenido()
        return exito
    
    def filtrar_busqueda(self, texto):
        texto = texto.lower().strip()
        self.vista.limpiar_grid()
        
        # Obtenemos todos los planes del DAO
        todos_los_planes = self.dao.obtener_todos_los_planes()
        
        # Filtramos por los 3 criterios
        filtrados = [
            p for p in todos_los_planes 
            if texto in p['nombre'].lower() or 
            texto in p['modelo_maquina'].lower() or 
            texto in str(p['id_plan'])
        ]
        
        # Dibujamos solo los filtrados
        for i, plan in enumerate(filtrados):
            fila, columna = i // 3, i % 3
            self.vista.agregar_tarjeta_plan(plan, (fila, columna))

    def obtener_detalle_reporte_plan(self, id_plan):
        return self.dao.obtener_detalle_reporte_plan(id_plan)
