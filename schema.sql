

USE python_employee_db;

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL
);

INSERT INTO employees (name, department)
VALUES
('John', 'DevOps'),
('David', 'Platform'),
('Rahul', 'SRE');
