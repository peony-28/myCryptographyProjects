import psycopg2
import cryptography
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from dotenv import load_dotenv
import os

load_dotenv()
# Encryption and decryption functions
def encrypt_data(plaintext, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return nonce + ciphertext

def decrypt_data(encrypted_data, key):
    aesgcm = AESGCM(key)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]

# Password hashing function
def hash_password(password):
    digest = hashes.Hash(hashes.SHA256())
    digest.update(password.encode())
    return digest.finalize()

# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

# Encryption key (should be kept secret and secure)
encryption_key = os.getenv('ENCRYPTION_KEY').encode()

# Function to authenticate user
def authenticate_user(username, password):
    hashed_password = hash_password(password)

    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT role
                FROM "User"
                WHERE username = %s AND password_hash = %s
                """,
                (username, hashed_password)
            )
            user = cur.fetchone()
            if user:
                return user[0]
            else:
                return None

# Function to register new user
def register_user(username, password, role):
    hashed_password = hash_password(password)

    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO "User" (username, password_hash, role)
                VALUES (%s, %s, %s)
                """,
                (username, hashed_password, role)
            )
            conn.commit()
            return True

# Function to manage users (Admin Dashboard)
def manage_users():
    print("Manage Users:")
    print("1. View All Users")
    print("2. Add User")
    print("3. Delete User")
    print("4. Go Back")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        view_all_users()
    elif choice == '2':
        add_user()
    elif choice == '3':
        delete_user()
    elif choice == '4':
        admin_dashboard()
    else:
        print("Invalid choice.")

