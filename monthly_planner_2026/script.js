document.addEventListener('DOMContentLoaded', () => {
    // --- State ---
    let currentDate = new Date(2026, 0, 1); // Start Jan 2026
    let tasks = JSON.parse(localStorage.getItem('planner_tasks_2026')) || {
        'unscheduled': []
    };
    if (!tasks['unscheduled']) tasks['unscheduled'] = [];

    let selectedDate = null; // YYYY-MM-DD

    // --- DOM Elements ---
    const monthYearDisplay = document.getElementById('current-month-year');
    const calendarGrid = document.getElementById('calendar-grid');
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');
    const todayBtn = document.getElementById('today-btn');

    // Modal
    const modal = document.getElementById('task-modal');
    const modalTitle = document.getElementById('modal-date-title');
    const closeModalBtn = document.getElementById('close-modal');
    const dailyTaskInput = document.getElementById('daily-task-input');
    const addDailyTaskBtn = document.getElementById('add-daily-task-btn');
    const dailyTaskList = document.getElementById('daily-task-list');

    // Sidebar
    const unscheduledInput = document.getElementById('unscheduled-input');
    const addUnscheduledBtn = document.getElementById('add-unscheduled-btn');
    const unscheduledList = document.getElementById('unscheduled-list');

    // --- Constants ---
    const MONTH_NAMES = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];

    // --- Initialization ---
    renderCalendar();
    renderUnscheduledTasks();

    // --- Event Listeners ---
    prevBtn.addEventListener('click', () => changeMonth(-1));
    nextBtn.addEventListener('click', () => changeMonth(1));
    todayBtn.addEventListener('click', () => {
        currentDate = new Date(); // Go to actual today
        renderCalendar();
    });

    closeModalBtn.addEventListener('click', () => modal.classList.add('hidden'));

    // Add Task (Sidebar)
    addUnscheduledBtn.addEventListener('click', () => {
        addUnscheduledTask();
    });
    unscheduledInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addUnscheduledTask();
    });

    // Add Task (Modal)
    addDailyTaskBtn.addEventListener('click', () => {
        addDailyTask();
    });
    dailyTaskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addDailyTask();
    });

    // --- Core Logic ---

    function saveTasks() {
        localStorage.setItem('planner_tasks_2026', JSON.stringify(tasks));
        renderCalendar(); // Re-render to update indicators
    }

    function changeMonth(delta) {
        currentDate.setMonth(currentDate.getMonth() + delta);
        renderCalendar();
    }

    function getFormattedDate(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
    }

    function renderCalendar() {
        const year = currentDate.getFullYear();
        const month = currentDate.getMonth();

        monthYearDisplay.textContent = `${MONTH_NAMES[month]} ${year}`;

        // Clear grid
        calendarGrid.innerHTML = '';

        // First day of month
        const firstDay = new Date(year, month, 1);
        const startDayIndex = firstDay.getDay(); // 0 (Sun) to 6 (Sat)

        // Days in month
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Empty cells for previous month
        for (let i = 0; i < startDayIndex; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.classList.add('calendar-day', 'empty');
            calendarGrid.appendChild(emptyCell);
        }

        // Days
        const today = new Date();
        const isCurrentMonth = today.getFullYear() === year && today.getMonth() === month;

        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('calendar-day');

            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

            // Check if today
            if (isCurrentMonth && day === today.getDate()) {
                dayCell.classList.add('today');
            }

            // Day Number
            const dayNum = document.createElement('div');
            dayNum.classList.add('day-number');
            dayNum.textContent = day;
            dayCell.appendChild(dayNum);

            // Indicators
            const indicatorsContainer = document.createElement('div');
            indicatorsContainer.classList.add('task-indicators-container');
            if (tasks[dateStr] && tasks[dateStr].length > 0) {
                const count = tasks[dateStr].filter(t => !t.completed).length;
                // Show max 5 dots
                for(let i=0; i < Math.min(count, 5); i++) {
                    const dot = document.createElement('span');
                    dot.classList.add('task-indicator');
                    indicatorsContainer.appendChild(dot);
                }
            }
            dayCell.appendChild(indicatorsContainer);

            // Click Event
            dayCell.addEventListener('click', () => openModal(dateStr));

            calendarGrid.appendChild(dayCell);
        }
    }

    function openModal(dateStr) {
        selectedDate = dateStr;
        modalTitle.textContent = `Tareas: ${dateStr}`;
        renderDailyTasks();
        modal.classList.remove('hidden');
        dailyTaskInput.focus();
    }

    function renderDailyTasks() {
        dailyTaskList.innerHTML = '';
        const dayTasks = tasks[selectedDate] || [];

        dayTasks.forEach((task, index) => {
            const li = createTaskElement(task, index, 'daily');
            dailyTaskList.appendChild(li);
        });
    }

    function renderUnscheduledTasks() {
        unscheduledList.innerHTML = '';
        const unscheduled = tasks['unscheduled'] || [];

        unscheduled.forEach((task, index) => {
            const li = createTaskElement(task, index, 'unscheduled');
            unscheduledList.appendChild(li);
        });
    }

    function createTaskElement(task, index, type) {
        const li = document.createElement('li');
        li.classList.add('task-item');
        if (task.completed) li.classList.add('completed');

        const span = document.createElement('span');
        span.textContent = task.text;
        li.appendChild(span);

        const actions = document.createElement('div');
        actions.classList.add('task-actions');

        const checkBtn = document.createElement('button');
        checkBtn.textContent = '✔';
        checkBtn.classList.add('check-btn');
        checkBtn.onclick = () => toggleTask(index, type);

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '🗑'; // trash icon
        deleteBtn.classList.add('delete-btn');
        deleteBtn.onclick = () => deleteTask(index, type);

        actions.appendChild(checkBtn);
        actions.appendChild(deleteBtn);
        li.appendChild(actions);

        return li;
    }

    function addDailyTask() {
        const text = dailyTaskInput.value.trim();
        if (!text) return;

        if (!tasks[selectedDate]) tasks[selectedDate] = [];

        tasks[selectedDate].push({
            id: Date.now(),
            text: text,
            completed: false
        });

        dailyTaskInput.value = '';
        saveTasks();
        renderDailyTasks();
    }

    function addUnscheduledTask() {
        const text = unscheduledInput.value.trim();
        if (!text) return;

        tasks['unscheduled'].push({
            id: Date.now(),
            text: text,
            completed: false
        });

        unscheduledInput.value = '';
        saveTasks();
        renderUnscheduledTasks();
    }

    function toggleTask(index, type) {
        if (type === 'daily') {
            tasks[selectedDate][index].completed = !tasks[selectedDate][index].completed;
            renderDailyTasks();
        } else {
            tasks['unscheduled'][index].completed = !tasks['unscheduled'][index].completed;
            renderUnscheduledTasks();
        }
        saveTasks();
    }

    function deleteTask(index, type) {
        if (confirm('¿Borrar tarea?')) {
            if (type === 'daily') {
                tasks[selectedDate].splice(index, 1);
                renderDailyTasks();
            } else {
                tasks['unscheduled'].splice(index, 1);
                renderUnscheduledTasks();
            }
            saveTasks();
        }
    }
});
