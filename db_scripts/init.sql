DROP DATABASE IF EXISTS test_db;    

CREATE DATABASE test_db;    

\c test_db;        

CREATE TABLE Role(
	RoleID SERIAL PRIMARY KEY,
	RoleName varchar(50)
);    
insert into Role (RoleName) values ('Admin'),('User');