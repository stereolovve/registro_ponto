// Inline Editor JavaScript
// Handles Excel-like inline editing, AJAX saves, and real-time calculations

// Track if a save is in progress to prevent duplicate requests
const savingCells = new Set();

/**
 * "Bater Ponto" - Fill current time in the input next to the clicked button
 * @param {HTMLElement} buttonElement - The clock icon button that was clicked
 */
function baterPontoInline(buttonElement) {
    const input = buttonElement.previousElementSibling;
    if (input && input.tagName === 'INPUT' && input.type === 'time') {
        input.value = getCurrentTime();
        // Trigger save
        saveTimeInput(input);
    }
}

/**
 * Save a time input value via AJAX
 * @param {HTMLInputElement} input - The time input element
 */
async function saveTimeInput(input) {
    const field = input.dataset.field;
    const date = input.dataset.date;
    const value = input.value;
    const row = input.closest('tr.timesheet-row');
    const recordId = row.dataset.recordId;

    // Validate time order before saving
    if (!validateRowTimes(row)) {
        showToast('Horário de saída deve ser maior que horário de entrada', 'error');
        return;
    }

    try {
        // If no record exists yet, create one first
        if (!recordId || recordId === '') {
            await createRecordForDate(date, row);
            // After creating, save the field
            await saveField(row.dataset.recordId, field, value);
        } else {
            await saveField(recordId, field, value);
        }

        // Update total hours for this row
        updateRowTotalHours(row);

        // Update summary statistics (updates sidebar)
        updateSummaryStats();

    } catch (error) {
        console.error('Error saving time:', error);
        showToast(error.message || 'Erro ao salvar horário', 'error');
    }
}

/**
 * Save work code selection via AJAX
 * @param {HTMLSelectElement} select - The work code select element
 */
async function saveWorkCode(select) {
    const date = select.dataset.date;
    const value = select.value;
    const row = select.closest('tr.timesheet-row');
    const recordId = row.dataset.recordId;

    if (!value) return; // Don't save empty work code

    try {
        // If no record exists yet, create one first
        if (!recordId || recordId === '') {
            await createRecordForDate(date, row, value);
        } else {
            await saveField(recordId, 'work_code_id', value);
        }

        showToast('Código de trabalho atualizado', 'success');

    } catch (error) {
        console.error('Error saving work code:', error);
        showToast(error.message || 'Erro ao salvar código de trabalho', 'error');
    }
}

/**
 * Create a new TimeRecord for a specific date
 * @param {string} date - Date in YYYY-MM-DD format
 * @param {HTMLElement} row - The table row element
 * @param {string} workCodeId - Optional work code ID
 * @returns {Promise<number>} The new record ID
 */
async function createRecordForDate(date, row, workCodeId = null) {
    const cellKey = `create-${date}`;

    // Prevent duplicate creation requests
    if (savingCells.has(cellKey)) {
        throw new Error('Já criando registro...');
    }

    savingCells.add(cellKey);

    try {
        const response = await fetch('/api/time-records/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                date: date,
                work_code_id: workCodeId
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.errors || 'Erro ao criar registro');
        }

        // Update row with new record ID
        row.dataset.recordId = data.record_id;

        return data.record_id;

    } finally {
        savingCells.delete(cellKey);
    }
}

/**
 * Save a single field via AJAX
 * @param {number} recordId - The TimeRecord ID
 * @param {string} field - Field name (entrada1, saida1, etc.)
 * @param {string} value - New value
 */
