import xlsxwriter

# Define the filename
filename = 'Balance_General_Maestro.xlsx'

# Create a workbook and add a worksheet
workbook = xlsxwriter.Workbook(filename)
worksheet_input = workbook.add_worksheet('Datos')
worksheet_report = workbook.add_worksheet('Balance_General')

# --- Formatting ---
# Header format
header_format = workbook.add_format({
    'bold': True,
    'font_color': 'white',
    'bg_color': '#4F81BD',
    'border': 1,
    'align': 'center',
    'valign': 'vcenter'
})

# Currency format
currency_format = workbook.add_format({
    'num_format': '"$"#,##0.00',
    'border': 1
})

# Standard cell format
cell_format = workbook.add_format({
    'border': 1
})

# Bold format for totals
bold_format = workbook.add_format({
    'bold': True,
    'border': 1
})

# Title format for report
title_format = workbook.add_format({
    'bold': True,
    'font_size': 16,
    'align': 'center',
    'valign': 'vcenter',
    'bg_color': '#DCE6F1',
    'border': 1
})

# Status format (Green - Balanced)
status_green = workbook.add_format({
    'bg_color': '#C6EFCE',
    'font_color': '#006100',
    'bold': True,
    'align': 'center',
    'border': 1
})

# Status format (Red - Unbalanced)
status_red = workbook.add_format({
    'bg_color': '#FFC7CE',
    'font_color': '#9C0006',
    'bold': True,
    'align': 'center',
    'border': 1
})

# --- Sheet 1: Input Data (Datos) ---

# Define headers
headers = ['Cuenta', 'Categoria', 'Subcategoria', 'Monto']
worksheet_input.write_row('A1', headers, header_format)

# Sample Data
data = [
    ['Caja', 'Activo', 'Corriente', 15000],
    ['Bancos', 'Activo', 'Corriente', 45000],
    ['Clientes', 'Activo', 'Corriente', 30000],
    ['Inventarios', 'Activo', 'Corriente', 25000],
    ['Terrenos', 'Activo', 'No Corriente', 100000],
    ['Edificios', 'Activo', 'No Corriente', 200000],
    ['Maquinaria', 'Activo', 'No Corriente', 50000],
    ['Proveedores', 'Pasivo', 'Corriente', 40000],
    ['Cuentas por Pagar', 'Pasivo', 'Corriente', 20000],
    ['Impuestos por Pagar', 'Pasivo', 'Corriente', 15000],
    ['Prestamos Largo Plazo', 'Pasivo', 'No Corriente', 120000],
    ['Capital Social', 'Patrimonio', 'Patrimonio', 200000],
    ['Utilidades Retenidas', 'Patrimonio', 'Patrimonio', 70000],
]

# Write data
row = 1
for item in data:
    worksheet_input.write_row(row, 0, item)
    worksheet_input.set_row(row, None, cell_format)  # Apply default border
    worksheet_input.write(row, 3, item[3], currency_format) # Apply currency to amount
    row += 1

# Create an Excel Table (List Object) for the data range
worksheet_input.add_table(0, 0, len(data), 3, {
    'columns': [{'header': 'Cuenta'},
                {'header': 'Categoria'},
                {'header': 'Subcategoria'},
                {'header': 'Monto'}],
    'name': 'TableDatos',
    'style': 'TableStyleMedium9'
})

worksheet_input.set_column('A:A', 25)
worksheet_input.set_column('B:C', 15)
worksheet_input.set_column('D:D', 15)

# --- Sheet 2: Balance General Report ---

# Report Structure
worksheet_report.merge_range('A1:E1', 'BALANCE GENERAL - REPORTE MAESTRO', title_format)

# Left Side: Assets
worksheet_report.write('A3', 'ACTIVOS', bold_format)
worksheet_report.write('A4', 'Activo Corriente', cell_format)
worksheet_report.write('A5', 'Activo No Corriente', cell_format)
worksheet_report.write('A6', 'TOTAL ACTIVOS', bold_format)

# Right Side: Liabilities & Equity
worksheet_report.write('D3', 'PASIVOS Y PATRIMONIO', bold_format)
worksheet_report.write('D4', 'Pasivo Corriente', cell_format)
worksheet_report.write('D5', 'Pasivo No Corriente', cell_format)
worksheet_report.write('D6', 'TOTAL PASIVOS', bold_format)
worksheet_report.write('D7', 'Patrimonio', cell_format)
worksheet_report.write('D8', 'TOTAL PASIVO + PATRIMONIO', bold_format)

# Formulas utilizing structured references from TableDatos
# Syntax for SUMIFS in Excel: SUMIFS(Sum_Range, Criteria_Range1, Criteria1, ...)
# Note: Excel formulas use localized separators (comma vs semicolon) depending on region.
# xlsxwriter writes the English formula and Excel translates it.

# Assets Formulas
f_act_corr = '=SUMIFS(TableDatos[Monto], TableDatos[Categoria], "Activo", TableDatos[Subcategoria], "Corriente")'
f_act_no_corr = '=SUMIFS(TableDatos[Monto], TableDatos[Categoria], "Activo", TableDatos[Subcategoria], "No Corriente")'
f_total_act = '=SUM(B4:B5)'

worksheet_report.write_formula('B4', f_act_corr, currency_format)
worksheet_report.write_formula('B5', f_act_no_corr, currency_format)
worksheet_report.write_formula('B6', f_total_act, currency_format)

# Liabilities Formulas
f_pas_corr = '=SUMIFS(TableDatos[Monto], TableDatos[Categoria], "Pasivo", TableDatos[Subcategoria], "Corriente")'
f_pas_no_corr = '=SUMIFS(TableDatos[Monto], TableDatos[Categoria], "Pasivo", TableDatos[Subcategoria], "No Corriente")'
f_total_pas = '=SUM(E4:E5)'

worksheet_report.write_formula('E4', f_pas_corr, currency_format)
worksheet_report.write_formula('E5', f_pas_no_corr, currency_format)
worksheet_report.write_formula('E6', f_total_pas, currency_format)

# Equity Formulas
f_patrimonio = '=SUMIFS(TableDatos[Monto], TableDatos[Categoria], "Patrimonio")'
f_total_pas_pat = '=E6+E7'

worksheet_report.write_formula('E7', f_patrimonio, currency_format)
worksheet_report.write_formula('E8', f_total_pas_pat, currency_format)

# Validation Check
worksheet_report.write('A10', 'ESTADO DEL BALANCE:', bold_format)
check_formula = '=IF(ABS(B6-E8)<0.01, "BALANCEADO", "DESCUADRADO")'
worksheet_report.write_formula('B10', check_formula)

# Conditional Formatting for the Check Cell (B10)
worksheet_report.conditional_format('B10', {
    'type': 'cell',
    'criteria': 'equal to',
    'value': '"BALANCEADO"',
    'format': status_green
})
worksheet_report.conditional_format('B10', {
    'type': 'cell',
    'criteria': 'not equal to',
    'value': '"BALANCEADO"',
    'format': status_red
})

# Adjust column widths
worksheet_report.set_column('A:A', 25)
worksheet_report.set_column('B:B', 20)
worksheet_report.set_column('C:C', 5) # Spacer
worksheet_report.set_column('D:D', 25)
worksheet_report.set_column('E:E', 20)

workbook.close()
print(f"File {filename} created successfully.")
