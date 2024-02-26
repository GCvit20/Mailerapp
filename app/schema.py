instructions = [
    'DROP TABLE IF EXISTS email;',
    """
        CREATE TABLE email (
            id INT PRIMARY KEY AUTO_INCREMENT,
            email TEXT NOT NULL,
            subjet TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """
]