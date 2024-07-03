import sqlite3
# Expense Tracker - My first-ever project using SQL and Python


# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    print(f"Connected to database {db_file}")
    return conn


# Function to create tables if they do not already exist
def create_tables(conn):
    cursor = conn.cursor()
    create_categories_table = """
    CREATE TABLE IF NOT EXISTS Categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """
    create_expenses_table = """
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category_id INTEGER,
        description TEXT,
        FOREIGN KEY (category_id) REFERENCES Categories (id)
    );
    """
    cursor.execute(create_categories_table)
    cursor.execute(create_expenses_table)
    conn.commit()


# Function to add a new expense to the Expenses table
def add_expense(conn, amount, date, category_id, description):
    cursor = conn.cursor()
    insert_expense = """
    INSERT INTO Expenses (amount, date, category_id, description) VALUES (?,?,?,?);
    """
    cursor.execute(insert_expense, (amount, date, category_id, description))
    conn.commit()


# Function to add a new category to the Categories table
def add_category(conn, category_name):
    cursor = conn.cursor()
    insert_category = """
    INSERT INTO Categories (name) VALUES (?);
    """
    cursor.execute(insert_category, (category_name,))
    conn.commit()


# Function to delete an expense by ID
def delete_expense(conn, expense_id):
    cursor = conn.cursor()
    delete_query = "DELETE FROM Expenses WHERE id = ?"
    cursor.execute(delete_query, (expense_id,))
    conn.commit()
    print(f"Deleted expense with ID {expense_id}")


# Function to delete a category by ID
def delete_category(conn, category_id):
    cursor = conn.cursor()
    delete_expenses_query = "DELETE FROM Expenses WHERE category_id = ?"
    delete_category_query = "DELETE FROM Categories WHERE id = ?"
    cursor.execute(delete_expenses_query, (category_id,))
    cursor.execute(delete_category_query, (category_id,))
    conn.commit()
    print(f"Deleted category with ID {category_id} and associated expenses")


# Function to create some default categories
def initialize_categories(conn):
    cursor = conn.cursor()
    initial_categories = ["🥗 Food", "✈️ Transport", "🎧 Entertainment", "🛠️ Utilities", "🏥 Health"]

    for category in initial_categories:
        cursor.execute("SELECT id FROM Categories WHERE name = ?", (category,))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO Categories (name) VALUES (?)", (category,))
            conn.commit()


# Function to display all categories
def display_categories(conn):
    cursor = conn.cursor()
    view_category_query = """
    SELECT id, name FROM Categories
    """
    cursor.execute(view_category_query)
    print('Available Categories')
    categories = cursor.fetchall()
    for category in categories:
        print(f"ID: {category[0]}, Category Name: {category[1]}")


# Function to view all expenses
def view_expenses(conn):
    cursor = conn.cursor()
    view_query = """
    SELECT e.id, e.amount, e.date, c.name as category, e.description
    FROM Expenses e
    LEFT JOIN Categories c ON e.category_id = c.id
    """
    cursor.execute(view_query)
    view_all = cursor.fetchall()
    for row in view_all:
        print(f"ID: {row[0]}, Amount: {row[1]}, Date: {row[2]}, Category: {row[3]}, Description: {row[4]}")


# Function to summarize expenses by category
def summarize_expenses_by_category(conn):
    cursor = conn.cursor()
    group_query = """
    SELECT c.name, SUM(e.amount)
    FROM Expenses e
    LEFT JOIN Categories c ON c.id = e.category_id
    GROUP BY c.name
    """
    cursor.execute(group_query)
    result = cursor.fetchall()
    for row in result:
        print(
            f"Category: {row[0]}, Total Expense: {row[1]}"
        )


# Main function to run the command-line interface
def main():
    user_input = 0
    database = "expenses.db"
    conn = create_connection(database)
    create_tables(conn)
    initialize_categories(conn)
    while True:
        print("""
---------------------------------   
Menu:
1. Add a new expense
2. Add a new category
3. Delete an expense
4. Delete a category
5. View all expenses
6. View all categories
7. Summarize expenses by category
8. Exit
---------------------------------
        """)
        try:
            user_input = int(input('Choose an option: '))
        except ValueError as e:
            print(f'Error: {e}. Please type a number.')

        if user_input == 8:
            sure = input("Are you sure about that? (Y/N): ")
            if sure.upper() == 'Y':
                print("Thank you for using the service")
                conn.close()
                break
            else:
                continue
        elif user_input == 1:
            try:
                amount = float(input("Amount Spent: $"))
                date = input("Date (YYYY-MM-DD): ")
                display_categories(conn)
                category_id = int(input("Category ID: "))
                description = input("Description: ")
                add_expense(conn, amount, date, category_id, description)
                print("Process executed successfully!")
            except ValueError as e:
                print(f"Error: {e}. Please enter valid inputs.")
        elif user_input == 2:
            category_name = input("Category (with an icon): ")
            add_category(conn, category_name)
            print('Category added successfully!')
        elif user_input == 3:
            try:
                expense_id = int(input("Enter the ID of the expense to delete: "))
                delete_expense(conn, expense_id)
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid expense ID.")
        elif user_input == 4:
            try:
                category_id = int(input("Enter the ID of the category to delete: "))
                delete_category(conn, category_id)
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid category ID.")
        elif user_input == 5:
            view_expenses(conn)
        elif user_input == 6:
            display_categories(conn)
        elif user_input == 7:
            summarize_expenses_by_category(conn)
        else:
            print("Invalid option. Please choose a number from 1 to 8.")


if __name__ == "__main__":
    main()
