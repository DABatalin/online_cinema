let isLogin = true;

// Переключение между режимами "Вход" и "Регистрация"
function toggleAuth() {
    isLogin = !isLogin;

    const authTitle = document.getElementById('authTitle');
    const authContainer = document.getElementById('authContainer');
    const errorDiv = document.getElementById('error');
    const toggleText = authContainer.querySelector('.toggle');
    const confirmPassword = document.getElementById('confirmPassword');
    const firstName = document.getElementById('firstName');
    const lastName = document.getElementById('lastName');
    const phone = document.getElementById('phone');

    authTitle.textContent = isLogin ? 'Login' : 'Register';
    errorDiv.style.display = 'none';
    authContainer.querySelector('button').textContent = isLogin ? 'Log In' : 'Register';
    toggleText.textContent = isLogin ? "Don't have an account? Register" : "Already have an account? Log In";
    confirmPassword.style.display = isLogin ? 'none' : 'block';
    firstName.style.display = isLogin ? 'none' : 'block';
    lastName.style.display = isLogin ? 'none' : 'block';
    phone.style.display = isLogin ? 'none' : 'block';
}

// Отправка данных формы
function submitAuth() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('error');

    if (!validateEmail(email)) {
        errorDiv.textContent = 'Invalid email format';
        errorDiv.style.display = 'block';
        return;
    }

    if (!isLogin) {
        const firstName = document.getElementById('firstName').value;
        const lastName = document.getElementById('lastName').value;
        const phone = document.getElementById('phone').value;

        if (!firstName || !lastName) {
            errorDiv.textContent = 'First name and last name are required';
            errorDiv.style.display = 'block';
            return;
        }

        if (!validatePhone(phone)) {
            errorDiv.textContent = 'Invalid phone number';
            errorDiv.style.display = 'block';
            return;
        }
    }

    const bodyData = isLogin
        ? { email, password }
        : { 
            email,  
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            phone_number: document.getElementById('phone').value,
            password
        };

    fetch(isLogin ? 'http://localhost:8000/auth/login/' : 'http://localhost:8000/auth/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bodyData),
        credentials: 'include'
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(data => {
            if (isLogin) {
                // Сохраняем токен и переходим на главную страницу
                localStorage.setItem('token', data.token);
                alert('Login successful!');
                errorDiv.style.display = 'none';
                window.location.href = 'main.html';
            } else {
                // В случае регистрации перенаправляем на страницу выбора фильмов
                sessionStorage.setItem('pendingRegistration', JSON.stringify(bodyData));
                window.location.href = 'choose-films.html';
            }
        })
        .catch(error => {
            errorDiv.textContent = error.message;
            errorDiv.style.display = 'block';
        });
}

// Завершение регистрации после выбора фильмов
function completeRegistration(selectedMovies) {
    const pendingRegistration = JSON.parse(sessionStorage.getItem('pendingRegistration'));

    if (!pendingRegistration) {
        alert('No pending registration data found!');
        return;
    }

    // Добавляем выбор фильмов к данным регистрации
    pendingRegistration.favorite_movies = selectedMovies;

    fetch('http://localhost:8000/auth/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(pendingRegistration),
        credentials: 'include'
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.detail || 'Unknown error');
                });
            }
            return response.json();
        })
        .then(() => {
            alert('Registration successful! Please log in.');
            sessionStorage.removeItem('pendingRegistration');
            window.location.href = 'index.html'; // Переход на страницу логина
        })
        .catch(error => {
            console.error('Registration completion error:', error.message);
            alert('Failed to complete registration. Please try again.');
        });
}

// Валидация email
function validateEmail(email) {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailPattern.test(email);
}

// Валидация телефона
function validatePhone(phone) {
    const phonePattern = /^\+\d{5,15}$/;
    return phonePattern.test(phone);
}

function checkAccess() {
    fetch('http://localhost:8000/auth/me/', {
        credentials: 'include' // Важно для работы с куками
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Access denied');
            }
            return response.json();
        })
        .then(data => {
            console.log('Access granted:', data);
            window.location.href = 'main.html'; // Перенаправление на главную страницу
        })
        .catch(error => {
            console.error('Access error:', error);
            alert('You need to log in to access this page.');
            window.location.href = 'index.html'; // Перенаправление на страницу логина
        });
}


// Проверка авторизации при загрузке страницы
window.onload = () => {
    if (window.location.pathname === '/main.html') {
        checkAccess();
    }
};

