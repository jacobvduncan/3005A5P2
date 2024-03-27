CREATE TABLE regular_member (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  email VARCHAR(255),
  fname VARCHAR(255),
  lname VARCHAR(255),
  birthday date,
  password VARCHAR(255)
);

CREATE TABLE trainer (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  email VARCHAR(255),
  fname VARCHAR(255),
  lname VARCHAR(255),
  password VARCHAR(255)
);

CREATE TABLE administrator (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255),
  password VARCHAR(255)
);

CREATE TABLE fitness_stats (
  id SERIAL PRIMARY KEY,
  member_id INT,
  date DATE,
  pushups FLOAT,
  pullups FLOAT,
  situps FLOAT,
  pounds_lifted FLOAT,
  minutes_of_cardio FLOAT,
  bmi FLOAT,
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

CREATE TABLE fitness_goals (
  id SERIAL PRIMARY KEY,
  member_id INT,
  date DATE,
  goal VARCHAR(255),
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

CREATE TABLE health_stats (
  id SERIAL PRIMARY KEY,
  member_id INT,
  date DATE,
  blood_pressure FLOAT,
  cholesterol FLOAT,
  height FLOAT,
  weight FLOAT,
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

CREATE TABLE health_goals (
  id SERIAL PRIMARY KEY,
  member_id INT,
  date DATE,
  goal VARCHAR(255),
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

CREATE TABLE achievements (
  id SERIAL PRIMARY KEY,
  member_id INT,
  date_started DATE,
  date_completed DATE,
  goal VARCHAR(255),
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

CREATE TABLE room_booking (
  id SERIAL PRIMARY KEY,
  room_number VARCHAR(255),
  booking_start_date DATE,
  booking_end_date DATE,
  trainer_id INT, 
  FOREIGN KEY (trainer_id) REFERENCES trainer(id)
);

CREATE TABLE training_session (
  id SERIAL PRIMARY KEY,
  trainer_id INT,
  room_booking_id INT,  
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  max_capacity INT,
  registered_users INT,
  FOREIGN KEY (trainer_id) REFERENCES trainer(id),
  FOREIGN KEY (room_booking_id) REFERENCES room_booking(id) 

);

CREATE TABLE training_session_users (
  session_id INT,
  member_id INT,
  FOREIGN KEY (session_id) REFERENCES training_session(id),
  FOREIGN KEY (member_id) REFERENCES regular_member(id),
  PRIMARY KEY (session_id, member_id)
);


CREATE TABLE equipment_maintenance (
  id SERIAL PRIMARY KEY,
  maintenance_date DATE,
  description VARCHAR(255)
);

CREATE TABLE class_schedule (
  id SERIAL PRIMARY KEY,
  administrator_id INT,
  class_name VARCHAR(255),
  class_date DATE,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  FOREIGN KEY (administrator_id) REFERENCES administrator(id)
);

CREATE TABLE billing (
  id SERIAL PRIMARY KEY,
  member_id INT,
  amount FLOAT,
  payment_date DATE,
  FOREIGN KEY (member_id) REFERENCES regular_member(id)
);

