document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const filmId = urlParams.get('id');

    if (filmId) {
        loadFilmDetails(filmId);
    }

    function loadFilmDetails(filmId) {
        const movies = getMovies();
        const film = movies.find(movie => movie.id === parseInt(filmId));

        if (film) {
            document.getElementById("movieTitle").textContent = film.title;
            document.getElementById("movieGenre").textContent = film.genre;
            document.getElementById("movieDescription").textContent = film.description;
            document.getElementById("movieRating").textContent = film.rating;
            document.getElementById("movieVideoSource").src = film.video_url;
        } else {
            alert("Фильм не найден!");
        }
    }

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
