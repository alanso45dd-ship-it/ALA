import xlsxwriter
from datetime import datetime

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('Balance_General_Maestro.xlsx')
worksheet_data = workbook.add_worksheet('Datos')
worksheet_balance = workbook.add_worksheet('Balance General')

# Create formats
header_format = workbook.add_format({'bold': True, 'bg_color': '#D9EAD3', 'border': 1})
currency_format = workbook.add_format({'num_format': '$#,##0.00'})
title_format = workbook.add_format({'bold': True, 'font_size': 14})
subtitle_format = workbook.add_format({'bold': True, 'font_size': 12, 'bottom': 1})
total_format = workbook.add_format({'bold': True, 'top': 6, 'bottom': 6, 'num_format': '$#,##0.00'}) # Double line

# --- SHEET 1: DATOS (DATA INPUT) ---

# Data headers
headers = ['Fecha', 'Cuenta', 'Categoría', 'Subcategoría', 'Debe', 'Haber']
worksheet_data.write_row('A1', headers, header_format)

# Sample Data
data = [
    [datetime(2023, 1, 1), 'Caja', 'Activo', 'Circulante', 50000, 0],
    [datetime(2023, 1, 1), 'Bancos', 'Activo', 'Circulante', 150000, 0],
    [datetime(2023, 1, 1), 'Inventario', 'Activo', 'Circulante', 75000, 0],
    [datetime(2023, 1, 2), 'Mobiliario', 'Activo', 'No Circulante', 25000, 0],
    [datetime(2023, 1, 2), 'Proveedores', 'Pasivo', 'Corto Plazo', 0, 30000],
    [datetime(2023, 1, 3), 'Capital Social', 'Patrimonio', 'Capital', 0, 200000],
    [datetime(2023, 1, 4), 'Ventas', 'Ingresos', 'Operativo', 0, 80000], # Not in Balance Sheet directly, creates Retained Earnings context
    [datetime(2023, 1, 5), 'Costo de Ventas', 'Gastos', 'Operativo', 40000, 0], # Not in Balance Sheet directly
    [datetime(2023, 1, 5), 'Utilidad Retenida', 'Patrimonio', 'Resultados', 0, 30000], # Simplified Retained Earnings
    [datetime(2023, 1, 31), 'Resultado del Ejercicio', 'Patrimonio', 'Resultados', 0, 40000], # Net Income to balance the sheet
]

# Write data
row = 1
for item in data:
    worksheet_data.write_datetime(row, 0, item[0], workbook.add_format({'num_format': 'yyyy-mm-dd'}))
    worksheet_data.write_string(row, 1, item[1])
    worksheet_data.write_string(row, 2, item[2])
    worksheet_data.write_string(row, 3, item[3])
    worksheet_data.write_number(row, 4, item[4], currency_format)
    worksheet_data.write_number(row, 5, item[5], currency_format)
    row += 1

# Add Excel Table
worksheet_data.add_table(0, 0, row - 1, 5, {'name': 'TablaDatos', 'columns': [{'header': h} for h in headers]})
worksheet_data.set_column('A:F', 15)


# --- SHEET 2: BALANCE GENERAL (REPORT) ---

worksheet_balance.set_column('A:A', 30) # Account Name
worksheet_balance.set_column('B:B', 20) # Amount

worksheet_balance.write('A1', 'BALANCE GENERAL', title_format)
worksheet_balance.write('A2', 'Generado Automáticamente', subtitle_format)

# --- ACTIVO (ASSETS) ---
worksheet_balance.write('A4', 'ACTIVO', subtitle_format)

