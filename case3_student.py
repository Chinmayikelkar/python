import sqlite3

con = sqlite3.connect("Student.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Student (
    StudentID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    dob TEXT,
    contact_details TEXT,
    status TEXT CHECK (
        status IN ('admitted', 'cancelled', 'InProgress')
    )
)
""")
con.commit()


def add_student():
    data = (
        int(input("Student ID: ")),
        input("Name: "),
        input("Date of birth (YYYY-MM-DD): "),
        input("Contact details: "),
        input("Status (admitted/cancelled/InProgress): ")
    )
    cur.execute("INSERT INTO Student VALUES (?, ?, ?, ?, ?)", data)
    con.commit()
    print("Student added.")


def update_student():
    sid = int(input("Student ID: "))
    name = input("New name: ")
    dob = input("New date of birth (YYYY-MM-DD): ")
    contact = input("New contact details: ")
    status = input("New status (admitted/cancelled/InProgress): ")

    cur.execute("""
        UPDATE Student
        SET name=?, dob=?, contact_details=?, status=?
        WHERE StudentID=?
    """, (name, dob, contact, status, sid))
    con.commit()
    print("Student updated." if cur.rowcount else "Student not found.")


def search_student():
    name = input("Enter student name: ")
    cur.execute("SELECT * FROM Student WHERE name LIKE ?", ('%' + name + '%',))
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No student found.")


while True:
    print("""
1. Add student
2. Update student
3. Search student by name
4. Exit
""")
    choice = input("Choice: ")

    try:
        if choice == "1":
            add_student()
        elif choice == "2":
            update_student()
        elif choice == "3":
            search_student()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
    except (sqlite3.IntegrityError, ValueError) as e:
        print("Error:", e)

con.close()
