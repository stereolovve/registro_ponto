// Sidebar Timesheet Navigation
// Handles month/year navigation from the sidebar controls

/**
 * Navigate to previous or next month from sidebar
 * @param {number} delta - Number of months to navigate (+1 or -1)
 */
function sidebarNavigateMonth(delta) {
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
 * Change month/year based on sidebar select dropdowns
 */
function sidebarChangeMonthYear() {
    const mes = document.getElementById('sidebar-mes-select').value;
    const ano = document.getElementById('sidebar-ano-select').value;

    window.location.href = `/timesheet/?mes=${mes}&ano=${ano}`;
}

/**
 * Go to current month from sidebar button
 */
function goToToday() {
    const today = new Date();
    const mes = today.getMonth() + 1; // JavaScript months are 0-indexed
    const ano = today.getFullYear();

    window.location.href = `/timesheet/?mes=${mes}&ano=${ano}`;
}

/**
 * Update sidebar month display
 */
function updateSidebarMonthDisplay() {
    const display = document.getElementById('sidebar-month-display');
    if (display) {
        const monthNames = [
            'JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO',
            'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO'
        ];
        display.textContent = `${monthNames[currentMonth - 1]} ${currentYear}`;
    }
}

/**
 * Update statistics in sidebar
 * @param {number} days - Number of days worked
 * @param {number} hours - Total hours
 */
function updateSidebarStats(days, hours) {
    const diasElement = document.getElementById('sidebar-total-dias');
    const horasElement = document.getElementById('sidebar-total-horas');

    if (diasElement) {
        diasElement.textContent = `${days} dias`;
    }

    if (horasElement) {
        horasElement.textContent = `${hours}h`;
    }
}

// Initialize sidebar on page load
document.addEventListener('DOMContentLoaded', () => {
    updateSidebarMonthDisplay();
});
