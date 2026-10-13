import sqlite3

con = sqlite3.connect("Customer.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    CustomerId INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Address TEXT,
    contact TEXT,
    username TEXT UNIQUE,
    password TEXT
)
""")
con.commit()


def add_customer():
    data = (
        int(input("Customer ID: ")),
        input("Name: "),
        input("Address: "),
        input("Contact: "),
        input("Username: "),
        input("Password: ")
    )
    cur.execute("INSERT INTO Customer VALUES (?, ?, ?, ?, ?, ?)", data)
    con.commit()
    print("Customer added.")


def update_customer():
    cid = int(input("Customer ID: "))
    name = input("New name: ")
    address = input("New address: ")
    contact = input("New contact: ")
    username = input("New username: ")
    password = input("New password: ")

    cur.execute("""
        UPDATE Customer
        SET Name=?, Address=?, contact=?, username=?, password=?
        WHERE CustomerId=?
    """, (name, address, contact, username, password, cid))
    con.commit()
    print("Customer updated." if cur.rowcount else "Customer not found.")


def display_customers():
    cur.execute("""
        SELECT CustomerId, Name, Address, contact, username
        FROM Customer
    """)
    rows = cur.fetchall()
    if not rows:
        print("No customers found.")
    for row in rows:
        print(row)


while True:
    print("""
1. Add customer
2. Update customer
3. Display customers
4. Exit
""")
    choice = input("Choice: ")

    try:
        if choice == "1":
            add_customer()
        elif choice == "2":
            update_customer()
        elif choice == "3":
            display_customers()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")
    except (sqlite3.IntegrityError, ValueError) as e:
        print("Error:", e)

con.close()
