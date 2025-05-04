/**
 * Логика для вкладки "Настройка AI".
 * Управляет формой настроек бота, включая AI-модель, имя, роль, цель, язык, базы знаний,
 * задачи, ограничения и настройки групп.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Инициализация вкладки
    loadModels().then(() => loadSettings());

    // Обработчик отправки формы
    const form = document.getElementById('ai-settings-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const settings = {
            ai_model: formData.get('ai_model'),
            name: formData.get('name'),
            role: formData.get('role'),
            goal: formData.get('goal'),
            language: formData.get('language') || 'ru',
            tasks: formData.get('tasks') ? formData.get('tasks').split(',').map(t => t.trim()).filter(t => t) : [],
            restrictions: formData.get('restrictions') ? formData.get('restrictions').split(',').map(r => r.trim()).filter(r => r) : [],
            group_trigger_name: formData.get('group_trigger_name') || null,
            check_subscription: formData.get('check_subscription') === 'on',
            group_type: formData.get('group_type'),
            subscription_group: formData.get('subscription_group') || null,
            subscription_group_id: formData.get('subscription_group_id') || null,
            subscription_message: formData.get('subscription_message') || null,
            show_typing_message: formData.get('show_typing_message') === 'on',
            typing_message_text: formData.get('typing_message_text') || "Панда пишет...",
            knowledge_bases: formData.getAll('knowledge_bases')
        };

        try {
            const response = await fetch('/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
                body: JSON.stringify(settings)
            });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Настройки успешно сохранены!', 'success');
            } else {
                throw new Error(result.detail || 'Ошибка сохранения настроек');
            }
        } catch (error) {
            showNotification(`Ошибка: ${error.message}`, 'error');
        }
    });

    // Обработчик кнопки перезагрузки настроек
    const reloadButton = document.getElementById('reload-form');
    reloadButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/reload', { method: 'POST' });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Настройки перезагружены!', 'success');
                await loadSettings();
            } else {
                throw new Error(result.detail || 'Ошибка перезагрузки настроек');
            }
        } catch (error) {
            showNotification(`Ошибка: ${error.message}`, 'error');
        }
    });
});

/**
 * Загружает доступные AI-модели из API и заполняет выпадающий список.
 */
