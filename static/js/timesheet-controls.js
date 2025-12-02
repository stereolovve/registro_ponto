// Timesheet Controls Navigation
// Handles month/year navigation from the timesheet controls

/**
 * Navigate to previous or next month
 * @param {number} delta - Number of months to navigate (+1 or -1)
 */
function navigateMonth(delta) {
    let mes = currentMonth + delta;
    let ano = currentYear;

    // Handle year transitions
    if (mes > 12) {
        mes = 1;
        ano++;
    } else if (mes < 1) {
        mes = 12;
        ano--;
    }

    // Reload page with new month/year
    window.location.href = `/timesheet/?mes=${mes}&ano=${ano}`;
}

/**
 * Change month/year based on select dropdowns
 */
function changeMonthYear() {
    const mes = document.getElementById('mes-select').value;
    const ano = document.getElementById('ano-select').value;

    window.location.href = `/timesheet/?mes=${mes}&ano=${ano}`;
}

/**
 * Go to current month
 */
function goToToday() {
    const today = new Date();
    const mes = today.getMonth() + 1; // JavaScript months are 0-indexed
    const ano = today.getFullYear();

    window.location.href = `/timesheet/?mes=${mes}&ano=${ano}`;
}

/**
 * Update month display
 */
function updateMonthDisplay() {
    const display = document.getElementById('month-display');
    if (display) {
        const monthNames = [
            'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
            'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
        ];
        display.textContent = `${monthNames[currentMonth - 1]} ${currentYear}`;
    }
}

/**
 * Update statistics display
 * @param {number} days - Number of days worked
 * @param {number} hours - Total hours
 */
function updateStats(days, hours) {
    const diasElement = document.getElementById('total-dias');
    const horasElement = document.getElementById('total-horas');

    if (diasElement) {
        diasElement.textContent = days;
    }

    if (horasElement) {
        horasElement.textContent = hours;
    }
}

// Initialize controls on page load
document.addEventListener('DOMContentLoaded', () => {
    updateMonthDisplay();
});
