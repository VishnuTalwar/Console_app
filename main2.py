import sqlite3
import datetime

# creating a connection to the database
conn = sqlite3.connect('vaccine.db')
cursor = conn.cursor()
# creating a table to store user information
conn.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

# creating a table to store vaccination center information
cursor.execute('''CREATE TABLE IF NOT EXISTS vaccination_centers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    working_hours TEXT NOT NULL
                )''')

# inserting some sample data
cursor.execute("INSERT INTO vaccination_centers (location, working_hours) VALUES (?, ?)",
               ("NEW DELHI", "9:00 AM - 5:00 PM"))
cursor.execute("INSERT INTO vaccination_centers (location, working_hours) VALUES (?, ?)",
               ("MUMBAI", "10:00 AM - 6:00 PM"))
cursor.execute("INSERT INTO vaccination_centers (location, working_hours) VALUES (?, ?)",
               ("BANGALORE", "8:00 AM - 4:00 PM"))

# creating a table to store appointment information
cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    location TEXT NOT NULL,
                    time TEXT NOT NULL,
                    date TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    is_admin INTEGER NOT NULL
                )''')

# creating a table to store vaccination center information
cursor.execute('''CREATE TABLE IF NOT EXISTS vaccination_centers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    working_hours TEXT NOT NULL
                )''')
######
#Run the code which is below when running the code for the first time then comment this block because the table would have been created.
# creating a table to store appointment information
# cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT NOT NULL,
#                     location TEXT NOT NULL,
#                     time TEXT NOT NULL,3
#                     date TEXT NOT NULL
#                 )''')
# cursor.execute('''ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;''')
######
cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
               ("admin", "adminpassword", 1))

# inserting an admin user into the user table
cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
               ("admin", "adminpassword", 1))

conn.commit()
# closing the connection
conn.close()


def show_menu():
    print("1. Search for vaccination centers")
    print("2. Book an appointment")
    print("3. Login")
    print("4. Signup")
    print("5. Admin Login")
    print("6. Exit")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    row = cursor.fetchone()

    if row is None:
        print("Invalid username or password")
    else:
        print("Login successful")

    conn.close()


def signup():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()


    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row is not None:
        print("Username already exists")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Signup successful")

    conn.close()


def search():
    search_type = input(
        "What would you like to search for?\n1. Vaccination centers\n2. Booked appointments\nEnter your choice: ")

    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()

    if search_type == "1":
        location = input("Enter your location: ")


        cursor.execute("SELECT * FROM vaccination_centers WHERE location = ?", (location,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No vaccination centers found")
        else:
            for row in rows:
                print(f"{row[1]} - {row[2]}")

    elif search_type == "2":
        username = input("Enter your username: ")


        cursor.execute("SELECT * FROM appointments WHERE username = ?", (username,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No appointments found")
        else:
            for row in rows:
                print(f"{row[3]} at {row[2]} on {row[4]}")

    else:
        print("Invalid choice")

    conn.close()


def book_appointment():
    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()


    today = datetime.date.today()
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE date = ?", (today,))
    count = cursor.fetchone()[0]

    if count >= 10:
        print("No more slots available for today")
    else:
        username = input("Enter your username: ")
        location = input("Enter the vaccination center location: ")
        time = input("Enter the time (e.g. 10:30 AM): ")

        # inserting a new appointment
        cursor.execute("INSERT INTO appointments (username, location, time, date) VALUES (?, ?, ?, ?)",
                       (username, location, time, today))
        conn.commit()
        print("Appointment scheduled")

    conn.close()


#function to admin log in
def admin_login():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")

        conn = sqlite3.connect('vaccine.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user is None:
            print("Invalid username or password. Please try again.")
        else:
            return admin_main()


#function to add a vaccination center
def add_vaccination_center():
    location = input("Enter location: ")
    working_hours = input("Enter working hours: ")

    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO vaccination_centers (location, working_hours) VALUES (?, ?)", (location, working_hours))

    conn.commit()
    conn.close()

    print("Vaccination center added successfully.")


#function to get dosage details grouped by center
def get_dosage_details():
    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()

    cursor.execute("SELECT location, COUNT(*) as dosage_count FROM appointments GROUP BY location")
    dosage_details = cursor.fetchall()

    conn.close()

    print("Dosage details:")
    for row in dosage_details:
        print(row[0] + ": " + str(row[1]))


#function to remove a vaccination center
def remove_vaccination_center():
    location = input("Enter location of vaccination center to remove: ")

    conn = sqlite3.connect('vaccine.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vaccination_centers WHERE location = ?", (location,))

    conn.commit()
    conn.close()

    print("Vaccination center removed successfully.")


#main function to handle admin input
def admin_main():
    while True:
        print("Welcome to the vaccination app.")

        print("\nAdmin Menu")
        print("1. Add Vaccination Center")
        print("2. Get Dosage Details (group by center)")
        print("3. Remove Vaccination Center")
        print("4. Logout")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            add_vaccination_center()
        if choice == "2":
            get_dosage_details()
        if choice == "3":
            remove_vaccination_center()
        if choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

#main funtion to handle user input
while True:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        search()
    elif choice == '2':
        book_appointment()
    elif choice == '3':
        login()
    elif choice == '4':
        signup()
    elif choice == '5':
        admin_login()
    elif choice == '6':
        print("GoodBye!")
        break
    else:
        print("Invalid choice")
