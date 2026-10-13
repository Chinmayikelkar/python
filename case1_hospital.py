import sqlite3

con = sqlite3.connect("HospitalManagement.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS hospital (
    hospital_id INTEGER PRIMARY KEY,
    hospital_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    established_year INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS doctor (
    doctor_id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    specialization VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    experience INTEGER,
    hospital_id INTEGER,
    salary REAL,
    FOREIGN KEY (hospital_id) REFERENCES hospital(hospital_id)
)
""")
con.commit()


def read_doctor(name):
    cur.execute("SELECT * FROM doctor WHERE name = ?", (name,))
    print("Doctor:", cur.fetchall())


def read_hospital(name):
    cur.execute("SELECT * FROM hospital WHERE hospital_name = ?", (name,))
    print("Hospital:", cur.fetchall())


def get_specialist_doctors_list(specialization, salary):
    cur.execute("""
        SELECT * FROM doctor
        WHERE specialization = ? AND salary > ?
    """, (specialization, salary))
    print("Specialist doctors:", cur.fetchall())


def doctors_by_hospital(hospital_name):
    cur.execute("""
        SELECT d.* FROM doctor d
        JOIN hospital h ON d.hospital_id = h.hospital_id
        WHERE h.hospital_name = ?
    """, (hospital_name,))
    print("Doctors in hospital:", cur.fetchall())


def update_experience(doctor_id, experience):
    cur.execute("UPDATE doctor SET experience = ? WHERE doctor_id = ?",
                (experience, doctor_id))
    con.commit()
    print("Experience updated." if cur.rowcount else "Doctor not found.")


while True:
    print("""
1. Read doctor details
2. Read hospital details
3. Find specialist doctors by salary
4. List doctors by hospital
5. Update doctor experience
6. Exit
""")
    choice = input("Enter choice: ")

    try:
        if choice == "1":
            read_doctor(input("Doctor name: "))
        elif choice == "2":
            read_hospital(input("Hospital name: "))
        elif choice == "3":
            specialization = input("Specialization: ")
            salary = float(input("Minimum salary: "))
            get_specialist_doctors_list(specialization, salary)
        elif choice == "4":
            doctors_by_hospital(input("Hospital name: "))
        elif choice == "5":
            doctor_id = int(input("Doctor ID: "))
            experience = int(input("New experience: "))
            update_experience(doctor_id, experience)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")
    except (ValueError, sqlite3.Error) as e:
        print("Error:", e)

con.close()
