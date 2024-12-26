DROP TABLE IF EXISTS Comments;

CREATE TABLE Comments (
    comment_id INT AUTO_INCREMENT,
    book_id INT,
    comment_datetime DATETIME DEFAULT NOW(),
    user_id INT,
    content TEXT NOT NULL,
    score INT DEFAULT 0,
    
    PRIMARY KEY(comment_id),
    
    FOREIGN KEY(book_id)
        REFERENCES Books(book_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    
    FOREIGN KEY(user_id)
        REFERENCES Users(user_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
