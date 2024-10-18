const BASE_URL = 'https://starfish-app-cx6jf.ondigitalocean.app';

// Função de Login - Envia os dados do formulário de login via AJAX e armazena o token de autenticação no localStorage se bem-sucedido
$('#login-form').on('submit', function(e) {
	e.preventDefault();
	const username = $('#username').val();
	const password = $('#password').val();

	$.ajax({
		url: `${BASE_URL}/login`,
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify({ name: username, password }),
		success: function(response) {
			localStorage.setItem('auth_token', response.auth_token);
			window.location.href = 'todo.html';
		},
		error: function(xhr) {
			const errorData = xhr.responseJSON;
			$('#login-error').text(errorData?.detail || 'Login failed.');
			console.error('Error:', errorData);
		}
	});
});

// Função de Cadastro - Envia dados para a criação de um novo usuário e armazena o token de autenticação no localStorage se bem-sucedido
$('#sign-up-button').on('click', function() {
	const username = $('#username').val();
	const password = $('#password').val();

	$.ajax({
		url: `${BASE_URL}/sign-up`,
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify({ name: username, password }),
		success: function(response) {
			localStorage.setItem('auth_token', response.auth_token);
			window.location.href = 'todo.html';
		},
		error: function(xhr) {
			const errorData = xhr.responseJSON;
			$('#login-error').text(errorData?.detail || 'Sign-up failed.');
			console.error('Error:', errorData);
		}
	});
});

// Função para Buscar e Exibir Tarefas - Faz uma requisição GET para buscar as tarefas do usuário autenticado e exibe na página
function fetchTasks() {
	$.ajax({
		url: `${BASE_URL}/todo-list`,
		type: 'GET',
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
		},
		success: function(tasks) {
			const todoList = $('#todo-list');
			todoList.empty();  // Clear current list

			tasks.forEach(task => {
				const taskItem = $('<div>').addClass('task-item').css('padding', '10px');

				// Task description with status inline
				const taskDescription = $('<span>').text(`${task.task} - `);
				const taskStatus = $('<span>')
					.text(`${task.status}`)
					.css('color', task.status === 'Pendente' ? 'yellow' : 'green');

				// Toggle status button
				const toggleStatusButton = $('<button>')
					.text('Trocar status')
					.addClass('toggle-status-btn')
					.css({ 'margin-top': '10px', 'margin-right': '5px' })
					.on('click', function() {
						toggleTaskStatus(task.id);
					});

				// Delete button
				const deleteButton = $('<button>')
					.text('Deletar')
					.addClass('delete-btn')
					.css({ 'margin-top': '10px' })
					.on('click', function() {
						deleteTask(task.id);
					});

				// Append description and status to task item
				taskItem.append(taskDescription, taskStatus);

				// Append buttons to the task item below the description and status
				taskItem.append('<br>', toggleStatusButton, deleteButton);

				// Add a separator line
				const separator = $('<hr>').addClass('task-separator');

				// Append task item and separator to the list
				todoList.append(taskItem, separator);
			});
		},
		error: function() {
			window.location.href = 'index.html';
		}
	});
}

// Função para Alternar o Status da Tarefa - Altera o status de uma tarefa específica (Pendente/Completa) enviando uma requisição PUT
function toggleTaskStatus(taskId) {
	$.ajax({
		url: `${BASE_URL}/todo-list/status/${taskId}`,
		type: 'PUT',
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
		},
		success: function() {
			fetchTasks();  // Refresh the task list
		},
		error: function(xhr) {
			console.error('Failed to toggle task status', xhr);
		}
	});
}

// Função para Deletar Tarefa - Remove uma tarefa específica enviando uma requisição DELETE
function deleteTask(taskId) {
	$.ajax({
		url: `${BASE_URL}/todo-list/${taskId}`,
		type: 'DELETE',
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
		},
		success: function() {
			fetchTasks();  // Refresh the task list
		},
		error: function(xhr) {
			console.error('Failed to delete task', xhr);
		}
	});
}

// Função para Adicionar Nova Tarefa - Envia uma requisição POST para o backend e atualiza a lista de tarefas com a função
// fetchTasks().
$('#add-task-form').on('submit', function(e) {
	e.preventDefault();
	const newTask = $('#new-task').val();

	$.ajax({
		url: `${BASE_URL}/todo-list`,
		type: 'POST',
		contentType: 'application/json',
		data: JSON.stringify({ task: newTask }),
		headers: {
			'Authorization': 'Bearer ' + localStorage.getItem('auth_token')
		},
		success: function() {
			fetchTasks();  // Refresh the task list
			$('#new-task').val('');  // Clear the input
		},
		error: function(xhr) {
			console.error('Failed to add task', xhr);
		}
	});
});

// Remove o token de autorização do local storage e redireciona o usuário para a tela de login.
function logout() {
	localStorage.removeItem('auth_token');
	window.location.href = 'index.html';
}

// Atualiza a lista de tarefas quando entra na página 
if (window.location.pathname.endsWith('todo.html')) {
	fetchTasks();
}
