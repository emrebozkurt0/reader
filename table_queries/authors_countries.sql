DROP TABLE IF EXISTS Countries;
DROP TABLE IF EXISTS Authors;

CREATE TABLE Countries (
	country_id INT AUTO_INCREMENT,
    country_name VARCHAR(20),
    country_region VARCHAR(20),
    
    PRIMARY KEY(country_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Authors (
	author_id INT AUTO_INCREMENT,
    author_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    about TEXT,
    img_url VARCHAR(250),
    country_id INT,
    
    PRIMARY KEY (author_id),
    
    FOREIGN KEY (country_id)
		REFERENCES Countries(country_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
