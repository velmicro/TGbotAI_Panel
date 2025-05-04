async function loadKnowledgeBases() {
    try {
        const response = await fetch('/knowledge_base/bases', { headers: { 'Accept-Charset': 'UTF-8' } });
        const data = await response.json();
        const select = document.getElementById('knowledge-base-select');
        select.innerHTML = '';
        data.bases.forEach(base => {
            const option = document.createElement('option');
            option.value = base;
            option.textContent = base;
            select.appendChild(option);
        });
        if (data.bases.length > 0) {
            select.value = data.bases[0];
            loadKnowledgeBase(data.bases[0]);
        }
    } catch (error) {
        console.error('Ошибка загрузки баз знаний:', error);
        showNotification('Ошибка загрузки баз знаний', 'error');
    }
}

async function loadKnowledgeBase(baseName) {
    try {
        const response = await fetch(`/knowledge_base/${baseName}`, { headers: { 'Accept-Charset': 'UTF-8' } });
        const data = await response.json();
        const tableBody = document.getElementById('knowledge-base-table-body');
        tableBody.innerHTML = '';
        data.entries.forEach(entry => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${entry.question}</td>
                <td>${entry.keywords}</td>
                <td>${entry.answer}</td>
                <td>
                    <button onclick="editKnowledgeEntry(${entry.id}, '${baseName}')" class="text-blue-500 hover:text-blue-700 mr-2">Редактировать</button>
                    <button onclick="deleteKnowledgeEntry(${entry.id}, '${baseName}')" class="text-red-500 hover:text-red-700">Удалить</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Ошибка загрузки базы знаний:', error);
        showNotification('Ошибка загрузки базы знаний', 'error');
    }
}

async function createKnowledgeBase() {
    const baseName = document.getElementById('new-base-name').value.trim();
    if (!baseName) {
        showNotification('Введите название базы знаний', 'error');
        return;
    }
    try {
        const response = await fetch('/knowledge_base/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
            body: JSON.stringify(baseName)
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('База знаний создана', 'success');
            document.getElementById('new-base-name').value = '';
            loadKnowledgeBases();
        } else {
            throw new Error(result.detail || 'Ошибка создания базы знаний');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}

async function deleteKnowledgeBase() {
    const baseName = document.getElementById('knowledge-base-select').value;
    if (!baseName) return;
    if (!confirm(`Вы уверены, что хотите удалить базу знаний "${baseName}"?`)) return;
    try {
        const response = await fetch(`/knowledge_base/${baseName}`, {
            method: 'DELETE',
            headers: { 'Accept-Charset': 'UTF-8' }
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('База знаний удалена', 'success');
            loadKnowledgeBases();
        } else {
            throw new Error(result.detail || 'Ошибка удаления базы знаний');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}

async function syncKnowledgeBase() {
    const baseName = document.getElementById('knowledge-base-select').value;
    if (!baseName) return;
    try {
        const response = await fetch(`/knowledge_base/${baseName}/sync`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' }
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('База знаний синхронизирована', 'success');
            loadKnowledgeBase(baseName);
        } else {
            throw new Error(result.detail || 'Ошибка синхронизации');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}

async function addKnowledgeEntry() {
    const baseName = document.getElementById('knowledge-base-select').value;
    const question = document.getElementById('new-knowledge-question').value.trim();
    const keywords = document.getElementById('new-knowledge-keywords').value.trim();
    const answer = document.getElementById('new-knowledge-answer').value.trim();
    if (!question || !keywords || !answer) {
        showNotification('Заполните все поля', 'error');
        return;
    }
    try {
        const response = await fetch(`/knowledge_base/${baseName}/add`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
            body: JSON.stringify({ question, keywords, answer })
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('Запись добавлена', 'success');
            document.getElementById('new-knowledge-question').value = '';
            document.getElementById('new-knowledge-keywords').value = '';
            document.getElementById('new-knowledge-answer').value = '';
            loadKnowledgeBase(baseName);
        } else {
            throw new Error(result.detail || 'Ошибка добавления записи');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}

async function editKnowledgeEntry(id, baseName) {
    const response = await fetch(`/knowledge_base/${baseName}`, { headers: { 'Accept-Charset': 'UTF-8' } });
    const data = await response.json();
    const entry = data.entries.find(e => e.id === id);
    if (!entry) return;

    document.getElementById('new-knowledge-question').value = entry.question;
    document.getElementById('new-knowledge-keywords').value = entry.keywords;
    document.getElementById('new-knowledge-answer').value = entry.answer;

    const form = document.getElementById('knowledge-entry-form');
    form.onsubmit = async (event) => {
        event.preventDefault();
        const question = document.getElementById('new-knowledge-question').value.trim();
        const keywords = document.getElementById('new-knowledge-keywords').value.trim();
        const answer = document.getElementById('new-knowledge-answer').value.trim();
        try {
            const response = await fetch(`/knowledge_base/${baseName}/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8' },
                body: JSON.stringify({ question, keywords, answer })
            });
            const result = await response.json();
            if (result.status === 'success') {
                showNotification('Запись обновлена', 'success');
                document.getElementById('new-knowledge-question').value = '';
                document.getElementById('new-knowledge-keywords').value = '';
                document.getElementById('new-knowledge-answer').value = '';
                form.onsubmit = addKnowledgeEntry;
                loadKnowledgeBase(baseName);
            } else {
                throw new Error(result.detail || 'Ошибка обновления записи');
            }
        } catch (error) {
            showNotification(`Ошибка: ${error.message}`, 'error');
        }
    };
}

async function deleteKnowledgeEntry(id, baseName) {
    if (!confirm('Вы уверены, что хотите удалить эту запись?')) return;
    try {
        const response = await fetch(`/knowledge_base/${baseName}/${id}`, {
            method: 'DELETE',
            headers: { 'Accept-Charset': 'UTF-8' }
        });
        const result = await response.json();
        if (result.status === 'success') {
            showNotification('Запись удалена', 'success');
            loadKnowledgeBase(baseName);
        } else {
            throw new Error(result.detail || 'Ошибка удаления записи');
        }
    } catch (error) {
        showNotification(`Ошибка: ${error.message}`, 'error');
    }
}