// Time Utilities
// Shared functions for time calculations and formatting

/**
 * Get current time as HH:MM string
 * @returns {string} Current time in HH:MM format
 */
function getCurrentTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * Calculate hours between two times (HH:MM format)
 * @param {string} entrada - Entry time (HH:MM)
 * @param {string} saida - Exit time (HH:MM)
 * @returns {number} Hours as decimal
 */
function calculateHours(entrada, saida) {
    if (!entrada || !saida) return 0;

    // Handle both HH:MM and HH:MM:SS formats
    const [h1, m1] = entrada.split(':').map(Number);
    const [h2, m2] = saida.split(':').map(Number);

    const minutes1 = h1 * 60 + m1;
    const minutes2 = h2 * 60 + m2;

    const diff = minutes2 - minutes1;
    return Math.max(0, diff / 60); // Ensure non-negative
}

/**
 * Format time string to HH:MM
 * @param {string} timeString - Time string to format
 * @returns {string} Formatted time (HH:MM)
 */
function formatTime(timeString) {
    if (!timeString) return '';

    // If already in HH:MM format, return as is
    if (/^\d{2}:\d{2}$/.test(timeString)) {
        return timeString;
    }

    // If in HH:MM:SS format, trim seconds
    if (/^\d{2}:\d{2}:\d{2}$/.test(timeString)) {
        return timeString.substring(0, 5);
    }

    return timeString;
}

/**
 * Parse time string to minutes since midnight
 * @param {string} timeString - Time in HH:MM format
 * @returns {number} Minutes since midnight
 */
function parseTimeToMinutes(timeString) {
    if (!timeString) return 0;

    const [hours, minutes] = timeString.split(':').map(Number);
    return hours * 60 + minutes;
}

/**
 * Convert minutes to HH:MM format
 * @param {number} minutes - Minutes since midnight
 * @returns {string} Time in HH:MM format
 */
function minutesToTime(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}`;
}

/**
 * Validate that exit time is after entry time
 * @param {string} entrada - Entry time (HH:MM)
 * @param {string} saida - Exit time (HH:MM)
 * @returns {boolean} True if valid
 */
function validateTimeOrder(entrada, saida) {
    if (!entrada || !saida) return true; // Empty is valid

    const minutes1 = parseTimeToMinutes(entrada);
    const minutes2 = parseTimeToMinutes(saida);

    return minutes2 > minutes1;
}

/**
 * Calculate total hours from multiple periods
 * @param {Array<Object>} periods - Array of {entrada, saida} objects
 * @returns {number} Total hours as decimal
 */
function calculateTotalHours(periods) {
    return periods.reduce((total, period) => {
        return total + calculateHours(period.entrada, period.saida);
    }, 0);
}

/**
 * Show a toast notification
 * @param {string} message - Message to display
 * @param {string} type - 'success', 'error', 'info', or 'warning'
 */
function showToast(message, type = 'info') {
    // Check if toast container exists, create if not
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toast = document.createElement('div');

    // Set colors based on type
    const colors = {
        success: 'bg-green-600',
        error: 'bg-red-600',
        warning: 'bg-yellow-600',
        info: 'bg-blue-600'
    };

    toast.className = `${colors[type] || colors.info} text-white px-6 py-3 rounded-lg shadow-lg flex items-center space-x-3 animate-slide-in-right`;

    // Add icon based on type
    const icons = {
        success: 'check-circle',
        error: 'alert-circle',
        warning: 'alert-triangle',
        info: 'info'
    };

    toast.innerHTML = `
        <i data-lucide="${icons[type] || icons.info}" class="w-5 h-5"></i>
        <span>${message}</span>
    `;

    toastContainer.appendChild(toast);

    // Recreate Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }

    // Auto-remove after delay
    const delay = type === 'error' ? 5000 : 3000;
    setTimeout(() => {
        toast.classList.add('animate-fade-out');
        setTimeout(() => {
            toast.remove();
            // Remove container if empty
            if (toastContainer.children.length === 0) {
                toastContainer.remove();
            }
        }, 300);
    }, delay);
}

/**
 * Debounce function to limit rate of function calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
