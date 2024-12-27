document.addEventListener("DOMContentLoaded", async () => {
    const movieTitle = document.getElementById("movieTitle");
    const movieGenre = document.getElementById("movieGenre");
    const movieDescription = document.getElementById("movieDescription");
    const movieRating = document.getElementById("movieRating");
    const movieVideoSource = document.getElementById("movieVideoSource");

    // Извлечение ID фильма из URL
    const urlParams = new URLSearchParams(window.location.search);
    const movieID = urlParams.get("id");

    if (movieID) {
        const movies = await fetchMovies(movieID); // Получаем список фильмов
        const movie = movies.find(m => m._source.movieID === parseInt(movieID)); // Находим нужный фильм

        if (movie) {
            const movieData = movie._source; // Данные фильма из _source
            movieTitle.textContent = movieData.title;
            movieGenre.textContent = movieData.genres.join(", ");
            movieDescription.textContent = movieData.description;
            movieRating.textContent = movieData.average_rating;
            movieVideoSource.src = movieData.film_link || "video.mp4"; // Используем ссылку или заглушку
        } else {
            movieTitle.textContent = "Фильм не найден.";
        }
    } else {
        movieTitle.textContent = "ID фильма не указан.";
    }

    // Функция для получения фильмов (из API /search/)
    async function fetchMovies(query) {
        try {
            const response = await fetch(`/films/search/?query=${query}`);
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error("Error fetching movie details:", error);
            return [];
        }
    }
});