def view_all_users():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve all users from the database
        cur.execute("SELECT * FROM \"User\"")
        users = cur.fetchall()

        # Display users
        print("All Users:")
        for user in users:
            print(user)

    except psycopg2.Error as e:
        print("Error fetching users:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

def add_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin, customer, or merchant): ").lower()

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Insert new user into the database
        cur.execute("INSERT INTO \"User\" (username, password_hash, role) VALUES (%s, %s, %s)", (username, password, role))
        conn.commit()
        print("User added successfully.")

    except psycopg2.Error as e:
        print("Error adding user:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

def delete_user():
    username = input("Enter username to delete: ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Delete user from the database
        cur.execute("DELETE FROM \"User\" WHERE username = %s", (username,))
        conn.commit()
        print("User deleted successfully.")

    except psycopg2.Error as e:
        print("Error deleting user:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to view credit card information (Admin Dashboard)
def view_credit_card_info():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve credit card information from the database
        cur.execute("SELECT * FROM credit_card")
        credit_card = cur.fetchall()

        # Display credit card information
        print("Credit Card Information:")
        for card in credit_card:
            print(card)

    except psycopg2.Error as e:
        print("Error fetching credit card information:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to manage roles and privileges (Admin Dashboard)
def manage_roles_privileges():
    print("Manage Roles and Privileges:")
    print("1. Assign Role to User")
    print("2. Modify Privileges")
    print("3. Go Back")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        assign_role()
    elif choice == '2':
        modify_privileges()
    elif choice == '3':
        admin_dashboard()
    else:
        print("Invalid choice.")

def assign_role():
    username = input("Enter username: ")
    role = input("Enter role (admin, customer, or merchant): ").lower()

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Update user's role in the database
        cur.execute("UPDATE \"User\" SET role = %s WHERE username = %s", (role, username))
        conn.commit()
        print("Role assigned successfully.")

    except psycopg2.Error as e:
        print("Error assigning role:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

def modify_privileges():
    print("Modify Privileges functionality under construction.")

# Function to view system logs (Admin Dashboard)
def view_system_logs():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve system logs from the database
        cur.execute("SELECT * FROM system_logs")
        logs = cur.fetchall()

        # Display system logs
        print("System Logs:")
        for log in logs:
            print(log)

    except psycopg2.Error as e:
        print("Error fetching system logs:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Customer dashboard functions
# Function to add a credit card (Customer Dashboard)
def add_credit_card():
    customer_id = input("Enter customer ID: ")
    card_number = input("Enter card number: ")
    cvv = input("Enter CVV: ")
    expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
    # Validate card number length (assuming it should be 16 digits)
    if len(card_number) != 16:
        print("Invalid card number length. It should be 16 digits.")
        return

    # Validate CVV length (assuming it should be 3 digits)
    if len(cvv) != 3:
        print("Invalid CVV length. It should be 3 digits.")
        return

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Encrypt credit card information
        encrypted_number = encrypt_data(card_number, encryption_key)
        encrypted_cvv = encrypt_data(cvv, encryption_key)

        # Insert credit card into the database
        cur.execute(
            """
            INSERT INTO credit_card (customer_id, encrypted_number, encrypted_cvv, expiration_date)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_id, encrypted_number, encrypted_cvv, expiration_date)
        )
        conn.commit()
        print("Credit card added successfully.")

    except psycopg2.Error as e:
        print("Error adding credit card:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to view stored credit cards (Customer Dashboard)
def view_stored_credit_card():
    customer_id = input("Enter customer ID: ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve credit cards for the customer from the database
        cur.execute("SELECT * FROM credit_card WHERE customer_id = %s", (customer_id,))
        credit_card = cur.fetchall()

        # Display credit card information
        print("Stored Credit Cards:")
        for card in credit_card:
            card_id, customer_id, encrypted_number, encrypted_cvv, expiration_date = card
            card_number = decrypt_data(encrypted_number, encryption_key)
            cvv = decrypt_data(encrypted_cvv, encryption_key)
            print(f"Card ID: {card_id}, Card Number: {card_number}, CVV: {cvv}, Expiration Date: {expiration_date}")

    except psycopg2.Error as e:
        print("Error fetching credit cards:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to edit or remove credit cards (Customer Dashboard)
def edit_or_remove_credit_card():
    print("Edit or Remove Credit Cards:")
    print("1. Edit Credit Card")
    print("2. Remove Credit Card")
    print("3. Go Back")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        edit_credit_card()
    elif choice == '2':
        remove_credit_card()
    elif choice == '3':
        customer_dashboard()
    else:
        print("Invalid choice.")

# Function to edit a credit card (Customer Dashboard)
def edit_credit_card():
    card_id = input("Enter card ID to edit: ")
    card_number = input("Enter new card number: ")
    cvv = input("Enter new CVV: ")
    expiration_date = input("Enter new expiration date (YYYY-MM-DD): ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Encrypt credit card information
        encrypted_number = encrypt_data(card_number, encryption_key)
        encrypted_cvv = encrypt_data(cvv, encryption_key)

        # Update credit card in the database
        cur.execute(
            """
            UPDATE credit_card
            SET encrypted_number = %s, encrypted_cvv = %s, expiration_date = %s
            WHERE card_id = %s
            """,
            (encrypted_number, encrypted_cvv, expiration_date, card_id)
        )
        conn.commit()
        print("Credit card updated successfully.")

    except psycopg2.Error as e:
        print("Error updating credit card:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to remove a credit card (Customer Dashboard)
def remove_credit_card():
    card_id = input("Enter card ID to remove: ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Delete credit card from the database
        cur.execute("DELETE FROM credit_card WHERE card_id = %s", (card_id,))
        conn.commit()
        print("Credit card removed successfully.")

    except psycopg2.Error as e:
        print("Error removing credit card:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to view customer credit cards (Merchant Dashboard)
def view_customer_credit_card():
    customer_id = input("Enter customer ID: ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve credit cards for the customer from the database
        cur.execute("SELECT * FROM credit_card WHERE customer_id = %s", (customer_id,))
        credit_card = cur.fetchall()

        # Display credit card information
        print("Customer Credit Cards:")
        for card in credit_card:
            card_id, customer_id, encrypted_number, encrypted_cvv, expiration_date = card
            card_number = decrypt_data(encrypted_number, encryption_key)
            cvv = decrypt_data(encrypted_cvv, encryption_key)
            print(f"Card ID: {card_id}, Card Number: {card_number}, CVV: {cvv}, Expiration Date: {expiration_date}")

    except psycopg2.Error as e:
        print("Error fetching customer credit cards:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to process transactions (Merchant Dashboard)
def process_transactions():
    card_id = input("Enter card ID: ")
    amount = float(input("Enter transaction amount: "))

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Insert transaction into the database
        cur.execute(
            """
            INSERT INTO transactions (credit_card_id, amount)
            VALUES (%s, %s)
            """,
            (card_id, amount)
        )
        conn.commit()
        print("Transaction processed successfully.")

    except psycopg2.Error as e:
        print("Error processing transaction:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Function to view transaction history for merchants (Merchant Dashboard)
def transaction_history_merchant():
    merchant_id = input("Enter merchant ID: ")

    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Retrieve transaction history for the merchant from the database
        cur.execute(
            """
            SELECT t.transaction_id, t.credit_card_id, c.customer_id, t.amount
            FROM transactions t
            INNER JOIN credit_card c ON t.credit_card_id = c.card_id
            WHERE c.merchant_id = %s
            """,
            (merchant_id,)
        )
        transactions = cur.fetchall()

        # Display transaction history
        print("Transaction History:")
        for transaction in transactions:
            print(transaction)

    except psycopg2.Error as e:
        print("Error fetching transaction history:", e)

    finally:
        # Close the connection
        if conn is not None:
            conn.close()

# Main function for admin dashboard
def admin_dashboard():
    print("Admin Dashboard:")
    print("1. Manage Users")
    print("2. View Credit Card Information")
    print("3. Manage Roles and Privileges")
    print("4. View System Logs")
    print("5. Log Out")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        manage_users()
    elif choice == '2':
        view_credit_card_info()
    elif choice == '3':
        manage_roles_privileges()
    elif choice == '4':
        view_system_logs()
    elif choice == '5':
        print("Logged out.")
        return
    else:
        print("Invalid choice.")
        admin_dashboard()

# Main function for customer dashboard
def customer_dashboard():
    print("Customer Dashboard:")
    print("1. Add Credit Card")
    print("2. View Stored Credit Cards")
    print("3. Edit or Remove Credit Cards")
    print("4. Log Out")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        add_credit_card()
    elif choice == '2':
        view_stored_credit_card()
    elif choice == '3':
        edit_or_remove_credit_card()
    elif choice == '4':
        print("Logged out.")
        return
    else:
        print("Invalid choice.")
        customer_dashboard()

# Main function for merchant dashboard
def merchant_dashboard():
    print("Merchant Dashboard:")
    print("1. View Customer Credit Cards")
    print("2. Process Transactions")
    print("3. Transaction History")
    print("4. Log Out")
    choice = input("Enter your choice: ").strip()
    if choice == '1':
        view_customer_credit_card()
    elif choice == '2':
        process_transactions()
    elif choice == '3':
        transaction_history_merchant()
    elif choice == '4':
        print("Logged out.")
        return
    else:
        print("Invalid choice.")
        merchant_dashboard()

# Main function for the login system
def main():
    while True:
        print("Welcome to the Credit Card Management System!")
        print("1. Log In")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = authenticate_user(username, password)
            if role == 'admin':
                admin_dashboard()
            elif role == 'customer':
                customer_dashboard()
            elif role == 'merchant':
                merchant_dashboard()
            else:
                print("Invalid username or password.")
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (admin, customer, or merchant): ").lower()
            if role in ['admin', 'customer', 'merchant']:
                if register_user(username, password, role):
                    print("Registration successful. Please log in.")
                else:
                    print("Registration failed.")
            else:
                print("Invalid role.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
