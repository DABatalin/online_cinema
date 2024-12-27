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
        try {
            // Получаем данные о фильме через batch API
            const movies = await fetchMovieDetails(movieID);

            if (movies && movies.length > 0) {
                const movie = movies[0]; // Предполагается, что batch возвращает массив с одним элементом

                // Отображение информации о фильме
                movieTitle.textContent = movie.title || "Название отсутствует";
                movieGenre.textContent = movie.genres ? movie.genres.join(", ") : "Жанр отсутствует";
                movieDescription.textContent = movie.description || "Описание отсутствует";
                movieRating.textContent = movie.average_rating || "Рейтинг отсутствует";
                movieVideoSource.src = movie.film_link || "video.mp4"; // Используем ссылку на фильм или заглушку
            } else {
                movieTitle.textContent = "Фильм не найден.";
            }
        } catch (error) {
            console.error("Ошибка при загрузке информации о фильме:", error);
            movieTitle.textContent = "Ошибка загрузки данных фильма.";
        }
    } else {
        movieTitle.textContent = "ID фильма не указан.";
    }

    // Функция для получения информации о фильме через batch API
    async function fetchMovieDetails(movieID) {
        try {
            const response = await fetch('/films/batch/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify([parseInt(movieID)]), // Передаём ID фильма как массив
            });

            if (!response.ok) {
                const errorText = await response.text();
                console.error("Ошибка запроса:", errorText);
                throw new Error(`Ошибка сервера: ${response.status}`);
            }

            return await response.json(); // Возвращаем массив фильмов
        } catch (error) {
            console.error("Ошибка при запросе batch API:", error);
            return [];
        }
    }
});