# Formula for Dynamic Asset List & Balances using LET, FILTER, UNIQUE, SORT, SUMIFS
# Logic: Filter unique accounts where Category is 'Activo'.
# Then output 2 columns: The Account Name and the Sum (Debe - Haber).
# Note: In a real balance sheet, Assets = Debit - Credit.
asset_formula = """=LET(
    Data, TablaDatos,
    Cuentas, SORT(UNIQUE(FILTER(TablaDatos[Cuenta], TablaDatos[Categoría]="Activo"))),
    Saldos, MAP(Cuentas, LAMBDA(c, SUMIFS(TablaDatos[Debe], TablaDatos[Cuenta], c) - SUMIFS(TablaDatos[Haber], TablaDatos[Cuenta], c))),
    HSTACK(Cuentas, Saldos)
)""".replace('\n', '')

# Since dynamic arrays spill, we just write it in the top-left cell of the range.
worksheet_balance.write_formula('A5', asset_formula)

# Total Activo
# We put this a bit lower down, or use a dynamic position reference if possible.
# However, xlsxwriter doesn't easily support "find last row" logic for formula placement *after* a spill
# unless we hardcode a sufficient gap or use another dynamic array for the total.
# A "Master" way is to put the total at the top or use a separate calculation block.
# Let's put Total Activo in a fixed position for simplicity in this demo, or use a formula that sums the spill range.
# Assuming the list won't exceed 20 rows for this demo.
worksheet_balance.write('A20', 'TOTAL ACTIVO', total_format)
worksheet_balance.write_formula('B20', '=SUM(INDEX(A5#,,2))', total_format)


# --- PASIVO (LIABILITIES) ---
worksheet_balance.write('D4', 'PASIVO', subtitle_format)
worksheet_balance.set_column('D:D', 30)
worksheet_balance.set_column('E:E', 20)

# Liabilities = Credit - Debit
liability_formula = """=LET(
    Data, TablaDatos,
    Cuentas, SORT(UNIQUE(FILTER(TablaDatos[Cuenta], TablaDatos[Categoría]="Pasivo"))),
    Saldos, MAP(Cuentas, LAMBDA(c, SUMIFS(TablaDatos[Haber], TablaDatos[Cuenta], c) - SUMIFS(TablaDatos[Debe], TablaDatos[Cuenta], c))),
    HSTACK(Cuentas, Saldos)
)""".replace('\n', '')

worksheet_balance.write_formula('D5', liability_formula)

worksheet_balance.write('D15', 'TOTAL PASIVO', total_format)
worksheet_balance.write_formula('E15', '=SUM(INDEX(D5#,,2))', total_format)


# --- PATRIMONIO (EQUITY) ---
worksheet_balance.write('D18', 'PATRIMONIO', subtitle_format)

# Equity = Credit - Debit
equity_formula = """=LET(
    Data, TablaDatos,
    Cuentas, SORT(UNIQUE(FILTER(TablaDatos[Cuenta], TablaDatos[Categoría]="Patrimonio"))),
    Saldos, MAP(Cuentas, LAMBDA(c, SUMIFS(TablaDatos[Haber], TablaDatos[Cuenta], c) - SUMIFS(TablaDatos[Debe], TablaDatos[Cuenta], c))),
    HSTACK(Cuentas, Saldos)
)""".replace('\n', '')

worksheet_balance.write_formula('D19', equity_formula)

worksheet_balance.write('D25', 'TOTAL PATRIMONIO', total_format)
worksheet_balance.write_formula('E25', '=SUM(INDEX(D19#,,2))', total_format)


# --- TOTAL PASIVO + PATRIMONIO ---
worksheet_balance.write('D27', 'TOTAL PASIVO + PATRIMONIO', total_format)
worksheet_balance.write_formula('E27', '=E15 + E25', total_format)


# --- CHECK (VALIDATION) ---
worksheet_balance.write('A27', 'CONTROL:', subtitle_format)
worksheet_balance.write_formula('B27', '=IF(ABS(B20 - E27) < 0.01, "OK - BALANCEADO", "ERROR - DESCUADRE")', workbook.add_format({'bold': True, 'color': 'green'}))


workbook.close()
