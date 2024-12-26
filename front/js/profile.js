// Функция для получения данных пользователя
function fetchUserProfile() {
    fetch('http://localhost:8000/auth/me/', {
        method: 'GET',
        credentials: 'include', // Для работы с куками
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user profile. Please log in.');
            }
            return response.json();
        })
        .then(data => {
            console.log('User data:', data);

            // Отображение информации о пользователе на странице
            const profileSection = document.querySelector('main section');
            profileSection.innerHTML = `
                <h2>Мой профиль</h2>
                <p>Добро пожаловать, ${data.first_name} ${data.last_name}!</p>
                <p>Email: ${data.email}</p>
                <p>Телефон: ${data.phone_number || 'Не указан'}</p>
            `;
        })
        .catch(error => {
            console.error('Error fetching user profile:', error);
            alert('Error fetching profile. Redirecting to login page.');
            window.location.href = 'index.html'; // Перенаправление на страницу логина
        });
}

// Функция выхода
function logout() {
    fetch('http://localhost:8000/auth/logout/', {
        method: 'POST',
        credentials: 'include', // Для работы с куками
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to log out');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message);
            alert('You have been logged out successfully.');
            window.location.href = 'index.html';
        })
        .catch(error => {
            console.error('Logout error:', error);
            alert('An error occurred while logging out.');
        });
}

// Назначение обработчиков событий
document.getElementById('logoutBtn').addEventListener('click', logout);

// Загрузка профиля при открытии страницы
window.onload = fetchUserProfile;
