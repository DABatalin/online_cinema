// IDs фильмов, которые нужно запросить
const movieIds = [
    27205, 155, 19995, 24428, 293660, 157336, 68718, 118340, 550, 70160, 76341, 49026, 
    603, 68721, 1726, 120, 135397, 680, 49051, 278, 122, 13, 140607, 597, 37724, 297761, 
    121, 272, 271110, 286217, 22, 209112, 671, 1771, 14160, 10138, 99861, 11, 106646, 
    150540, 1930, 10195, 101299, 16869, 20352, 11324, 281957, 49521, 10681, 18785
];

// URL API
const apiUrl = 'http://localhost:8000/films/batch/';
const recommendApiUrl = 'http://localhost:8000/films/recommend/';

// Хранение выбранных фильмов
const selectedMovies = new Set();

// Функция для получения фильмов
async function fetchMovies() {
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(movieIds),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Ошибка от сервера:', errorData);
            throw new Error(errorData.detail || 'Ошибка получения фильмов');
        }

        const films = await response.json();
        displayFilms(films);
    } catch (error) {
        console.error('Ошибка при загрузке фильмов:', error);
        alert('Не удалось загрузить список фильмов. Проверьте подключение.');
    }
}

// Функция для отображения списка фильмов
function displayFilms(films) {
    const filmList = document.getElementById('filmList');
    const submitButton = document.getElementById('submitSelection');
    filmList.innerHTML = ''; // Очищаем список, если он уже есть

    films.forEach(film => {
        const listItem = document.createElement('li');
        listItem.textContent = film.title; // Предполагаем, что в объекте фильма есть поле "title"
        listItem.dataset.id = film.id; // Сохраняем ID фильма
        listItem.classList.add('film-item');

        // Добавляем обработчик клика
        listItem.addEventListener('click', () => {
            const movieId = Number(listItem.dataset.id);

            if (selectedMovies.has(movieId)) {
                // Если фильм уже выбран, снимаем выбор
                selectedMovies.delete(movieId);
                listItem.classList.remove('selected');
            } else {
                // Если фильм не выбран, добавляем его
                if (selectedMovies.size < 10) {
                    selectedMovies.add(movieId);
                    listItem.classList.add('selected');
                } else {
                    alert('Вы можете выбрать не более 10 фильмов.');
                }
            }

            // Включаем/отключаем кнопку отправки в зависимости от выбора
            submitButton.disabled = selectedMovies.size === 0;
        });

        filmList.appendChild(listItem);
    });
}

// Функция для отправки выбранных фильмов
async function submitSelection() {
    const submitButton = document.getElementById('submitSelection');
    submitButton.disabled = true; // Блокируем кнопку на время выполнения

    try {
        const response = await fetch(recommendApiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                movie_ids: Array.from(selectedMovies), // Преобразуем Set в массив
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Ошибка от сервера рекомендаций:', errorData);
            throw new Error(errorData.detail || 'Ошибка получения рекомендаций');
        }

        const recommendedMovieIds = await response.json();
        console.log('Рекомендации:', recommendedMovieIds);
        localStorage.setItem('recommendedMovieIds', JSON.stringify(recommendedMovieIds));
        alert('Рекомендации успешно получены! Проверьте консоль для деталей.');
        window.location.href = 'index.html';
    } catch (error) {
        console.error('Ошибка при отправке выбранных фильмов:', error);
        alert('Не удалось получить рекомендации. Проверьте подключение.');
    } finally {
        submitButton.disabled = false; // Разблокируем кнопку
    }
}

// Запускаем загрузку фильмов при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    fetchMovies();

    // Привязываем обработчик к кнопке отправки
    const submitButton = document.getElementById('submitSelection');
    submitButton.addEventListener('click', submitSelection);
});
