DROP TABLE IF EXISTS Subscriptions;
DROP TABLE IF EXISTS Users;

CREATE TABLE Subscriptions(
    subscription_id INT AUTO_INCREMENT,
    subscription_plan VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY (subscription_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE Users(
    user_id INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    date_of_birth DATE,
    gender VARCHAR(10),
    subscription_id INT NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id),
    FOREIGN KEY (subscription_id) 
        REFERENCES Subscriptions(subscription_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
