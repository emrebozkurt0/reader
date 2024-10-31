CREATE TABLE Authors (
	author_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    gender VARCHAR(10),
    about TEXT,
    img_url VARCHAR(250),
    country_id INT,
    
    PRIMARY KEY (author_id),
    
    FOREIGN KEY (country_id)
		REFERENCES Countries(country_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE Countries (
	country_id INT AUTO_INCREMENT,
    name VARCHAR(20),
    region VARCHAR(20),
    
    PRIMARY KEY(country_id)
);

CREATE TABLE Comments (
	comment_id INT AUTO_INCREMENT,
    comment_date DATETIME DEFAULT NOW(),
    user_id INT,
    reference_id INT DEFAULT NULL,
    content TEXT NOT NULL,
    score INT DEFAULT 0,
    
    PRIMARY KEY(comment_id),
    
    FOREIGN KEY(user_id)
		REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
        
	FOREIGN KEY(reference_id)
		REFERENCES Comments(comment_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);