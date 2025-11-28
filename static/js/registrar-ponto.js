// Registrar Ponto JavaScript
// Handles time calculations and "bater ponto" functionality

// Bater ponto - fills current time
function baterPonto(inputId) {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const timeString = `${hours}:${minutes}`;

    document.getElementById(inputId).value = timeString;
    updateAllHours();
}

// Calculate hours between entrada and saida
function calculateHours(entrada, saida) {
    if (!entrada || !saida) return 0;

    const [h1, m1] = entrada.split(':').map(Number);
    const [h2, m2] = saida.split(':').map(Number);

    const minutes1 = h1 * 60 + m1;
    const minutes2 = h2 * 60 + m2;

    const diff = minutes2 - minutes1;
    return diff / 60;
}

// Update display of hours for a period
function updatePeriodHours(period) {
    const entrada = document.getElementById(`entrada${period}`).value;
    const saida = document.getElementById(`saida${period}`).value;
    const hours = calculateHours(entrada, saida);

    const displayElement = document.getElementById(`horas-periodo${period}`);
    if (displayElement) {
        displayElement.textContent = hours > 0 ? `${hours.toFixed(2)}h` : '-';
    }
}

// Update total hours
function updateTotalHours() {
    let total = 0;
    for (let i = 1; i <= 3; i++) {
        const entrada = document.getElementById(`entrada${i}`).value;
        const saida = document.getElementById(`saida${i}`).value;
        total += calculateHours(entrada, saida);
    }

    const totalElement = document.getElementById('horas-total');
    if (totalElement) {
        totalElement.textContent = `${total.toFixed(2)}h`;
    }
}

// Update all hours displays
function updateAllHours() {
    updatePeriodHours(1);
    updatePeriodHours(2);
    updatePeriodHours(3);
    updateTotalHours();
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Add change listeners to all time inputs
    for (let i = 1; i <= 3; i++) {
        ['entrada', 'saida'].forEach(type => {
            const input = document.getElementById(`${type}${i}`);
            if (input) {
                input.addEventListener('change', updateAllHours);
                input.addEventListener('blur', updateAllHours);
            }
        });
    }

    // Calculate on page load if there are existing values
    updateAllHours();

    // Recreate Lucide icons after any dynamic changes
    if (window.lucide) {
        lucide.createIcons();
    }
});
