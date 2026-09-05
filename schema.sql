use mysql;
begin;
create user 'appuser'@'%' identified with mysql_native_password by "Testing#123";
grant all privileges on employee_db.* to 'appuser'@'%';
flush privileges;


USE employee_db;
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

commit;
