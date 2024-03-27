-- Inserting data into regular_member table
INSERT INTO regular_member (username, email, fname, lname, birthday, password)
VALUES ('john_doe', 'john@mail.com', 'John', 'Doe', '1990-05-15', 'password123'),
       ('jane_smith', 'jane@mail.com', 'Jane', 'Smith', '1985-09-20', 'p@ssw0rd'),
       ('jacobvduncan', 'jacobvduncan@mail.com', 'Jacob', 'Duncan', '1985-09-20', '3005');

-- Inserting data into trainer table
INSERT INTO trainer (username, email, fname, lname, password)
VALUES ('trainer1', 'trainer1@mail.com', 'Trainer', 'One', 'trainerpass'),
       ('trainer1', 'trainer1@mail.com', 'Trainer', 'One', 'trainerpass'),
       ('trainer', 'trainer@mail.com', 'Trainer', 'Two', '3005');

-- Inserting data into administrator table
INSERT INTO administrator (username, password)
VALUES ('admin', '3005');

-- Inserting data into fitness_stats table
INSERT INTO fitness_stats (member_id, date, pushups, pullups, situps, pounds_lifted, minutes_of_cardio, bmi)
VALUES (1, '2024-03-25', 50, 20, 30, 1000, 30, 25.5),
       (2, '2024-03-25', 40, 15, 25, 800, 25, 23.0);

-- Inserting data into fitness_goals table
INSERT INTO fitness_goals (member_id, date, goal)
VALUES (1, '2024-04-30', 'Increase pushups to 100'),
       (2, '2024-04-30', 'Achieve 20 pullups');

-- Inserting data into health_stats table
INSERT INTO health_stats (member_id, date, blood_pressure, cholesterol, height, weight)
VALUES (1, '2024-03-25', 120, 180, 175, 70),
       (2, '2024-03-25', 130, 190, 165, 65);

-- Inserting data into health_goals table
INSERT INTO health_goals (member_id, date, goal)
VALUES (1, '2024-04-30', 'Lower blood pressure to 110/70'),
       (2, '2024-04-30', 'Reduce cholesterol levels');

-- Inserting data into achievements table
INSERT INTO achievements (member_id, date_started, date_completed, goal)
VALUES (1, '2024-03-01', '2024-03-25', 'Reached fitness goals'),
       (2, '2024-03-01', '2024-03-25', 'Started weight loss journey');

-- Inserting data into room_booking table
INSERT INTO room_booking (room_number, booking_start_date, booking_end_date, trainer_id)
VALUES ('Room A', '2024-04-01', '2024-04-02', 1),
       ('Room B', '2024-04-03', '2024-04-04', 2);

-- Inserting data into training_session table
INSERT INTO training_session (trainer_id, room_booking_id, start_time, end_time, max_capacity, registered_users)
VALUES (1, 1, '2024-04-01 10:00:00', '2024-04-01 11:00:00', 10, 5),
       (2, 2, '2024-04-03 14:00:00', '2024-04-03 15:00:00', 15, 8);

-- Inserting data into training_session_users table
INSERT INTO training_session_users (session_id, member_id)
VALUES (1, 1),
       (1, 2),
       (2, 1);

-- Inserting data into equipment_maintenance table
INSERT INTO equipment_maintenance (maintenance_date, description)
VALUES ('2024-03-28', 'Treadmill maintenance'),
       ('2024-04-05', 'Weight machine lubrication');

-- Inserting data into class_schedule table
INSERT INTO class_schedule (administrator_id, class_name, class_date, start_time, end_time)
VALUES (1, 'Gym Class', '2024-04-05', '2024-04-05 09:00:00', '2024-04-05 10:00:00'),
       (1, 'Pushup Class', '2024-04-06', '2024-04-06 18:00:00', '2024-04-06 19:00:00');

-- Inserting data into billing table
INSERT INTO billing (member_id, amount, payment_date)
VALUES (1, 50.00, '2024-03-27'),
       (2, 60.00, '2024-03-27');