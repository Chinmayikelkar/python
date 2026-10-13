import sqlite3

con = sqlite3.connect("Library.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")

cur.execute("""
CREATE TABLE IF NOT EXISTS Member (
    MemberId INTEGER PRIMARY KEY,
    MName TEXT NOT NULL,
    Email TEXT,
    Address TEXT,
    PhoneNo TEXT,
    MembershipDate TEXT,
    ExpiryDate TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Book (
    BookId INTEGER PRIMARY KEY,
    BookName TEXT NOT NULL,
    AuthorName TEXT,
    PublicationYear INTEGER,
    Price REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS Transactions (
    TransactionId INTEGER PRIMARY KEY,
    BookId INTEGER,
    MemberID INTEGER,
    IssueDate TEXT,
    DueDate TEXT,
    ReturnDate TEXT,
    FinalAmount REAL,
    Status TEXT CHECK (
        Status IN ('Issued', 'Returned', 'Overdue', 'Reserved')
    ),
    FOREIGN KEY (BookId) REFERENCES Book(BookId),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberId)
)
""")
con.commit()


def add_member():
    data = (
        int(input("Member ID: ")),
        input("Name: "),
        input("Email: "),
        input("Address: "),
        input("Phone: "),
        input("Membership date (YYYY-MM-DD): "),
        input("Expiry date (YYYY-MM-DD): ")
    )
    cur.execute("INSERT INTO Member VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()
    print("Member added.")


def display_members():
    cur.execute("SELECT * FROM Member")
    rows = cur.fetchall()
    if not rows:
        print("No members found.")
    for row in rows:
        print(row)


def update_member():
    member_id = int(input("Member ID to update: "))
    name = input("New name: ")
    email = input("New email: ")
    address = input("New address: ")
    phone = input("New phone: ")
    membership_date = input("New membership date (YYYY-MM-DD): ")
    expiry_date = input("New expiry date (YYYY-MM-DD): ")

    cur.execute("""
        UPDATE Member
        SET MName=?, Email=?, Address=?, PhoneNo=?,
            MembershipDate=?, ExpiryDate=?
        WHERE MemberId=?
    """, (name, email, address, phone, membership_date, expiry_date, member_id))
    con.commit()
    print("Member updated." if cur.rowcount else "Member not found.")


def delete_member():
    member_id = int(input("Member ID to delete: "))
    cur.execute("DELETE FROM Member WHERE MemberId=?", (member_id,))
    con.commit()
    print("Member deleted." if cur.rowcount else "Member not found.")


while True:
    print("""
1. Add member
2. Display members
3. Update member
4. Delete member
5. Exit
""")
    choice = input("Choice: ")

    try:
        if choice == "1":
            add_member()
        elif choice == "2":
            display_members()
        elif choice == "3":
            update_member()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")
    except (sqlite3.IntegrityError, ValueError) as e:
        print("Error:", e)

con.close()
