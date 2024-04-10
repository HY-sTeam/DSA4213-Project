\c mydatabase
-- create schema dsa4213_project;

-- CREATE TABLE slides (
	-- slides_id int,
	-- title VARCHAR(80),
	-- bytes bytea,
	-- generated_time TIMESTAMP without time zone not null default(CURRENT_TIMESTAMP at time zone 'utc'),
	-- user_id int
-- ); 	

-- CREATE TABLE Role(
	-- RoleID SERIAL PRIMARY KEY,
	-- RoleName varchar(50)
-- );    
-- insert into Role (RoleName) values ('Admin'),('User');


CREATE TABLE Users (
	email TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	pin TEXT NOT NULL
);

CREATE TABLE Slides (
	sid SERIAL PRIMARY KEY,
	title TEXT NOT NULL,
	bytes BYTEA NOT NULL,
	generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	email TEXT REFERENCES Users(email)
);