async function loadModels() {
    try {
        const response = await fetch('/models', { headers: { 'Accept-Charset': 'UTF-8' } });
        const data = await response.json();
        const select = document.getElementById('ai-model');
        select.innerHTML = '<option value="" disabled>Выберите модель</option>';
        data.models.forEach(model => {
            const option = document.createElement('option');
            option.value = model;
            option.textContent = model;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Ошибка загрузки моделей:', error);
        showNotification('Ошибка загрузки моделей', 'error');
    }
}

/**
 * Загружает текущие настройки бота из API и заполняет форму.
 */
async function loadSettings() {
    try {
        const response = await fetch('/settings', { headers: { 'Accept-Charset': 'UTF-8' } });
        const settings = await response.json();
        document.getElementById('ai-model').value = settings.ai_model || '';
        document.getElementById('name').value = settings.name || '';
        document.getElementById('role').value = settings.role || '';
        document.getElementById('goal').value = settings.goal || '';
        document.getElementById('language').value = settings.language || 'ru';
        document.getElementById('group_trigger_name').value = settings.group_trigger_name || '';
        document.getElementById('check_subscription').checked = settings.check_subscription || false;
        document.getElementById('group_type').value = settings.group_type || '';
        document.getElementById('subscription_group').value = settings.subscription_group || '';
        document.getElementById('subscription_group_id').value = settings.subscription_group_id || '';
        document.getElementById('subscription_message').value = settings.subscription_message || '';
        document.getElementById('show_typing_message').checked = settings.show_typing_message || false;
        document.getElementById('typing_message_text').value = settings.typing_message_text || "Панда пишет...";
        
        const knowledgeSelect = document.getElementById('knowledge_bases');
        const basesResponse = await fetch('/knowledge_base/bases');
        const basesData = await basesResponse.json();
        knowledgeSelect.innerHTML = '';
        basesData.bases.forEach(base => {
            const option = document.createElement('option');
            option.value = base;
            option.textContent = base;
            if (settings.knowledge_bases.includes(base)) {
                option.selected = true;
            }
            knowledgeSelect.appendChild(option);
        });

        loadTasks(settings.tasks || []);
        loadRestrictions(settings.restrictions || []);
        toggleGroupField();
    } catch (error) {
        console.error('Ошибка загрузки настроек:', error);
        showNotification('Ошибка загрузки настроек', 'error');
    }
}

/**
 * Переключает видимость полей для открытой/закрытой группы в зависимости от типа группы.
 */
function toggleGroupField() {
    const groupType = document.getElementById('group_type').value;
    const openField = document.getElementById('subscription-group-field');
    const closedField = document.getElementById('subscription-group-id-field');

    if (groupType === 'open') {
        openField.classList.remove('hidden');
        closedField.classList.add('hidden');
    } else if (groupType === 'closed') {
        openField.classList.add('hidden');
        closedField.classList.remove('hidden');
    } else {
        openField.classList.add('hidden');
        closedField.classList.add('hidden');
    }
}

/**
 * Загружает список задач в интерфейс и обновляет скрытое поле.
 * @param {string[]} tasks - Список задач.
 */
function loadTasks(tasks) {
    const list = document.getElementById('tasks-list');
    list.innerHTML = '';
    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.className = 'flex justify-between items-center p-2 border-b dark:border-gray-700';
        li.innerHTML = `${task} <button onclick="removeTask(${index})" class="text-red-500 hover:text-red-700">Удалить</button>`;
        list.appendChild(li);
    });
    document.getElementById('tasks').value = tasks.join(', ');
}

/**
 * Добавляет новую задачу в список.
 */
function addTask() {
    const input = document.getElementById('new-task');
    const task = input.value.trim();
    if (task) {
        const tasks = document.getElementById('tasks').value.split(',').map(t => t.trim()).filter(t => t);
        tasks.push(task);
        loadTasks(tasks);
        input.value = '';
    }
}

/**
 * Удаляет задачу по индексу.
 * @param {number} index - Индекс задачи.
 */
function removeTask(index) {
    const tasks = document.getElementById('tasks').value.split(',').map(t => t.trim()).filter(t => t);
    tasks.splice(index, 1);
    loadTasks(tasks);
}

/**
 * Загружает список ограничений в интерфейс и обновляет скрытое поле.
 * @param {string[]} restrictions - Список ограничений.
 */
function loadRestrictions(restrictions) {
    const list = document.getElementById('restrictions-list');
    list.innerHTML = '';
    restrictions.forEach((restriction, index) => {
        const li = document.createElement('li');
        li.className = 'flex justify-between items-center p-2 border-b dark:border-gray-700';
        li.innerHTML = `${restriction} <button onclick="removeRestriction(${index})" class="text-red-500 hover:text-red-700">Удалить</button>`;
        list.appendChild(li);
    });
    document.getElementById('restrictions').value = restrictions.join(', ');
}

/**
 * Добавляет новое ограничение в список.
 */
function addRestriction() {
    const input = document.getElementById('new-restriction');
    const restriction = input.value.trim();
    if (restriction) {
        const restrictions = document.getElementById('restrictions').value.split(',').map(r => r.trim()).filter(r => r);
        restrictions.push(restriction);
        loadRestrictions(restrictions);
        input.value = '';
    }
}

/**
 * Удаляет ограничение по индексу.
 * @param {number} index - Индекс ограничения.
 */
function removeRestriction(index) {
    const restrictions = document.getElementById('restrictions').value.split(',').map(r => r.trim()).filter(r => r);
    restrictions.splice(index, 1);
    loadRestrictions(restrictions);
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