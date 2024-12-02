CREATE TABLE Publishers(
	publisher_id INT AUTO_INCREMENT,
    name VARCHAR(50),
    
    PRIMARY KEY(publisher_id)
);

CREATE TABLE Books (
	book_id INT AUTO_INCREMENT,
    isbn CHAR(13),
    title VARCHAR(50) NOT NULL,
    author_id INT,
    publication_year YEAR,
    publisher_id INT,
    
    PRIMARY KEY (book_id),
    
    FOREIGN KEY (author_id)
		REFERENCES Authors (author_id)
		ON DELETE SET NULL
        ON UPDATE CASCADE,
    
    FOREIGN KEY (publisher_id)
        REFERENCES Publishers (publisher_id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

CREATE TABLE BookDetails (
	book_details_id INT AUTO_INCREMENT,
	book_id INT,
    rating DECIMAL(2,1) DEFAULT 0 CHECK(rating <= 10 AND rating >=0),
	language varchar(20),
    page_number SMALLINT,
    image_path varchar(1024),
    
    PRIMARY KEY(book_details_id),
    
    FOREIGN KEY(book_id)
		REFERENCES Books (book_id)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);
