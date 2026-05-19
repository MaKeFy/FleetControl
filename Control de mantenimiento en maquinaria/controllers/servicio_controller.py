# controllers/servicio_controller.py
import sys
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.maquinaria_dao import MaquinariaDAO

class ServicioController:
    def __init__(self, vista):
        self.vista = vista
        self.dao = MaquinariaDAO()

    def cargar_ordenes(self, estado=None):
        """
        Recupera las órdenes y actualiza la vista. 
        Si 'estado' es 'Todos los Estados' o None, trae todo.
        """
        # Normalizar el filtro
        filtro = None if not estado or "Todos" in estado else estado
        
        # Obtener datos del DAO
        ordenes = self.dao.obtener_ordenes_servicio(filtro)
        
        # Actualizar la interfaz
        self.vista.actualizar_grid(ordenes)

    def cerrar_orden_mantenimiento(self, id_orden, id_maquina, id_plan, horas_cierre, costo, notas):
        """Cierra la orden y resetea el horómetro del plan específico (RF05/RF06)."""
        # 1. Registrar el cumplimiento del plan (Metas Dinámicas)
        if id_plan: # Solo si es preventivo
            self.dao.registrar_cumplimiento_plan(id_maquina, id_plan, horas_cierre)
        
        # 2. Cerrar la orden de servicio
        if self.dao.cerrar_orden_servicio(id_orden, costo, notas):
            self.cargar_ordenes()
            return True
        return False
    
    def procesar_cierre_orden(self, id_orden, id_maquina, id_plan, datos_cierre):
        # 1. Actualizamos la meta del plan (Metas Dinámicas)
        # Esto hará que el semáforo vuelva a VERDE
        if id_plan:
            self.dao.registrar_cumplimiento_plan(
                id_maquina, 
                id_plan, 
                datos_cierre['horas_cierre']
            )
        
        # 2. Registramos repuestos y actualizamos el último mantenimiento general.
        if datos_cierre.get('repuestos'):
            if not self.dao.registrar_repuestos_orden(id_orden, datos_cierre['repuestos']):
                return False

        if not self.dao.actualizar_ultimo_servicio_maquina(
            id_maquina, 
            datos_cierre['horas_cierre']
        ):
            return False

        # 3. Cerramos la orden físicamente
        exito = self.dao.cerrar_orden_servicio(
            id_orden, 
            datos_cierre['costo_total'], 
            datos_cierre['notas']
        )
        
        if exito:
            self.cargar_ordenes() # Refrescar la vista de servicios
        return exito
            
    # controllers/servicio_controller.py
    def finalizar_orden(self, id_orden, id_maquina, id_plan, datos):
        # 1. Registrar repuestos en la BD
        if datos['repuestos']:
            self.dao.registrar_repuestos_orden(id_orden, datos['repuestos'])
        
        # 2. Cerrar la orden con el costo total calculado
        self.dao.cerrar_orden_servicio(id_orden, datos['costo_total'], datos['notas'])
        
        # 3. Actualizar horómetro del plan (para el semáforo)
        if id_plan:
            self.dao.registrar_cumplimiento_plan(id_maquina, id_plan, datos['horas_cierre'])
            
    def filtrar_ordenes(self, texto):
        """Filtra las órdenes mostradas basándose en el texto de búsqueda."""
        # Obtenemos todas las órdenes actuales del DAO o de una variable caché
        todas = self.dao.obtener_ordenes_servicio() 
        
        if not texto:
            self.vista.actualizar_grid(todas)
            return

        termino = texto.lower()
        filtradas = [
            o for o in todas if 
            termino in str(o.get('id_orden')).lower() or
            termino in o.get('marca', '').lower() or
            termino in o.get('modelo', '').lower() or
            termino in o.get('descripcion_falla', '').lower()
        ]
        
        self.vista.actualizar_grid(filtradas)
        
    # controllers/servicio_controller.py

    def crear_incidencia_manual(self, datos):
        """Procesa el reporte de falla manual (RF06)"""
        id_maq = datos.get('id_maquina')
        descripcion = datos.get('descripcion')

        # 1. Crear la orden de servicio tipo 'correctivo'
        # Nota: Pasamos None en id_plan porque es una falla inesperada, no un mantenimiento programado
        exito_orden = self.dao.crear_orden_manual(id_maq, 'correctivo', descripcion)
        
        # 2. Forzamos el color Negro en la maquinaria
        if exito_orden:
            self.dao.actualizar_estado_color(id_maq, "Negro")
            return True
        return False

    def eliminar_orden(self, id_orden, motivo, usuario):
        exito = self.dao.eliminar_orden_servicio(id_orden, motivo, usuario)
        if exito:
            self.cargar_ordenes()
        return exito
