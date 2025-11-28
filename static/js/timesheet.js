// Timesheet JavaScript
// Simplified version - calendar functions removed (now in sidebar)

/**
 * Update summary statistics dynamically (updates sidebar stats)
 */
function updateSummaryStats() {
    let totalHours = 0;
    let recordCount = 0;

    document.querySelectorAll('tr.timesheet-row').forEach(row => {
        const totalCell = row.querySelector('.total-hours');
        if (totalCell && totalCell.textContent !== '-') {
            const hoursText = totalCell.textContent.replace('h', '').trim();
            const hours = parseFloat(hoursText);
            if (!isNaN(hours) && hours > 0) {
                totalHours += hours;
                recordCount++;
            }
        }
    });

    // Update sidebar statistics
    updateSidebarStats(recordCount, totalHours.toFixed(1));
}

/**
 * Initialize timesheet
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Timesheet initialized (minimalist version)');

    // Recreate Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // Scroll to today's row on load
    const today = new Date();
    const todayStr = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    const todayRow = document.querySelector(`tr.timesheet-row[data-date="${todayStr}"]`);

    if (todayRow) {
        setTimeout(() => {
            todayRow.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }, 500);
    }
});
