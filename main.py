import psycopg
import os
import datetime
from datetime import datetime

entered_username = None
entered_password = None
id = None
trainer_id = None
admin_id = None
# Database parameters for login
db_params = {
    "host": "localhost",
    "dbname": "fitness_database",
    "user": "postgres",
    "password": "3005",
}

# Main loop function for I/O and calling other functions
def main():
    while True:
        print("\nHEALTH AND FITNESS CLUB MANAGEMENT SYSTEM\n")
        print("(1) Member Functions")
        print("(2) Trainer Functions")
        print("(3) Administrative Staff Functions")
        print("(4) Quit\n")



        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            print("(1) User Register")
            print("(2) User Login\n")

            try:
                choice = int(input("Enter your choice: "))
                os.system('cls')
                if(choice == 1):
                    user_registration()
                elif(choice == 2):
                    member_login()

            except ValueError:
                print("Invalid input, try again.")
                continue

            #
        elif choice == 2:
            print("(1) Trainer Register")
            print("(2) Trainer Login\n")

            try:
                choice = int(input("Enter your choice: "))
                os.system('cls')
                if(choice == 1):
                    trainer_register()
                elif(choice == 2):
                    trainer_login()

            except ValueError:
                print("Invalid input, try again.")
                continue




        elif choice == 3:
            print("(1) Admin Register")
            print("(2) Admin Login\n")

            try:
                choice = int(input("Enter your choice: "))
                os.system('cls')
                if(choice == 1):
                    admin_register()
                elif(choice == 2):
                    admin_login()

            except ValueError:
                print("Invalid input, try again.")
                continue


        elif choice == 4:
            print("Exiting the program.")
            break
        elif choice == 5:
            test()
            break


def test():
    print("test values below:")
    print(entered_username)
    print(entered_password)
    choice = int(input("Enter your choice: "))





def admin_register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    
    # Check if the username already exists
    if is_admin_username_available(username):
        try:
            with psycopg.connect(**db_params) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO administrator (username, password) VALUES (%s, %s)"
                    cursor.execute(sql, (username, password))
                    connection.commit()
                    print("Admin registered successfully!")
        except psycopg.Error as e:
            print(f"Database error: {e}")
    else:
        print("Username already exists. Please choose a different username.")

def is_admin_username_available(username):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM administrator WHERE username = %s"
                cursor.execute(sql, (username,))
                count = cursor.fetchone()[0]
                return count == 0
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False



def trainer_register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    email = input("Enter date of birth (YYYY-MM-DD): ")
    fname = input("Enter your first name: ")
    lname = input("Enter your last name: ")
    
    # Check if the username already exists
    if is_trainer_username_available(username):
        try:
            with psycopg.connect(**db_params) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO trainer (username, password, email, fname, lname) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql, (username, password, email, fname, lname))
                    connection.commit()
                    print("Trainer registered successfully!")
        except psycopg.Error as e:
            print(f"Database error: {e}")
    else:
        print("Username already exists. Please choose a different username.")

def is_trainer_username_available(username):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM trainer WHERE username = %s"
                cursor.execute(sql, (username,))
                count = cursor.fetchone()[0]
                return count == 0
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False



def trainer_login():
    global entered_username  # Specify that entered_username is a global variable
    global entered_password  # Specify that entered_password is a global variable
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if validate_trainer(username, password):
        print("Login successful!")
        entered_username = username
        entered_password = password
        trainer_functions()
    else:
        print("Invalid username or password.")


def admin_login():
    global entered_username  # Specify that entered_username is a global variable
    global entered_password  # Specify that entered_password is a global variable
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if validate_admin(username, password):
        print("Login successful!")
        entered_username = username
        entered_password = password
        admin_functions()
    else:
        print("Invalid username or password.")

def validate_admin(username, password):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id, COUNT(*) FROM administrator WHERE username = %s AND password = %s GROUP BY id"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if result:
                    user_id, count = result
                    #print(f"Validated user's ID: {user_id}")
                    global admin_id
                    admin_id = user_id
                    return count == 1
                else:
                    print("No user found with the provided credentials.")
                    return False
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False







def validate_trainer(username, password):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id, COUNT(*) FROM trainer WHERE username = %s AND password = %s GROUP BY id"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if result:
                    user_id, count = result
                    #print(f"Validated user's ID: {user_id}")
                    global trainer_id
                    trainer_id = user_id
                    return count == 1
                else:
                    print("No user found with the provided credentials.")
                    return False
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False












def get_user_id(username):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id FROM regular_member WHERE username = %s"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Return the user ID
                else:
                    return None  # Username not found
    except psycopg.Error as e:
        print(f"Database error: {e}")



