document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const suggestionsContainer = document.getElementById("suggestions");
    const recommendedContainer = document.getElementById("recommendedMovies"); // Контейнер для рекомендованных фильмов

    // Показ рекомендованных фильмов
    displayRecommendedMovies();

    // Обработчик ввода текста с использованием debounce
    searchInput.addEventListener("input", debounce(async () => {
        const query = searchInput.value.trim();
        if (query.length > 0) {
            const suggestions = await fetchMovies(query);
            displaySuggestions(suggestions);
        } else {
            suggestionsContainer.innerHTML = ""; // Очищаем подсказки, если запрос пустой
            suggestionsContainer.style.display = 'none'; // Скрываем подсказки
        }
    }, 300));

    // Функция для получения фильмов с сервера
    async function fetchMovies(query) {
        try {
            const response = await fetch(`/films/search/?query=${query}`);
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching movies:", error);
            return [];
        }
    }

    // Отображение подсказок
    function displaySuggestions(movies) {
        suggestionsContainer.innerHTML = ""; // Очищаем старые подсказки
        if (movies.length > 0) {
            suggestionsContainer.style.display = 'block'; // Показываем контейнер подсказок
            movies.forEach(movie => {
                const suggestionItem = document.createElement("li");

                // Добавляем текст фильма в элемент списка
                suggestionItem.textContent = movie._source.title;

                // Добавляем обработчик клика на каждый фильм
                suggestionItem.addEventListener("click", () => {
                    window.location.href = `film.html?id=${movie._source.movieID}`; // Переход на страницу фильма
                });

                // Добавляем элемент списка в контейнер подсказок
                suggestionsContainer.appendChild(suggestionItem);
            });
        } else {
            suggestionsContainer.style.display = 'none'; // Если нет фильмов, скрываем подсказки
        }
    }

    // Показ рекомендованных фильмов
    async function displayRecommendedMovies() {
        const recommendedData = JSON.parse(localStorage.getItem('recommendedMovieIds') || '{}');
    
        // Проверяем, что данные являются объектом с ключом `recommended_movies`
        if (!recommendedData || !Array.isArray(recommendedData.recommended_movies)) {
            console.error("Invalid data for batch request:", recommendedData);
            recommendedContainer.innerHTML = "<p>Нет рекомендованных фильмов</p>";
            return;
        }
    
        // Извлекаем массив ID фильмов
        const recommendedMovieIds = recommendedData.recommended_movies;
        console.log('Рекомендованные ID фильмов:', recommendedMovieIds);
    
        try {
            const response = await fetch('/films/batch/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(recommendedMovieIds), // Передаём только массив ID
            });
    
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Ошибка запроса:', errorText);
                throw new Error(`Ошибка сервера: ${response.status}`);
            }
    
            const movies = await response.json();
            console.log('Рекомендованные фильмы:', movies);
    
            recommendedContainer.innerHTML = ""; // Очищаем контейнер
            movies.forEach(movie => {
                const movieItem = document.createElement("div");
                movieItem.classList.add("recommended-movie");
    
                const movieTitle = document.createElement("h3");
                movieTitle.textContent = movie.title;
    
                movieItem.addEventListener("click", () => {
                    window.location.href = `film.html?id=${movie.id}`;
                });
    
                movieItem.appendChild(movieTitle);
                recommendedContainer.appendChild(movieItem);
            });
        } catch (error) {
            console.error("Ошибка при загрузке рекомендованных фильмов:", error);
            recommendedContainer.innerHTML = "<p>Ошибка загрузки рекомендованных фильмов</p>";
        }
    }

    // Функция задержки вызова
    function debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }
});
