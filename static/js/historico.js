// Histórico JavaScript
// Handles automatic form submission when filters change

document.addEventListener('DOMContentLoaded', () => {
    const mesSelect = document.getElementById('mes');
    const anoSelect = document.getElementById('ano');
    const filtroForm = document.getElementById('filtro-form');

    // Auto-submit on month change
    if (mesSelect) {
        mesSelect.addEventListener('change', () => {
            filtroForm.submit();
        });
    }

    // Auto-submit on year change
    if (anoSelect) {
        anoSelect.addEventListener('change', () => {
            filtroForm.submit();
        });
    }

    // Initialize Lucide icons
    if (window.lucide) {
        lucide.createIcons();
    }
});
