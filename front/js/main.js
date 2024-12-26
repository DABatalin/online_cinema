document.addEventListener("DOMContentLoaded", () => {
    // Пример фильмов
    const allMovies = getMovies();

    // Контейнеры для отображения фильмов
    const recommendedMoviesContainer = document.getElementById("recommendedMovies");
    const genresMoviesContainer = document.getElementById("genresMovies");

    // Отображение фильмов
    renderMovies(allMovies);

    // Функция для рендеринга фильмов
    function renderMovies(movies) {
        displayRecommendedMovies(movies);
        displayGenreMovies(movies);
    }

    // Отображение рекомендованных фильмов
    function displayRecommendedMovies(movies) {
        recommendedMoviesContainer.innerHTML = ""; // Очистка контейнера
        const recommended = movies.slice(0, 10); // Берём первые 10 фильмов как рекомендованные

        recommended.forEach(movie => {
            const movieElement = createMovieElement(movie);
            recommendedMoviesContainer.appendChild(movieElement);
        });
    }

    // Отображение фильмов по жанрам
    function displayGenreMovies(movies) {
        genresMoviesContainer.innerHTML = ""; // Очистка контейнера

        const genres = groupMoviesByGenre(movies);

        Object.keys(genres).forEach(genre => {
            const genreSection = document.createElement("div");
            genreSection.classList.add("genre-section");

            const genreTitle = document.createElement("h3");
            genreTitle.textContent = genre;
            genreSection.appendChild(genreTitle);

            genres[genre].slice(0, 5).forEach(movie => { // Ограничиваем по 5 фильмов на жанр
                const movieElement = createMovieElement(movie);
                genreSection.appendChild(movieElement);
            });

            genresMoviesContainer.appendChild(genreSection);
        });
    }

    // Функция для фильтрации фильмов по поисковому запросу
    window.searchMovies = function() {
        const searchQuery = document.getElementById('searchInput').value.toLowerCase();
        const filteredMovies = allMovies.filter(movie => movie.title.toLowerCase().includes(searchQuery));
        
        // Перерисовываем фильмы на странице
        renderMovies(filteredMovies);
    }

    // Создание элемента фильма
    function createMovieElement(movie) {
        const movieDiv = document.createElement("div");
        movieDiv.classList.add("movie");
        movieDiv.dataset.id = movie.id;

        // Создаем ссылку на страницу фильма
        const movieLink = document.createElement("a");
        movieLink.href = `film.html?id=${movie.id}`; // Переход на страницу фильма по ID
        movieLink.textContent = movie.title;

        movieDiv.appendChild(movieLink);
        return movieDiv;
    }

    // Группировка фильмов по жанру
    function groupMoviesByGenre(movies) {
        return movies.reduce((acc, movie) => {
            const genre = movie.genre || "Другие";
            if (!acc[genre]) {
                acc[genre] = [];
            }
            acc[genre].push(movie);
            return acc;
        }, {});
    }

    // Функция для получения тестовых данных (фильмов)
    function getMovies() {
        return [
            { 
                "id": 1, 
                "title": "Inception", 
                "genre": "Sci-Fi", 
                "description": "A mind-bending thriller about a thief who enters the dreams of others.", 
                "rating": "8.8/10", 
                "video_url": "path_to_inception_video.mp4" 
            },
            { 
                "id": 2, 
                "title": "The Godfather", 
                "genre": "Crime", 
                "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", 
                "rating": "9.2/10", 
                "video_url": "path_to_godfather_video.mp4" 
            },
            { 
                "id": 3, 
                "title": "The Dark Knight", 
                "genre": "Action", 
                "description": "Batman faces off against the Joker, a criminal mastermind who seeks to create chaos in Gotham City.", 
                "rating": "9.0/10", 
                "video_url": "path_to_dark_knight_video.mp4" 
            }
        ];
    }
});
