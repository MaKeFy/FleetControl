from views.dialogo_nuevo_plan import DialogoNuevoPlan
from PySide6.QtWidgets import QMessageBox

class DialogoEditarPlan(DialogoNuevoPlan):
    def __init__(self, datos_plan, lista_maquinaria, parent=None):
        # Reutilizamos la estructura del diálogo de creación
        super().__init__(lista_maquinaria, parent)
        self.setWindowTitle(f"Editando: {datos_plan['nombre']}")
        self.id_plan = datos_plan['id_plan']
        self.btn_guardar.setText("Guardar Cambios")
        
        # 1. Precargar Nombre
        self.txt_nombre.setText(datos_plan['nombre'])
        
        # 2. Bloquear maquinaria (no se suele cambiar el dueño de un plan ya creado)
        index = self.combo_maquina.findData(datos_plan['id_maquina'])
        self.combo_maquina.setCurrentIndex(index)
        self.combo_maquina.setEnabled(False) 

        # 3. Limpiar la tarea por defecto y cargar las reales
        for fila in self.inputs_tareas: # Limpiamos lo que crea el padre
            fila.parent().deleteLater()
        self.inputs_tareas.clear()

        for tarea_desc in datos_plan['tareas']:
            self.agregar_fila_tarea_con_texto(tarea_desc)

    def agregar_fila_tarea_con_texto(self, texto):
        """Versión extendida para cargar texto existente"""
        self.agregar_fila_tarea()
        self.inputs_tareas[-1].setText(texto)

    def obtener_datos(self):
        """Retorna datos incluyendo el ID del plan"""
        datos = super().obtener_datos()
        datos['id_plan'] = self.id_plan
        return datos