// Default Data from the Image
const defaultItems = [
    {
        item: 1,
        codigo: "202756",
        nroBulto: 4,
        tipoBulto: "PALLETS (96 CAJAS)",
        cantidad: 51523.00,
        unidMed: "MTK",
        lote: "154344-001, 154344-005",
        descripcion: "GEOMEMBRANA HDPE LISA 1.50-7.01X210",
        pesoNeto: 1161.60,
        pesoBruto: 1219.20
    }
];

let items = [...defaultItems];

function calculateTotals() {
    return items.reduce((acc, item) => {
        acc.totalNeto += parseFloat(item.pesoNeto) || 0;
        acc.totalBruto += parseFloat(item.pesoBruto) || 0;
        acc.totalBultos += parseFloat(item.nroBulto) || 0;
        return acc;
    }, { totalNeto: 0, totalBruto: 0, totalBultos: 0 });
}

function renderTable(tbody) {
    tbody.innerHTML = '';
    items.forEach((item) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.item}</td>
            <td>${item.codigo}</td>
            <td class="highlight-yellow">${item.nroBulto}</td>
            <td class="highlight-yellow">${item.tipoBulto}</td>
            <td>${formatNumber(item.cantidad)}</td>
            <td>${item.unidMed}</td>
            <td class="highlight-yellow">${item.lote}</td>
            <td>${item.descripcion}</td>
            <td class="highlight-yellow">${formatNumber(item.pesoNeto)}</td>
            <td class="highlight-yellow">${formatNumber(item.pesoBruto)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function renderInputs(inputsContainer) {
    inputsContainer.innerHTML = '';
    items.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'item-row-input';
        div.innerHTML = `
            <div style="grid-column: span 3; font-weight: bold;">Item ${index + 1} <button onclick="removeItem(${index})" style="float:right; color: red;">X</button></div>
            <input type="text" placeholder="Código" value="${item.codigo}" onchange="updateItem(${index}, 'codigo', this.value)">
            <input type="number" placeholder="Nro Bulto" value="${item.nroBulto}" onchange="updateItem(${index}, 'nroBulto', this.value)">
            <input type="text" placeholder="Tipo Bulto" value="${item.tipoBulto}" onchange="updateItem(${index}, 'tipoBulto', this.value)">
            <input type="number" placeholder="Cantidad" value="${item.cantidad}" onchange="updateItem(${index}, 'cantidad', this.value)">
            <input type="text" placeholder="Unid. Med." value="${item.unidMed}" onchange="updateItem(${index}, 'unidMed', this.value)">
            <input type="text" placeholder="Lote" value="${item.lote}" onchange="updateItem(${index}, 'lote', this.value)">
            <input type="text" placeholder="Descripción" value="${item.descripcion}" onchange="updateItem(${index}, 'descripcion', this.value)" style="grid-column: span 3">
            <input type="number" placeholder="Peso Neto" value="${item.pesoNeto}" onchange="updateItem(${index}, 'pesoNeto', this.value)">
            <input type="number" placeholder="Peso Bruto" value="${item.pesoBruto}" onchange="updateItem(${index}, 'pesoBruto', this.value)">
        `;
        inputsContainer.appendChild(div);
    });
}

function updateTotalsDisplay(totals) {
    document.getElementById('total-bultos').innerText = totals.totalBultos;
    document.getElementById('total-neto').innerText = formatNumber(totals.totalNeto);
    document.getElementById('total-bruto').innerText = formatNumber(totals.totalBruto);
    document.getElementById('final-total-neto').innerText = formatNumber(totals.totalNeto);
    document.getElementById('final-total-bruto').innerText = formatNumber(totals.totalBruto);
}

function renderItems() {
    const tbody = document.getElementById('items-table-body');
    const inputsContainer = document.getElementById('items-inputs');

    renderTable(tbody);
    renderInputs(inputsContainer);

    const totals = calculateTotals();
    updateTotalsDisplay(totals);
}

function updateItem(index, field, value) {
    items[index][field] = value;
    // Special handling for numeric fields to ensure they are stored as numbers if possible
    if (['nroBulto', 'cantidad', 'pesoNeto', 'pesoBruto'].includes(field)) {
         items[index][field] = parseFloat(value) || 0;
    }
    renderItems();
}

function addItemRow() {
    const newItem = {
        item: items.length + 1,
        codigo: "",
        nroBulto: 0,
        tipoBulto: "",
        cantidad: 0,
        unidMed: "MTK",
        lote: "",
        descripcion: "",
        pesoNeto: 0,
        pesoBruto: 0
    };
    items.push(newItem);
    renderItems();
}

function removeItem(index) {
    items.splice(index, 1);
    // Re-index items
    items.forEach((item, i) => item.item = i + 1);
    renderItems();
}

function formatNumber(num) {
    if (num === undefined || num === null) return "0.00";
    return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// Global Event Listeners for Static Inputs
const inputMap = {
    'input-factura': 'disp-factura',
    'input-fecha': 'disp-fecha',
    'input-referencia': 'disp-referencia',
    'input-importador-nombre': 'disp-importador-nombre',
    'input-importador-rut': 'disp-importador-rut',
    'input-importador-direccion': 'disp-importador-direccion',
    'input-contacto-atencion': 'disp-contacto-atencion',
    'input-contacto-telefono': 'disp-contacto-telefono',
    'input-contacto-correo': 'disp-contacto-correo',
    'input-partida': 'disp-partida'
};

for (const [inputId, displayId] of Object.entries(inputMap)) {
    const inputElement = document.getElementById(inputId);
    if (inputElement) {
        inputElement.addEventListener('input', (e) => {
            document.getElementById(displayId).innerText = e.target.value;
        });
    }
}

// Initial Render
renderItems();
