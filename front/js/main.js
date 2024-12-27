document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("searchInput");
    const suggestionsContainer = document.getElementById("suggestions");

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

    // Функция задержки вызова
    function debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func(...args), delay);
        };
    }
});
