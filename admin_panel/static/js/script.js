/**
 * Основной скрипт для админ-панели.
 * Управляет общей инициализацией, переключением секций, темой, логами и управлением ботом.
 * Логика для отдельных вкладок (AI Settings, Knowledge Base, Dialogs) вынесена в отдельные файлы.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Инициализация
    initializeSidebar();
    initializeTheme();
    initializeLogs();
    initializeBotControls();
    showSection('dashboard'); // Показываем панель управления по умолчанию
});

/**
 * Инициализирует боковую панель (сворачивание/разворачивание).
 */
function initializeSidebar() {
    const toggleButton = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const sidebarTitle = document.getElementById('sidebar-title');
    const sidebarTexts = document.getElementsByClassName('sidebar-text');

    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('w-64');
        sidebar.classList.toggle('w-16');
        sidebarTitle.classList.toggle('hidden');
        for (let text of sidebarTexts) {
            text.classList.toggle('hidden');
        }
    });
}

/**
 * Инициализирует переключение темы (светлая/тёмная).
 */
function initializeTheme() {
    const toggleThemeButton = document.getElementById('toggle-theme');
    const isDarkMode = localStorage.getItem('dark-mode') === 'true';
    if (isDarkMode) {
        document.documentElement.classList.add('dark');
        toggleThemeButton.querySelector('span').textContent = 'light_mode';
    }

    toggleThemeButton.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark');
        const isDark = document.documentElement.classList.contains('dark');
        localStorage.setItem('dark-mode', isDark);
        toggleThemeButton.querySelector('span').textContent = isDark ? 'light_mode' : 'dark_mode';
    });
}

/**
 * Инициализирует управление логами (загрузка, автообновление, очистка).
 */
function initializeLogs() {
    const refreshButton = document.getElementById('refresh-logs');
    const clearButton = document.getElementById('clear-logs');
    const autoRefreshSelect = document.getElementById('auto-refresh');
    let autoRefreshInterval = null;

    async function loadLogs() {
        try {
            const response = await fetch('/logs');
            const logs = await response.text();
            document.getElementById('log-content').textContent = logs;
        } catch (error) {
            showNotification('Ошибка загрузки логов', 'error');
        }
    }

    refreshButton.addEventListener('click', loadLogs);

    clearButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/logs/clear', { method: 'POST' });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Логи очищены', 'success');
                loadLogs();
            } else {
                showNotification('Ошибка очистки логов', 'error');
            }
        } catch (error) {
            showNotification('Ошибка очистки логов', 'error');
        }
    });

    autoRefreshSelect.addEventListener('change', () => {
        if (autoRefreshInterval) {
            clearInterval(autoRefreshInterval);
            autoRefreshInterval = null;
        }
        const interval = parseInt(autoRefreshSelect.value) * 1000;
        if (interval > 0) {
            autoRefreshInterval = setInterval(loadLogs, interval);
        }
    });

    loadLogs(); // Загружаем логи при инициализации
}

/**
 * Инициализирует кнопки управления ботом (запуск, перезагрузка, остановка).
 */
function initializeBotControls() {
    const startButton = document.getElementById('start-bot');
    const restartButton = document.getElementById('restart-bot');
    const stopButton = document.getElementById('stop-bot');

    startButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/start', { method: 'POST' });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Бот запущен', 'success');
            } else {
                showNotification('Ошибка запуска бота', 'error');
            }
        } catch (error) {
            showNotification('Ошибка запуска бота', 'error');
        }
    });

    restartButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/reload', { method: 'POST' });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Бот перезагружен', 'success');
            } else {
                showNotification('Ошибка перезагрузки бота', 'error');
            }
        } catch (error) {
            showNotification('Ошибка перезагрузки бота', 'error');
        }
    });

    stopButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/stop', { method: 'POST' });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Бот остановлен', 'success');
            } else {
                showNotification('Ошибка остановки бота', 'error');
            }
        } catch (error) {
            showNotification('Ошибка остановки бота', 'error');
        }
    });
}

/**
 * Показывает указанную секцию и скрывает остальные.
 * @param {string} sectionId - ID секции для показа.
 */
function showSection(sectionId) {
    const sections = document.getElementsByClassName('section');
    for (let section of sections) {
        section.classList.add('hidden');
    }
    document.getElementById(sectionId).classList.remove('hidden');
}

/**
 * Показывает уведомление об успехе или ошибке.
 * @param {string} message - Сообщение уведомления.
 * @param {string} type - Тип уведомления ('success' или 'error').
 */
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${type === 'success' ? 'bg-green-500' : 'bg-red-500'} text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 3000);
}