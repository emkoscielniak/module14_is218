INSERT INTO users (username, email, password_hash) VALUES 
('alice', 'alice@example.com', '$pbkdf2-sha256$29000$...$...'),
('bob', 'bob@example.com', '$pbkdf2-sha256$29000$...$...');

INSERT INTO calculations (operation, operand_a, operand_b, result, user_id) VALUES
('add', 2, 3, 5, 1),
('divide', 10, 2, 5, 1),
('multiply', 4, 5, 20, 2);
