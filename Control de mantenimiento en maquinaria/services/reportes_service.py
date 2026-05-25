from html import escape
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

from PySide6.QtGui import QPdfWriter, QTextDocument, QPageSize
from PySide6.QtCore import QMarginsF


class ReportesService:
    @staticmethod
    def generar_hoja_servicio_html(orden, repuestos, ruta_salida):
        repuestos_rows = "\n".join(
            f"<tr><td>{escape(str(r.get('nombre', '')))}</td><td class='money'>${float(r.get('costo') or 0):,.2f}</td></tr>"
            for r in repuestos
        )
        if not repuestos_rows:
            repuestos_rows = "<tr><td colspan='2'>Sin repuestos registrados</td></tr>"

        tareas = escape(str(orden.get("descripcion_falla") or "Sin descripcion"))
        costo = float(orden.get("costo_total") or 0)
        html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Hoja de Servicio {escape(str(orden.get('id_orden', '')))}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #111827; }}
    header {{ border-bottom: 3px solid #111827; padding-bottom: 14px; margin-bottom: 22px; }}
    h1 {{ margin: 0; font-size: 26px; }}
    h2 {{ margin-top: 26px; font-size: 17px; border-bottom: 1px solid #d1d5db; padding-bottom: 6px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px 24px; }}
    .box {{ border: 1px solid #d1d5db; padding: 10px; min-height: 24px; }}
    .label {{ color: #6b7280; font-size: 12px; text-transform: uppercase; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 9px; text-align: left; }}
    th {{ background: #f3f4f6; }}
    .money {{ text-align: right; }}
    .checklist td:first-child {{ width: 28px; text-align: center; }}
    .signatures {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; margin-top: 70px; }}
    .line {{ border-top: 1px solid #111827; text-align: center; padding-top: 8px; }}
    @media print {{ body {{ margin: 18mm; }} button {{ display: none; }} }}
  </style>
</head>
<body>
  <button onclick="window.print()">Imprimir</button>
  <header>
    <h1>Hoja de Servicio</h1>
    <div>Folio: {escape(str(orden.get('folio') or orden.get('id_orden') or 'S/F'))}</div>
  </header>

  <section class="grid">
    <div class="box"><div class="label">Maquinaria</div>{escape(str(orden.get('marca', '')))} {escape(str(orden.get('modelo', '')))}</div>
    <div class="box"><div class="label">VIN / Serie</div>{escape(str(orden.get('vin', 'S/N')))}</div>
    <div class="box"><div class="label">Tipo</div>{escape(str(orden.get('tipo', '')))}</div>
    <div class="box"><div class="label">Estado</div>{escape(str(orden.get('estado', '')))}</div>
    <div class="box"><div class="label">Fecha creacion</div>{escape(str(orden.get('fecha_creacion', '')))}</div>
    <div class="box"><div class="label">Fecha cierre</div>{escape(str(orden.get('fecha_cierre') or 'Pendiente'))}</div>
    <div class="box"><div class="label">Mecanico</div>{escape(str(orden.get('mecanico') or 'Pendiente'))}</div>
    <div class="box"><div class="label">Costo total</div>${costo:,.2f}</div>
  </section>

  <h2>Descripcion / trabajo solicitado</h2>
  <p>{tareas.replace(chr(10), '<br>')}</p>

  <h2>Checklist de servicio</h2>
  <table class="checklist">
    <tr><th></th><th>Actividad</th><th>Observaciones</th></tr>
    <tr><td>[ ]</td><td>Revision general de seguridad</td><td></td></tr>
    <tr><td>[ ]</td><td>Revision de fluidos y lubricacion</td><td></td></tr>
    <tr><td>[ ]</td><td>Inspeccion de filtros, bandas y mangueras</td><td></td></tr>
    <tr><td>[ ]</td><td>Prueba funcional posterior al servicio</td><td></td></tr>
  </table>

  <h2>Repuestos utilizados</h2>
  <table>
    <tr><th>Repuesto</th><th>Costo</th></tr>
    {repuestos_rows}
  </table>

  <section class="signatures">
    <div class="line">Responsable de mantenimiento</div>
    <div class="line">Mecanico</div>
  </section>
</body>
</html>"""
        Path(ruta_salida).write_text(html, encoding="utf-8")

    @staticmethod
    def exportar_ordenes_xlsx(ordenes, ruta_salida):
        headers = [
            "ID Orden", "Folio", "Maquinaria", "VIN", "Tipo", "Estado",
            "Fecha Creacion", "Fecha Cierre", "Descripcion", "Costo Refacciones",
            "Costo Mano de Obra", "Costo Total"
        ]
        rows = [headers]
        total_refacciones = 0
        total_mano_obra = 0
        total_general = 0
        for orden in ordenes:
            costo_total = float(orden.get("costo_total") or 0)
            costo_refacciones = float(orden.get("costo_repuestos") or 0)
            costo_mano_obra = max(costo_total - costo_refacciones, 0)
            total_refacciones += costo_refacciones
            total_mano_obra += costo_mano_obra
            total_general += costo_total
            rows.append([
                orden.get("id_orden", ""),
                orden.get("folio", ""),
                f"{orden.get('marca', '')} {orden.get('modelo', '')}".strip(),
                orden.get("vin", ""),
                orden.get("tipo", ""),
                orden.get("estado", ""),
                str(orden.get("fecha_creacion", "")),
                str(orden.get("fecha_cierre") or ""),
                orden.get("descripcion_falla", ""),
                costo_refacciones,
                costo_mano_obra,
                costo_total,
            ])
        rows.append([""] * len(headers))
        rows.append(["TOTALES", "", "", "", "", "", "", "", "", total_refacciones, total_mano_obra, total_general])

        sheet_xml = ReportesService._sheet_xml(rows)
        workbook_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Servicios" sheetId="1" r:id="rId1"/></sheets></workbook>"""
        rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>"""
        workbook_rels_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>"""
        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font></fonts><fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill><fill><patternFill patternType="solid"><fgColor rgb="FF0F766E"/><bgColor indexed="64"/></patternFill></fill></fills><borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders><cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs></styleSheet>"""
        content_types_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>"""

        with ZipFile(ruta_salida, "w", ZIP_DEFLATED) as xlsx:
            xlsx.writestr("[Content_Types].xml", content_types_xml)
            xlsx.writestr("_rels/.rels", rels_xml)
            xlsx.writestr("xl/workbook.xml", workbook_xml)
            xlsx.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml)
            xlsx.writestr("xl/styles.xml", styles_xml)
            xlsx.writestr("xl/worksheets/sheet1.xml", sheet_xml)

    @staticmethod
    def _sheet_xml(rows):
        col_widths = "".join(
            f'<col min="{i}" max="{i}" width="{w}" customWidth="1"/>'
            for i, w in enumerate([10, 14, 24, 22, 14, 14, 16, 16, 48, 18, 18, 14], start=1)
        )
        xml_rows = []
        for row_idx, row in enumerate(rows, start=1):
            cells = []
            for col_idx, value in enumerate(row, start=1):
                ref = f"{ReportesService._col_name(col_idx)}{row_idx}"
                style = ' s="1"' if row_idx == 1 else ""
                if isinstance(value, (int, float)):
                    cells.append(f'<c r="{ref}"{style}><v>{value}</v></c>')
                else:
                    cells.append(
                        f'<c r="{ref}" t="inlineStr"{style}><is><t>{escape(str(value))}</t></is></c>'
                    )
            xml_rows.append(f'<row r="{row_idx}">{"".join(cells)}</row>')

        return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews><cols>{col_widths}</cols><sheetData>{"".join(xml_rows)}</sheetData><autoFilter ref="A1:L{len(rows)}"/><pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>"""

    @staticmethod
    def generar_reporte_plan_pdf(detalle, ruta_salida):
        plan = detalle.get("plan") or {}
        maquinas = detalle.get("maquinas") or []
        tareas = detalle.get("tareas") or []
        incidencias = detalle.get("incidencias") or []
        folio = f"HS-{datetime.now().strftime('%Y%m%d%H%M%S')}-{plan.get('id_plan', '0')}"

        maquinas_html = "".join(
            f"<tr><td>{escape(str(m.get('id_maquina', '')))}</td><td>{escape(str(m.get('marca', '')))} {escape(str(m.get('modelo', '')))}</td><td>{escape(str(m.get('vin', '')))}</td><td>{escape(str(m.get('horas_motor_total', '')))} h</td></tr>"
            for m in maquinas
        ) or "<tr><td colspan='4'>Sin maquinaria asociada</td></tr>"

        tareas_html = "".join(
            f"<tr><td class='check'>[ ]</td><td>{escape(str(t))}</td><td></td><td class='money'>$</td></tr>"
            for t in tareas
        ) or "<tr><td colspan='4'>Sin tareas registradas</td></tr>"

        incidencias_html = "".join(
            f"<tr><td>{escape(str(i.get('id_orden', '')))}</td><td>{escape(str(i.get('maquinaria', '')))}</td><td>{escape(str(i.get('fecha_creacion', '')))}</td><td>{escape(str(i.get('descripcion_falla', '')))}</td></tr>"
            for i in incidencias
        ) or "<tr><td colspan='4'>Sin incidencias urgentes pendientes</td></tr>"

        ancho_tabla = 640
        ancho_panel = 288
        margen_panel = ancho_tabla - ancho_panel

        html = f"""
        <html>
        <head>
          <style>
            body {{ font-family: Arial, sans-serif; color: #111827; margin: 0; }}
            h1 {{ font-size: 25px; margin-bottom: 4px; text-align: left; }}
            h2 {{ font-size: 16px; margin-top: 22px; border-bottom: 1px solid #d1d5db; padding-bottom: 5px; text-align: left; }}
            .meta {{ color: #4b5563; margin-bottom: 14px; }}
            .folio {{ float: right; border: 1px solid #111827; padding: 8px 12px; font-weight: bold; }}
            .urgent {{ color: #b91c1c; font-weight: bold; }}
            table {{ border-collapse: collapse; margin-top: 8px; }}
            .full-table {{ width: {ancho_tabla}px; }}
            th, td {{ border: 1px solid #d1d5db; padding: 10px; font-size: 10.5pt; vertical-align: top; text-align: left; word-wrap: break-word; }}
            th {{ background: #f3f4f6; text-align: center; }}
            .check {{ text-align: center; }}
            .money {{ text-align: right; }}
            .total-box {{ margin-top: 18px; margin-left: {margen_panel}px; width: {ancho_panel}px; }}
            .total-box td {{ height: 28px; }}
            .firma-wrap {{ margin-top: 60px; width: {ancho_tabla}px; border: none; }}
            .firma-wrap td {{ border: none; padding: 0; }}
            .firma-box {{ width: {ancho_panel}px; margin-left: {margen_panel}px; border-collapse: collapse; }}
            .firma-box td {{ border: none; border-top: 1px solid #111827; text-align: center; padding-top: 8px; }}
          </style>
        </head>
        <body>
          <div class="folio">Folio: {escape(folio)}</div>
          <h1>Reporte de Plan de Mantenimiento y Servicio</h1>
          <div class="meta">
            <b>Plan:</b> {escape(str(plan.get('nombre_plan', '')))}<br>
            <b>Intervalo:</b> {escape(str(plan.get('intervalo_horas', '')))} horas
          </div>

          <h2>Maquinaria Asociada</h2>
          <table class="full-table" width="{ancho_tabla}">
            <tr><th width="70">ID</th><th width="250">Unidad</th><th width="200">VIN / Serie</th><th width="120">Horómetro</th></tr>
            {maquinas_html}
          </table>

          <h2>Checklist del Plan</h2>
          <table class="full-table" width="{ancho_tabla}">
            <tr><th width="44"></th><th width="300">Tarea</th><th width="220">Observaciones</th><th width="76">Costo</th></tr>
            {tareas_html}
          </table>

          <table class="total-box">
            <tr><th>Total estimado / autorizado</th><td class="money">$</td></tr>
          </table>

          <h2 class="urgent">Urgente: Incidencias no atendidas</h2>
          <table class="full-table" width="{ancho_tabla}">
            <tr><th width="75">Orden</th><th width="175">Unidad</th><th width="120">Fecha</th><th width="270">Descripción</th></tr>
            {incidencias_html}
          </table>

          <table class="firma-wrap" width="{ancho_tabla}">
            <tr><td>
              <table class="firma-box" width="{ancho_panel}">
                <tr><td>Firma / Responsable</td></tr>
              </table>
            </td></tr>
          </table>
        </body>
        </html>
        """
        writer = QPdfWriter(str(ruta_salida))
        writer.setPageSize(QPageSize(QPageSize.A4))
        writer.setResolution(96)
        writer.setPageMargins(QMarginsF(14, 14, 14, 14))
        doc = QTextDocument()
        doc.setPageSize(writer.pageLayout().paintRectPixels(writer.resolution()).size())
        doc.setHtml(html)
        doc.print_(writer)

    @staticmethod
    def _col_name(index):
        name = ""
        while index:
            index, remainder = divmod(index - 1, 26)
            name = chr(65 + remainder) + name
        return name