def member_profile_viewing():
    while True:
        print("(1) View Profile By Username")
        print("(2) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            username = input("Enter the username: ")
            user_id = get_user_id(username)
            if user_id is not None:
                #print(user_id)
                view_profile(user_id)
                pass
            else:
                print("Username not found. Please try again.")
        elif choice == 2:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")




def admin_functions():
    while True:
        print("\nADMIN FUNCTIONS\n")
        print("(1) Room Booking Management")
        print("(2) Equipment Maintenance Logs")
        print("(3) Class Schedule Updating")
        print("(4) Billing Management")
        print("(5) Logout\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            room_booking()
        elif choice == 2:
            equipment_logs()
        if choice == 3:
            class_update()
        if choice == 4:
            billing_view()
        elif choice == 5:
            print("Logging out.")
            global entered_username
            global entered_password
            global admin_id
            entered_username = None
            entered_password = None
            admin_id = None
            break



def billing_view():
 while True:
        print("\nBILL MANAGEMENT\n")
        print("(1) View All Bills")
        print("(2) Edit Bill Price")
        print("(3) Delete Bill")
        print("(4) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            print_all_bills()
        if choice == 2:
            update_bill_amount()
        if choice == 3:
            delete_bill_by_id()
        if choice == 4:
            break



def print_all_bills():
    try:

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id, member_id, amount, payment_date FROM billing"
                cursor.execute(sql)
                bills = cursor.fetchall()

        if bills:
            print("BILLS\n")
            for bill in bills:
                bill_id, member_id, amount, payment_date = bill
                print(f"Bill ID: {bill_id}, Member ID: {member_id}, Amount: {amount}, Payment Date: {payment_date}")
        else:
            print("No bills found.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def delete_bill_by_id():
    try:

        bill_id = int(input("Enter the bill ID: "))

      
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
          
                cursor.execute("SELECT id FROM billing WHERE id = %s", (bill_id,))
                existing_bill = cursor.fetchone()
                
                if existing_bill:
                    # Delete the bill
                    cursor.execute("DELETE FROM billing WHERE id = %s", (bill_id,))
                    connection.commit()
                    print("Bill deleted successfully!")
                else:
                    print("No bill found with the specified ID.")
    except (ValueError, psycopg.Error) as e:
        print(f"Error: {e}")

def update_bill_amount():
    try:
       
        bill_id = int(input("Enter the bill ID: "))
        new_amount = float(input("Enter the new amount: "))

     
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
      
                cursor.execute("SELECT id FROM billing WHERE id = %s", (bill_id,))
                existing_bill = cursor.fetchone()
                
                if existing_bill:
            
                    cursor.execute("UPDATE billing SET amount = %s WHERE id = %s", (new_amount, bill_id))
                    connection.commit()
                    print("Bill amount updated successfully!")
                else:
                    print("No bill found with the specified ID.")
    except (ValueError, psycopg.Error) as e:
        print(f"Error: {e}")



















def class_update():
 while True:
        print("\nCLASS SCHEDULE UPDATING\n")
        print("(1) View All Sessions")
        print("(2) Change Session Time")
        print("(3) Change Session Capacity")
        print("(4) Cancel Session")
        print("(5) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_all_sessions()
        if choice == 2:
            change_session_time()
        if choice == 3:
            change_session_capacity()
        if choice == 4:
            cancel_session()
        if choice == 5:
            break


def view_all_sessions():
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM training_session"
                cursor.execute(sql)
                sessions = cursor.fetchall()
                if sessions:
                    print("ALL TRAINING SESSIONS\n")
                    for session in sessions:
                        print(f"Session ID: {session[0]}")
                        print(f"Trainer ID: {session[1]}")
                        print(f"Start Time: {session[2]}")
                        print(f"End Time: {session[3]}")
                        print(f"Max Capacity: {session[4]}")
                        print(f"Registered Users: {session[5]}")
                        print()
                else:
                    print("No training sessions found.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def change_session_time():
    try:
        session_id = int(input("Enter the ID of the session you want to change the time for: "))
        new_start_time = input("Enter the new start time (YYYY-MM-DD HH:MM:SS): ")
        new_end_time = input("Enter the new end time (YYYY-MM-DD HH:MM:SS): ")

        # Convert input strings to datetime objects
        new_start_time = datetime.strptime(new_start_time, "%Y-%m-%d %H:%M:%S")
        new_end_time = datetime.strptime(new_end_time, "%Y-%m-%d %H:%M:%S")

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE training_session SET start_time = %s, end_time = %s WHERE id = %s"
                cursor.execute(sql, (new_start_time, new_end_time, session_id))
                connection.commit()
                print("Session time updated successfully!")
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def change_session_capacity():
    try:
        session_id = int(input("Enter the ID of the session you want to change the capacity for: "))
        new_capacity = int(input("Enter the new max capacity: "))

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "UPDATE training_session SET max_capacity = %s WHERE id = %s"
                cursor.execute(sql, (new_capacity, session_id))
                connection.commit()
                print("Session capacity updated successfully!")
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def cancel_session():
    try:
        session_id = int(input("Enter the ID of the session you want to cancel: "))

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                # Delete training session users associated with the session ID
                sql_delete_users = "DELETE FROM training_session_users WHERE session_id = %s"
                cursor.execute(sql_delete_users, (session_id,))

                # Delete the training session itself
                sql_delete_session = "DELETE FROM training_session WHERE id = %s"
                cursor.execute(sql_delete_session, (session_id,))

                connection.commit()
                print("Session and associated users canceled successfully!")
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")







def room_booking():
    while True:
        print("\nROOM BOOKING MANAGEMENT\n")
        print("(1) View Booked Rooms")
        print("(2) Book New Room")
        print("(3) Unbook Room")
        print("(4) Back\n")
    
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_booked_rooms()
        if choice == 2:
            book_new_room()
        if choice == 3:
            unbook_room()

        if choice == 4:
            break


def view_booked_rooms():
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM room_booking"
                cursor.execute(sql)
                records = cursor.fetchall()
                if records:
                    print("BOOKED ROOMS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Room Number: {record[1]}")
                        print(f"Booking Start Date: {record[2]}")
                        print(f"Booking End Date: {record[3]}")
                        print()
                else:
                    print("No booked rooms found.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def book_new_room():
    try:
        room_number = input("Enter room number: ")
        booking_start_date = input("Enter booking start date (YYYY-MM-DD): ")
        booking_end_date = input("Enter booking end date (YYYY-MM-DD): ")

        # Convert input date strings to datetime objects
        booking_start_date = datetime.strptime(booking_start_date, "%Y-%m-%d").date()
        booking_end_date = datetime.strptime(booking_end_date, "%Y-%m-%d").date()

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO room_booking (room_number, booking_start_date, booking_end_date) VALUES (%s, %s, %s)"
                cursor.execute(sql, (room_number, booking_start_date, booking_end_date))
                connection.commit()
                print("New room booked successfully!")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def unbook_room():
    try:
        view_booked_rooms()
        booking_id = int(input("Enter the ID of the room booking you want to delete: "))

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM room_booking WHERE id = %s"
                cursor.execute(sql_check, (booking_id,))
                record = cursor.fetchone()

                if record:
                    sql_delete = "DELETE FROM room_booking WHERE id = %s"
                    cursor.execute(sql_delete, (booking_id,))
                    connection.commit()
                    print("Room booking deleted successfully!")
                else:
                    print("The specified room booking does not exist.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")


























 
def equipment_logs():
    while True:
        print("\nEQUIPMENT MAINTENANCE LOGS\n")
        print("(1) View Maintenance Logs")
        print("(2) Add Maintenance Log")
        print("(3) Delete Maintenance Log")
        print("(4) Back\n")
    
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_equipment_logs()
        if choice == 2:
            add_equipment_maintenance()
        if choice == 3:
            delete_equipment_maintenance()

        if choice == 4:
            break

def delete_equipment_maintenance():
    try:
        maintenance_id = int(input("Enter the ID of the equipment maintenance log you want to delete: "))

        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM equipment_maintenance WHERE id = %s"
                cursor.execute(sql_check, (maintenance_id,))
                record = cursor.fetchone()

                if record:
                    sql_delete = "DELETE FROM equipment_maintenance WHERE id = %s"
                    cursor.execute(sql_delete, (maintenance_id,))
                    connection.commit()
                    print("Equipment maintenance log deleted successfully!")
                else:
                    print("The specified equipment maintenance log does not exist.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")



def add_equipment_maintenance():
    try:
        maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
        description = input("Enter maintenance description: ")
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO equipment_maintenance (maintenance_date, description) VALUES (%s, %s)"
                cursor.execute(sql, (maintenance_date, description))
                connection.commit()
                print("New equipment maintenance log added successfully!")
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")


    
def view_equipment_logs():
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM equipment_maintenance"
                cursor.execute(sql)
                records = cursor.fetchall()
                if records:
                    print("EQUIPMENT MAINTENANCE LOGS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Maintenance Date: {record[1]}")
                        print(f"Description: {record[2]}")
                        print()
                else:
                    print("No equipment maintenance logs found.")
                    
    except psycopg.Error as e:
        print(f"Database error: {e}")


def trainer_functions():
    while True:
        print("\nTRAINER FUNCTIONS\n")
        print("(1) Schedule Management")
        print("(2) Member Profile Viewing")
        print("(3) Logout\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            trainer_schedule_management()
        elif choice == 2:
            member_profile_viewing()
        elif choice == 3:
            print("Logging out.")
            global entered_username
            global entered_password
            global trainer_id
            entered_username = None
            entered_password = None
            trainer_id = None
            break


def trainer_schedule_management():
    while True:
        print("\nTRAINER SCHEDULE MANAGEMENT\n")
        print("(1) View All Registered Sessions")
        print("(2) Show All Rooms")
        print("(3) Create Session")
        print("(4) Cancel Session")
        print("(5) Show All User Profiles In Session")
        print("(6) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_training_sessions()
        if choice == 2:
            view_booked_rooms()
        if choice == 3:
            create_training_session()
        if choice == 4:
            delete_training_session()
        if choice == 5:
            get_training_session_users()

        if choice == 6:
            break 


def get_training_session_users():
    try:
        session_id = int(input("Enter the ID of the training session: "))

        # Retrieve training session users for the given session ID
        training_session_users = []
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT member_id FROM training_session_users WHERE session_id = %s"
                cursor.execute(sql, (session_id,))
                rows = cursor.fetchall()
                for row in rows:
                    training_session_users.append(row[0])
        
        if training_session_users:
            print(f"Training Session Users for Session ID {session_id}:")
            for user_id in training_session_users:
                view_profile(user_id)
        else:
            print("No training session users found for the provided session ID.")
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")










def delete_training_session():
    try:
        session_id = int(input("Enter the ID of the training session you want to delete: "))

        # Check if the training session ID exists
        if not is_training_session_id_valid(session_id):
            print("Invalid training session ID. Please try again.")
            return

        # Delete the training session from the database
        delete_training_session_by_id(session_id)
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def is_training_session_id_valid(session_id):
    try:
        # Check if the training session ID exists in the training_session table
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id FROM training_session WHERE id = %s"
                cursor.execute(sql, (session_id,))
                return cursor.fetchone() is not None
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False

def delete_training_session_by_id(session_id):
    try:
        # Delete the training session and associated users from the database
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                # Delete training session users associated with the session ID
                sql_delete_users = "DELETE FROM training_session_users WHERE session_id = %s"
                cursor.execute(sql_delete_users, (session_id,))

                # Delete the training session itself
                sql_delete_session = "DELETE FROM training_session WHERE id = %s"
                cursor.execute(sql_delete_session, (session_id,))

                connection.commit()
                print(f"Training session with ID {session_id} and associated users deleted successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def create_training_session():
    try:
        room_booking_id = int(input("Enter the room booking ID: "))

        # Verify if the room booking ID exists
        if not is_room_booking_id_valid(room_booking_id):
            print("Invalid room booking ID. Please try again.")
            return

        start_time_str = input("Enter the start time (YYYY-MM-DD HH:MM:SS): ")
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")

        end_time_str = input("Enter the end time (YYYY-MM-DD HH:MM:SS): ")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        max_capacity = int(input("Enter the max capacity: "))

        # Insert the new training session into the database
        insert_training_session(room_booking_id, start_time, end_time, max_capacity)
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def is_room_booking_id_valid(room_booking_id):
    try:
        # Check if the room booking ID exists in the room_booking table
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id FROM room_booking WHERE id = %s"
                cursor.execute(sql, (room_booking_id,))
                return cursor.fetchone() is not None
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False

def insert_training_session(room_booking_id, start_time, end_time, max_capacity):
    try:
        global trainer_id
        # Insert the new training session into the database
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO training_session (trainer_id, room_booking_id, start_time, end_time, max_capacity, registered_users) 
                VALUES (%s, %s, %s, %s, %s, 0) RETURNING id
                """
                cursor.execute(sql, (trainer_id, room_booking_id, start_time, end_time, max_capacity))
                connection.commit()
                session_id = cursor.fetchone()[0]
                print(f"New training session created with ID: {session_id}")
    except psycopg.Error as e:
        print(f"Database error: {e}")




def view_training_sessions():
    global trainer_id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM training_session WHERE trainer_id = %s"
                cursor.execute(sql, (trainer_id,))
                records = cursor.fetchall()
                if records:
                    print("TRAINING SESSIONS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Room ID: {record[2]}")
                        print(f"Start Time: {record[3]}")
                        print(f"End Time: {record[4]}")
                        print(f"Max Capacity: {record[5]}")
                        print(f"Registered Users: {record[6]}")
                        print()
                else:
                    print("No registered training sessions found.")
                    
    except psycopg.Error as e:
        print(f"Database error: {e}")



































































# Member Functions
def member_login():
    global entered_username  # Specify that entered_username is a global variable
    global entered_password  # Specify that entered_password is a global variable
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if validate_member(username, password):
        print("Login successful!")
        entered_username = username
        entered_password = password
        member_functions()
    else:
        print("Invalid username or password.")




def validate_member(username, password):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id, COUNT(*) FROM regular_member WHERE username = %s AND password = %s GROUP BY id"
                cursor.execute(sql, (username, password))
                result = cursor.fetchone()
                if result:
                    user_id, count = result
                    #print(f"Validated user's ID: {user_id}")
                    global id
                    id = user_id
                    return count == 1
                else:
                    print("No user found with the provided credentials.")
                    return False
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False
def member_functions():
    while True:
        print("\nMEMBER FUNCTIONS\n")
        print("(1) Profile Management")
        print("(2) Dashboard Display")
        print("(3) Schedule Management")
        print("(4) Logout\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            profile_management()
        elif choice == 2:
            dashboard_display()
        elif choice == 3:
            schedule_management()
        elif choice == 4:
            print("Logging out.")
            global entered_username
            global entered_password
            global id
            entered_username = None
            entered_password = None
            id = None
            break


def schedule_management():
    while True:
        print("\nMEMBER SCHEDULE MANAGEMENT\n")
        print("(1) View All Open Sessions")
        print("(2) View All Registered Sessions")
        print("(3) Join Session")
        print("(4) Cancel Session")
        print("(5) Back")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            print_sessions_with_available_capacity()
        if choice == 2:
            global id
            print_sessions_for_member(id)
        if choice == 3:
            update_session_and_create_user()
        if choice == 4:
            cancel_session_member()
        if choice == 5:
            break



def cancel_session_member():
    session_id = int(input("Enter the session ID: "))
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                # Delete the training session user
                cursor.execute("DELETE FROM training_session_users WHERE session_id = %s AND member_id = %s", (session_id, id))
                
                # Update registered user count for the session
                cursor.execute("UPDATE training_session SET registered_users = registered_users - 1 WHERE id = %s", (session_id,))
                
                connection.commit()
                print("Session canceled successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")







def update_session_and_create_user():
    global id
    try:
        session_id = int(input("Enter the ID of the session: "))

        # Connect to the database and retrieve session details
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                # Retrieve session details
                sql_select_session = "SELECT max_capacity, registered_users FROM training_session WHERE id = %s"
                cursor.execute(sql_select_session, (session_id,))
                session_details = cursor.fetchone()

                if session_details:
                    max_capacity, registered_users = session_details
                    if registered_users < max_capacity:
                        # Update registered user count for the session
                        new_registered_users = registered_users + 1
                        sql_update_session = "UPDATE training_session SET registered_users = %s WHERE id = %s"
                        cursor.execute(sql_update_session, (new_registered_users, session_id))

                        # Create new training session user
                        member_id = id
                        sql_insert_user = "INSERT INTO training_session_users (session_id, member_id) VALUES (%s, %s)"
                        cursor.execute(sql_insert_user, (session_id, member_id))

                        connection.commit()
                        print("Registration successful!")
                    else:
                        print("Session is already at maximum capacity.")
                else:
                    print("Session not found.")
    except ValueError:
        print("Invalid input format.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def print_sessions_for_member(member_id):
    try:
        # Connect to the database and retrieve training sessions
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT ts.id, ts.trainer_id, ts.start_time, ts.end_time, ts.max_capacity, ts.registered_users
                FROM training_session ts
                JOIN training_session_users tsu ON ts.id = tsu.session_id
                WHERE tsu.member_id = %s
                """
                cursor.execute(sql, (member_id,))
                sessions = cursor.fetchall()

        if sessions:
            print(f"Training Sessions for Member ID {member_id}:")
            for session in sessions:
                session_id, trainer_id, start_time, end_time, max_capacity, registered_users = session
                print(f"Session ID: {session_id}, Trainer ID: {trainer_id}, Start Time: {start_time}, End Time: {end_time}, Max Capacity: {max_capacity}, Registered Users: {registered_users}")
        else:
            print(f"No training sessions found for Member ID {member_id}.")
    except psycopg.Error as e:
        print(f"Database error: {e}")












def print_sessions_with_available_capacity():
    try:
        # Connect to the database and retrieve training sessions
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = """
                SELECT id, trainer_id, start_time, end_time, max_capacity, registered_users
                FROM training_session
                WHERE max_capacity > registered_users
                """
                cursor.execute(sql)
                sessions = cursor.fetchall()

        if sessions:
            print("Training Sessions with Available Capacity:")
            for session in sessions:
                session_id, trainer_id, start_time, end_time, max_capacity, registered_users = session
                print(f"Session ID: {session_id}, Trainer ID: {trainer_id}, Start Time: {start_time}, End Time: {end_time}, Max Capacity: {max_capacity}, Registered Users: {registered_users}")
        else:
            print("No training sessions with available capacity found.")
    except psycopg.Error as e:
        print(f"Database error: {e}")













































def mark_fitness_goal_complete():
    view_fitness_goals() 
    global id
    try:
    
        health_stat_id = int(input("Enter the ID of the fitness goal you want to delete: "))
        
 
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM fitness_goals WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
                    print()
                  
                    sql_delete = "DELETE FROM fitness_goals WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    date_started = record[2]
                    goal = record[3]
                    current_date = datetime.now().strftime('%Y-%m-%d')
        
                    try:
                        print()
                        sql = "INSERT INTO achievements (member_id, date_started, date_completed, goal) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (id, date_started, current_date, goal))
                        connection.commit()
                        print("Fitness goal completed successfully!")
                    except psycopg.Error as e:
                        print(f"Database error: {e}")
                else:
                    print("The specified fitness goal either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")










 
def create_fitness_goal():
    global id
    date = input("Enter the date goal was started (YYYY-MM-DD): ")
    goal = input("Enter the goal: ")
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO fitness_goals (member_id, date, goal) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id, date, goal))
                connection.commit()
                print("Fitness goal added successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")


def delete_fitness_goal():
    view_fitness_goals() 
    global id
    try:
      
        health_stat_id = int(input("Enter the ID of the fitness goal you want to delete: "))
        
       
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM fitness_goals WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
            
                    sql_delete = "DELETE FROM fitness_goals WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    print("Fitness goal deleted successfully!")
                else:
                    print("The specified fitness goal either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")









def view_fitness_goals():
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM fitness_goals WHERE member_id = %s"
                cursor.execute(sql, (id,))
                records = cursor.fetchall()
                if records:
                    print("FITNESS GOALS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Date Started: {record[2]}")
                        print(f"Goal: {record[3]}")
                        print()
                else:
                    print("No fitness goals found.")
                    
    except psycopg.Error as e:
        print(f"Database error: {e}")





def fitness_goals_menu():
    while True:
        print("\nVIEW FITNESS GOALS\n")
        print("(1) View Fitness Goals")
        print("(2) Add Fitness Goal")
        print("(3) Delete Fitness Goal")
        print("(4) Mark Fitness Goal Complete")
        print("(5) Back")
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            view_fitness_goals()
        if choice == 2:
            create_fitness_goal()
        if choice == 3:
            delete_fitness_goal()
        if choice == 4:
            mark_fitness_goal_complete()
        if choice == 5:
            break



















def dashboard_display():
    while True:
        print("\nDASHBOARD DISPLAY\n")
        print("(1) View Health Goals")
        print("(2) View Fitness Goals")
        print("(3) View Achievements")
        print("(4) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            health_goals_menu()
        if choice == 2:
            fitness_goals_menu()
        if choice == 3:
            achievement_menu()
        if choice == 4:
            break


def achievement_menu():
    while True:
        print("\nDASHBOARD DISPLAY\n")
        print("(1) View Achievements")
        print("(2) Delete Achievement")
        print("(3) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            view_achievements()
        if choice == 2:
            delete_achievement()

        if choice == 3:
            break

def delete_achievement():
    view_achievements()  
    global id
    try:

        health_stat_id = int(input("Enter the ID of the achievement you want to delete: "))
        
     
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM achievements WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
          
                    sql_delete = "DELETE FROM achievements WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    print("Achievement deleted successfully!")
                else:
                    print("The specified achievement either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def view_achievements():
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM achievements WHERE member_id = %s"
                cursor.execute(sql, (id,))
                records = cursor.fetchall()
                if records:
                    print("ACHIEVEMENTS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Date Started: {record[2]}")
                        print(f"Date Completed: {record[3]}")
                        print(f"Achievement: {record[4]}")
                        print()
                else:
                    print("No achievements found.")
                    
    except psycopg.Error as e:
        print(f"Database error: {e}") 







def health_goals_menu():
    while True:
        print("\nVIEW HEALTH GOALS\n")
        print("(1) View Health Goals")
        print("(2) Add Health Goal")
        print("(3) Delete Health Goal")
        print("(4) Mark Health Goal Complete")
        print("(5) Back")
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            view_health_goals()
        if choice == 2:
            create_health_goal()
        if choice == 3:
            delete_health_goal()
        if choice == 4:
            mark_health_goal_complete()
        if choice == 5:
            break


























def mark_health_goal_complete():
    view_health_goals() 
    global id
    try:
     
        health_stat_id = int(input("Enter the ID of the health goal you want to delete: "))
        
     
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM health_goals WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
                    print()
                 
                    sql_delete = "DELETE FROM health_goals WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    date_started = record[2]
                    goal = record[3]
                    current_date = datetime.now().strftime('%Y-%m-%d')
        
                    try:
                        print()
                        sql = "INSERT INTO achievements (member_id, date_started, date_completed, goal) VALUES (%s, %s, %s, %s)"
                        cursor.execute(sql, (id, date_started, current_date, goal))
                        connection.commit()
                        print("Health goal completed successfully!")
                    except psycopg.Error as e:
                        print(f"Database error: {e}")
                else:
                    print("The specified health goal either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")








def view_health_goals():
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM health_goals WHERE member_id = %s"
                cursor.execute(sql, (id,))
                records = cursor.fetchall()
                if records:
                    print("HEALTH GOALS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Date Started: {record[2]}")
                        print(f"Goal: {record[3]}")
                        print()
                else:
                    print("No health goals found.")
                    
    except psycopg.Error as e:
        print(f"Database error: {e}")

 
def create_health_goal():
    global id
    date = input("Enter the date goal was started (YYYY-MM-DD): ")
    goal = input("Enter the goal: ")
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO health_goals (member_id, date, goal) VALUES (%s, %s, %s)"
                cursor.execute(sql, (id, date, goal))
                connection.commit()
                print("Health goal added successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")


def delete_health_goal():
    view_health_goals() 
    global id
    try:
 
        health_stat_id = int(input("Enter the ID of the health goal you want to delete: "))
        
     
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM health_goals WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
                 
                    sql_delete = "DELETE FROM health_goals WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    print("Fitness statistic deleted successfully!")
                else:
                    print("The specified health goal either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")












def create_new_bill(member_id, amount):
    try:

        payment_date = datetime.now().date()

  
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
     
                cursor.execute("INSERT INTO billing (member_id, amount, payment_date) VALUES (%s, %s, %s)", (member_id, amount, payment_date))
                connection.commit()
                print("New bill created successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")








def user_registration():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    birthday = input("Enter date of birth (YYYY-MM-DD): ")
    consent =  input("Upon registering you will be charged $30.0 do you consent? (Y / N): ")
    if consent.upper() != "Y":
        return

    
    # Check if the username already exists
    if is_username_available(username):
        try:
            with psycopg.connect(**db_params) as connection:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO regular_member (username, password, birthday) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (username, password, birthday))
                    connection.commit()
                    member_id = get_user_id(username)
             
                    print(f"User registered successfully with ID: {member_id}")
            
                    create_new_bill(member_id, 30)


        except psycopg.Error as e:
            print(f"Database error: {e}")
    else:
        print("Username already exists. Please choose a different username.")

def is_username_available(username):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM regular_member WHERE username = %s"
                cursor.execute(sql, (username,))
                count = cursor.fetchone()[0]
                return count == 0
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False

def profile_management():
    while True:
        print("\nPROFILE MANAGEMENT\n")
        print("(1) View Profile")
        print("(2) Update Personal Information")
        print("(3) Update Health Stats")
        print("(4) Update Fitness Stats")
        print("(5) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            global id
            view_profile(id)
        
        if choice == 2:
            update_personal_info()

        if choice == 3:
            update_health_metrics()

        if choice == 4:
            update_fitness_metrics()
            
        if choice == 5:
            break



def update_fitness_metrics():
    while True:
        print("\nUPDATE FITNESS STATISTICS\n")
        print("(1) View Fitness Statistics")
        print("(2) Add Fitness Statistic")
        print("(3) Delete Fitness Statistic")
        print("(4) Back")
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_fitness_statistics()
        if choice == 2:
            create_fitness_statistics()
        if choice == 3:
            delete_fitness_statistic()
        if choice == 4:
            break



def view_fitness_statistics():
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM fitness_stats WHERE member_id = %s"
                cursor.execute(sql, (id,))
                records = cursor.fetchall()
                if records:
                    print("HEALTH STATSTICS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Date: {record[2]}")
                        print(f"Pushups: {record[3]}")
                        print(f"Pullups: {record[4]}")
                        print(f"Situps: {record[5]}")
                        print(f"Pounds Lifted: {record[6]}")
                        print(f"Minutes of Cardio: {record[7]}")
                        print(f"BMI: {record[8]}")
                        print()
                else:
                    print("No health statistics found.")
                    create_fitness_statistics()
    except psycopg.Error as e:
        print(f"Database error: {e}")


#fitness_database
def create_fitness_statistics():
    global id
    date = input("Enter the date (YYYY-MM-DD): ")
    pushups = float(input("Enter number of pushups: "))
    pullups = float(input("Enter number of pullups: "))
    situps = float(input("Enter number of situps: "))
    pounds_lifted = float(input("Enter pounds lifted: "))
    minutes_of_cardio = float(input("Enter minutes of cardio: "))
    bmi = float(input("BMI: "))

    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO fitness_stats (member_id, date, pushups, pullups, situps, pounds_lifted, minutes_of_cardio, bmi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (id, date, pushups, pullups, situps, pounds_lifted, minutes_of_cardio, bmi))
                connection.commit()
                print("Fitness statistics added successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")



def delete_fitness_statistic():
    view_fitness_statistics()  
    global id
    try:
       
        health_stat_id = int(input("Enter the ID of the fitness statistic you want to delete: "))
        
      
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM fitness_stats WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
                    # If the health statistic belongs to the user, delete it
                    sql_delete = "DELETE FROM fitness_stats WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    print("Fitness statistic deleted successfully!")
                else:
                    print("The specified fitness statistic either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")



























def update_health_metrics():
    while True:
        print("\nUPDATE HEALTH STATISTICS\n")
        print("(1) View Health Statistics")
        print("(2) Add Health Statistic")
        print("(3) Delete Health Statistic")
        print("(4) Back")
        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')
        except ValueError:
            print("Invalid input, try again.")
            continue
        if choice == 1:
            view_health_statistics()
        if choice == 2:
            create_health_statistics()
        if choice == 3:
            delete_health_statistic()
        if choice == 4:
            break


def delete_health_statistic():
    view_health_statistics()  
    global id
    try:
   
        health_stat_id = int(input("Enter the ID of the health statistic you want to delete: "))
        
      
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM health_stats WHERE id = %s AND member_id = %s"
                cursor.execute(sql_check, (health_stat_id, id))
                record = cursor.fetchone()

                if record:
           
                    sql_delete = "DELETE FROM health_stats WHERE id = %s"
                    cursor.execute(sql_delete, (health_stat_id,))
                    connection.commit()
                    print("Health statistic deleted successfully!")
                else:
                    print("The specified health statistic either does not exist or does not belong to you.")
    except ValueError:
        print("Please enter a valid integer for the ID.")
    except psycopg.Error as e:
        print(f"Database error: {e}")




def view_health_statistics():
    global id
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM health_stats WHERE member_id = %s"
                cursor.execute(sql, (id,))
                records = cursor.fetchall()
                if records:
                    print("HEALTH STATSTICS\n")
                    for record in records:
                        print(f"ID: {record[0]}")
                        print(f"Date: {record[2]}")
                        print(f"Blood Pressure: {record[3]}")
                        print(f"Cholesterol: {record[4]}")
                        print(f"Height: {record[5]}")
                        print(f"Weight: {record[6]}")
                        print()
                else:
                    print("No health statistics found.")
                    create_health_statistics(id)
    except psycopg.Error as e:
        print(f"Database error: {e}")

def create_health_statistics():
    global id
    date = input("Enter the date (YYYY-MM-DD): ")
    blood_pressure = float(input("Enter blood pressure: "))
    cholesterol = float(input("Enter cholesterol level: "))
    height = float(input("Enter height (in feet): "))
    weight = float(input("Enter weight (in lbs): "))

    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO health_stats (member_id, date, blood_pressure, cholesterol, height, weight) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (id, date, blood_pressure, cholesterol, height, weight))
                connection.commit()
                print("Health statistics added successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")



def update_personal_info():
    while True:
        print("\nUPDATE PERSONAL INFORMATION\n")
        print("(1) Edit first name")
        print("(2) Edit last name")
        print("(3) Edit email")
        print("(4) Back\n")

        try:
            choice = int(input("Enter your choice: "))
            os.system('cls')  
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice == 1:
            new_fname = input("Enter your new first name: ")
            update_field('fname', new_fname)
        elif choice == 2:
            new_lname = input("Enter your new last name: ")
            update_field('lname', new_lname)
        elif choice == 3:
            new_email = input("Enter your new email: ")
            update_field('email', new_email)
        elif choice == 4:
            break
        else:
            print("Invalid choice, please select again.")


def update_field(field, new_value):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = f"UPDATE regular_member SET {field} = %s WHERE username = %s"
                cursor.execute(sql, (new_value, entered_username))
                connection.commit()
                print(f"{field.capitalize()} updated successfully!")
    except psycopg.Error as e:
        print(f"Database error: {e}")

def view_profile(uid):
    try:
        with psycopg.connect(**db_params) as connection:
            with connection.cursor() as cursor:
                sql = "SELECT id, username, fname, lname, email, birthday FROM regular_member WHERE id = %s"
                cursor.execute(sql, (uid,))
                result = cursor.fetchone()
                if result:
                    while True:
                        os.system('cls')
                        user_id, username, fname, lname, email, birthday = result
                        print(f"User ID: {user_id}")
                        print(f"Username: {username}")
                        print(f"First Name: {fname}")
                        print(f"Last Name: {lname}")
                        print(f"Email: {email}")
                        print(f"Date of birth: {birthday}")
                        print("(1) Back")
                        signedin_id = user_id
                    
                        choice = int(input("Enter your choice: "))
                        if(choice == 1):
                            os.system('cls')
                            break
                  
                else:
                    print("No user found with the provided credentials.")
                    return False
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False




if __name__ == "__main__":
    main()































