-- Connect to the database
\c mydatabase;

-- Create Users table
CREATE TABLE Users(
    email TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    pin TEXT NOT NULL -- haven't done it to be hashed
);

-- Create Slides table
CREATE TABLE Slides (
    sid SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    bytes BYTEA NOT NULL,
    generated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email TEXT REFERENCES Users(email)
);

-- Create Temps table for OTP management
CREATE TABLE Temps (
    time_otp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    otp CHAR(6) NOT NULL, 
    email TEXT REFERENCES Users(email), 
    PRIMARY KEY (time_otp, email)
);
