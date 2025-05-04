async function loadDialogs() {
    try {
        const response = await fetch('/dialogs', { headers: { 'Accept-Charset': 'UTF-8' } });
        const data = await response.json();
        const tableBody = document.getElementById('dialogs-table-body');
        tableBody.innerHTML = '';
        data.dialogs.forEach(dialog => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${dialog.question}</td>
                <td>${dialog.answer}</td>
                <td>
                    <button onclick="editDialog(${dialog.id})" class="text-blue-500 hover:text-blue-700 mr-2">Редактировать</button>
                    <button onclick="deleteDialog(${dialog.id})" class="text-red-500 hover:text-red-700">Удалить</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Ошибка загрузки диалогов:', error);
        showNotification('Ошибка загрузки диалогов', 'error');
    }
}

async function addDialog() {
    const question = document.getElementById('new-dialog-question').value.trim();
    const answer = document.getElementById('new-dialog-answer').value.trim();
    if (!question || !answer) {
        showNotification('Заполните все поля', 'error');
        return;
    }
    try {
        const response = await fetch('/dialogs/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
            body: JSON.stringify({ question, answer })
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('Диалог добавлен', 'success');
            document.getElementById('new-dialog-question').value = '';
            document.getElementById('new-dialog-answer').value = '';
            loadDialogs();
        } else {
            throw new Error(result.detail || 'Ошибка добавления диалога');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}

async function editDialog(id) {
    const response = await fetch('/dialogs', { headers: { 'Accept-Charset': 'UTF-8' } });
    const data = await response.json();
    const dialog = data.dialogs.find(d => d.id === id);
    if (!dialog) return;

    document.getElementById('new-dialog-question').value = dialog.question;
    document.getElementById('new-dialog-answer').value = dialog.answer;

    const form = document.getElementById('dialog-entry-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        const question = document.getElementById('new-dialog-question').value.trim();
        const answer = document.getElementById('new-dialog-answer').value.trim();
        try {
            const response = await fetch(`/dialogs/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
                body: JSON.stringify({ question, answer })
            });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Диалог обновлён', 'success');
                document.getElementById('new-dialog-question').value = '';
                document.getElementById('new-dialog-answer').value = '';
                form.onsubmit = addDialog;
                loadDialogs();
            } else {
                throw new Error(result.detail || 'Ошибка обновления диалога');
            }
        } catch (error) {
            showNotification(`Ошибка: ${error.message}`, 'error');
        }
    };
}

async function deleteDialog(id) {
    if (!confirm('Вы уверены, что хотите удалить этот диалог?')) return;
    try {
        const response = await fetch(`/dialogs/${id}`, {
            method: 'DELETE',
            headers: { 'Accept-Charset': 'UTF-8' }
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('Диалог удалён', 'success');
            loadDialogs();
        } else {
            throw new Error(result.detail || 'Ошибка удаления диалога');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}