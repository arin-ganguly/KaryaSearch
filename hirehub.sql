-- Create database
CREATE DATABASE IF NOT EXISTS mamaar;
USE mamaar;

-- ======================
-- CLIENT TABLE
-- ======================
CREATE TABLE client (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  mobile BIGINT NOT NULL,
  city VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  isAdmin TINYINT(1) DEFAULT 0
);

INSERT INTO client (name, mobile, city, email, password, isAdmin) VALUES
('Rahul Sharma', 9876543210, 'Delhi', 'rahul@gmail.com', 'pass', 1),
('Ananya Das', 9123456780, 'Kolkata', 'ananya@gmail.com', 'pass', 0),
('Arjun Patel', 9988776655, 'Ahmedabad', 'arjun@gmail.com', 'pass', 0);

-- ======================
-- WORKER TABLE
-- ======================
CREATE TABLE worker (
  worker_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  mobile BIGINT NOT NULL,
  city VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(50) NOT NULL,
  title VARCHAR(50) NOT NULL,
  rating FLOAT DEFAULT 0
);

INSERT INTO worker (name, mobile, city, email, password, title, rating) VALUES
('Ramesh Kumar', 9012345678, 'Delhi', 'ramesh@gmail.com', 'pass', 'Math Teacher', 4.5),
('Sanjay Verma', 9871122334, 'Mumbai', 'sanjay@gmail.com', 'pass', 'Chef', 4.2),
('Imran Khan', 9988771122, 'Hyderabad', 'imran@gmail.com', 'pass', 'Tour Guide', 3.9),
('Vikram Singh', 9090909090, 'Bangalore', 'vikram@gmail.com', 'pass', 'Mechanical Engineer', 4.0);

-- ======================
-- JOB TABLE
-- ======================
CREATE TABLE job (
  job_id INT AUTO_INCREMENT PRIMARY KEY,
  worker_id INT,
  job_title VARCHAR(50) NOT NULL,
  rate INT NOT NULL,
  description TEXT,
  FOREIGN KEY (worker_id) REFERENCES worker(worker_id) ON DELETE CASCADE
);

INSERT INTO job (worker_id, job_title, rate, description) VALUES
(1, 'Home Math Tutor', 500, 'Provide mathematics tuition for school students'),
(2, 'Private Chef Service', 800, 'Professional chef service for home events'),
(3, 'City Tour Guide', 1000, 'Guided tour across historical places'),
(4, 'Mechanical Repair Expert', 1200, 'Repair and maintenance of machines');

-- ======================
-- REQUESTED TABLE
-- ======================
CREATE TABLE requested (
  job_id INT,
  worker_id INT,
  client_id INT,
  FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE,
  FOREIGN KEY (worker_id) REFERENCES worker(worker_id) ON DELETE CASCADE,
  FOREIGN KEY (client_id) REFERENCES client(user_id) ON DELETE CASCADE
);

-- ======================
-- ACCEPTED TABLE
-- ======================
CREATE TABLE accepted (
  job_id INT,
  worker_id INT,
  client_id INT,
  FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE,
  FOREIGN KEY (worker_id) REFERENCES worker(worker_id) ON DELETE CASCADE,
  FOREIGN KEY (client_id) REFERENCES client(user_id) ON DELETE CASCADE
);