CREATE TABLE films (
	id INTEGER primary key,
	title TEXT,
	film_link TEXT,
	average_rating FLOAT, 
	description TEXT,
	vote_count FLOAT
);

CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255)
);


CREATE TABLE film_genres (
    film_id INTEGER REFERENCES films(id),
    genre_ids INTEGER[]
);