async function saveField(recordId, field, value) {
    const cellKey = `${recordId}-${field}`;

    // Prevent duplicate save requests
    if (savingCells.has(cellKey)) {
        return;
    }

    savingCells.add(cellKey);

    try {
        const response = await fetch(`/api/time-records/${recordId}/update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                field: field,
                value: value || null
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.errors || 'Erro ao salvar');
        }

        // Show success feedback
        showSuccessCheckmark(cellKey);

    } finally {
        savingCells.delete(cellKey);
    }
}

/**
 * Show a brief checkmark animation on successful save
 * @param {string} cellKey - Unique identifier for the cell
 */
function showSuccessCheckmark(cellKey) {
    // Visual feedback: brief green border on the input
    const inputs = document.querySelectorAll('input.time-input, select.work-code-select');
    inputs.forEach(input => {
        const row = input.closest('tr');
        const recordId = row?.dataset.recordId;
        const field = input.dataset.field;

        if (recordId && field && `${recordId}-${field}` === cellKey) {
            input.classList.add('ring-2', 'ring-green-500');
            setTimeout(() => {
                input.classList.remove('ring-2', 'ring-green-500');
            }, 1000);
        }
    });
}

/**
 * Validate that exit times are after entry times in a row
 * @param {HTMLElement} row - The table row
 * @returns {boolean} True if valid
 */
function validateRowTimes(row) {
    const periods = [
        { entrada: 'entrada1', saida: 'saida1' },
        { entrada: 'entrada2', saida: 'saida2' },
        { entrada: 'entrada3', saida: 'saida3' }
    ];

    for (const period of periods) {
        const entradaInput = row.querySelector(`input[data-field="${period.entrada}"]`);
        const saidaInput = row.querySelector(`input[data-field="${period.saida}"]`);

        if (entradaInput && saidaInput) {
            const entrada = entradaInput.value;
            const saida = saidaInput.value;

            if (entrada && saida && !validateTimeOrder(entrada, saida)) {
                return false;
            }
        }
    }

    return true;
}

/**
 * Update total hours display for a row
 * @param {HTMLElement} row - The table row
 */
function updateRowTotalHours(row) {
    let total = 0;

    const periods = [
        { entrada: 'entrada1', saida: 'saida1' },
        { entrada: 'entrada2', saida: 'saida2' },
        { entrada: 'entrada3', saida: 'saida3' }
    ];

    periods.forEach(period => {
        const entradaInput = row.querySelector(`input[data-field="${period.entrada}"]`);
        const saidaInput = row.querySelector(`input[data-field="${period.saida}"]`);

        if (entradaInput && saidaInput) {
            const entrada = entradaInput.value;
            const saida = saidaInput.value;
            total += calculateHours(entrada, saida);
        }
    });

    const totalCell = row.querySelector('.total-hours');
    if (totalCell) {
        if (total > 0) {
            totalCell.innerHTML = `${total.toFixed(1)}h`;
            totalCell.classList.remove('text-gray-400');
            totalCell.classList.add('font-semibold', 'text-gray-900', 'dark:text-white');
        } else {
            totalCell.innerHTML = '<span class="text-gray-400">-</span>';
        }
    }
}


/**
 * Handle Tab key navigation between cells
 * @param {KeyboardEvent} e - The keyboard event
 * @param {HTMLElement} currentInput - Current input element
 */
function handleTabNavigation(e, currentInput) {
    if (e.key !== 'Tab') return;

    e.preventDefault();

    const row = currentInput.closest('tr');
    const allInputs = Array.from(row.querySelectorAll('input.time-input, select.work-code-select'));
    const currentIndex = allInputs.indexOf(currentInput);

    if (e.shiftKey) {
        // Shift+Tab: Go to previous input
        const prevIndex = currentIndex - 1;
        if (prevIndex >= 0) {
            allInputs[prevIndex].focus();
        } else {
            // Go to last input of previous row
            const prevRow = row.previousElementSibling;
            if (prevRow && prevRow.classList.contains('timesheet-row')) {
                const prevInputs = prevRow.querySelectorAll('input.time-input, select.work-code-select');
                if (prevInputs.length > 0) {
                    prevInputs[prevInputs.length - 1].focus();
                }
            }
        }
    } else {
        // Tab: Go to next input
        const nextIndex = currentIndex + 1;
        if (nextIndex < allInputs.length) {
            allInputs[nextIndex].focus();
        } else {
            // Go to first input of next row
            const nextRow = row.nextElementSibling;
            if (nextRow && nextRow.classList.contains('timesheet-row')) {
                const nextInput = nextRow.querySelector('input.time-input, select.work-code-select');
                if (nextInput) {
                    nextInput.focus();
                }
            }
        }
    }
}

/**
 * Handle Enter key to move to next row, same column
 * @param {KeyboardEvent} e - The keyboard event
 * @param {HTMLElement} currentInput - Current input element
 */
function handleEnterNavigation(e, currentInput) {
    if (e.key !== 'Enter') return;

    e.preventDefault();

    const row = currentInput.closest('tr');
    const field = currentInput.dataset.field;

    // Move to same field in next row
    const nextRow = row.nextElementSibling;
    if (nextRow && nextRow.classList.contains('timesheet-row')) {
        const nextInput = nextRow.querySelector(`[data-field="${field}"]`);
        if (nextInput) {
            nextInput.focus();
        }
    }
}

/**
 * Setup event listeners for inline editing
 */
function setupInlineEditing() {
    // Time inputs
    document.querySelectorAll('input.time-input').forEach(input => {
        // Save on blur (when user leaves the field)
        input.addEventListener('blur', debounce(function() {
            saveTimeInput(this);
        }, 300));

        // Keyboard navigation
        input.addEventListener('keydown', function(e) {
            handleTabNavigation(e, this);
            handleEnterNavigation(e, this);
        });

        // Real-time hour calculation on input
        input.addEventListener('input', debounce(function() {
            const row = this.closest('tr');
            updateRowTotalHours(row);
        }, 200));
    });

    // Work code selects
    document.querySelectorAll('select.work-code-select').forEach(select => {
        // Save on change
        select.addEventListener('change', function() {
            saveWorkCode(this);
        });

        // Keyboard navigation
        select.addEventListener('keydown', function(e) {
            handleTabNavigation(e, this);
            handleEnterNavigation(e, this);
        });
    });

    console.log('Inline editing initialized');
}

/**
 * Initialize inline editor
 */
document.addEventListener('DOMContentLoaded', () => {
    setupInlineEditing();

    // Calculate initial totals for all rows
    document.querySelectorAll('tr.timesheet-row').forEach(row => {
        updateRowTotalHours(row);
    });
});
