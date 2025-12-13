SELECT * FROM users;

SELECT * FROM calculations;

SELECT users.username, calculations.operation, calculations.operand_a, calculations.operand_b, calculations.result
FROM calculations
JOIN users ON calculations.user_id = users.id;
