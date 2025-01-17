import sqlite3
import random
import string

# Connect to the SQLite database
conn = sqlite3.connect('alpha.db') #123456788496 9876  123456786884 1234
cursor = conn.cursor()
# cursor.execute("CREATE TABLE users (account_number TEXT PRIMARY KEY, name TEXT,phone TEXT,email TEXT,balance REAL DEFAULT 0,pin TEXT)")


# Function to generate a 12-digit account number
def generate_account_number():
    base_account_number = "123456789012"  # Example base number (12 digits)
    random_last_digit = str(random.randint(1000, 9999))  # Random 4 digits
    account_number = base_account_number[:-4] + random_last_digit  # Replace last 4 digits
    return account_number

# Function to convert pin to alphabet format (using ord)
def pin_to_alphabet(pin):
    return ''.join([chr(int(digit) + 65) for digit in pin])

# Function to create a new user
def create_user():
    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    email = input("Enter your email address: ")
    account_number = generate_account_number()
    balance = 0  # Initial balance is 0
    pin = None  # Initial pin is None

    # Insert user into the database
    cursor.execute("""
        INSERT INTO users (account_number, name, phone, email, balance, pin)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (account_number, name, phone, email, balance, pin))
    conn.commit()

    print(f"Account created successfully. Your account number is: {account_number}")
    return account_number

# Function to validate pin
def validate_pin(account_number, entered_pin):
    cursor.execute("SELECT pin FROM users WHERE account_number = ?", (account_number,))
    stored_pin = cursor.fetchone()
    if stored_pin:
        stored_pin = stored_pin[0]
        return stored_pin == pin_to_alphabet(entered_pin)
    return False

# Function for PIN generation
def generate_pin(account_number):
    pin = input("Enter a 4-digit PIN to set: ")
    if len(pin) == 4 and pin.isdigit():
        alphabet_pin = pin_to_alphabet(pin)
        cursor.execute("""
            UPDATE users SET pin = ? WHERE account_number = ?
        """, (alphabet_pin, account_number))
        conn.commit()
        print("PIN set successfully.")
    else:
        print("Invalid PIN. Please enter a 4-digit number.")

# Function for withdrawal
def withdraw(account_number):
    pin = input("Enter your 4-digit PIN: ")
    if not validate_pin(account_number, pin):
        print("Invalid PIN. Withdrawal failed.")
        return
    amount = float(input("Enter the amount to withdraw: "))
    cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
    current_balance = cursor.fetchone()[0]
    if current_balance >= amount:
        new_balance = current_balance - amount
        cursor.execute("""
            UPDATE users SET balance = ? WHERE account_number = ?
        """, (new_balance, account_number))
        conn.commit()
        print(f"Withdrawal successful. New balance: {new_balance}")
    else:
        print("Insufficient balance.")

# Function for deposit
def deposit(account_number):
    pin = input("Enter your 4-digit PIN: ")
    if not validate_pin(account_number, pin):
        print("Invalid PIN. Deposit failed.")
        return
    amount = float(input("Enter the amount to deposit: "))
    cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
    current_balance = cursor.fetchone()[0]
    new_balance = current_balance + amount
    cursor.execute("""
        UPDATE users SET balance = ? WHERE account_number = ?
    """, (new_balance, account_number))
    conn.commit()
    print(f"Deposit successful. New balance: {new_balance}")

# Function for account transfer
def transfer(account_number):
    print("1. Pay to account holder")
    print("2. Pay to mobile number")
    option = input("Choose an option: ")
    
    if option == '1':
        account_to = input("Enter the account number to transfer to: ")
        amount = float(input("Enter the amount to transfer: "))
        pin = input("Enter your 4-digit PIN: ")
        if not validate_pin(account_number, pin):
            print("Invalid PIN. Transfer failed.")
            return
        cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_number,))
        current_balance = cursor.fetchone()[0]
        if current_balance >= amount:
            new_balance = current_balance - amount
            cursor.execute("""
                UPDATE users SET balance = ? WHERE account_number = ?
            """, (new_balance, account_number))
            cursor.execute("SELECT balance FROM users WHERE account_number = ?", (account_to,))
            recipient_balance = cursor.fetchone()[0]
            recipient_new_balance = recipient_balance + amount
            cursor.execute("""
                UPDATE users SET balance = ? WHERE account_number = ?
            """, (recipient_new_balance, account_to))
            conn.commit()
            print(f"Transfer successful. Your new balance: {new_balance}")
        else:
            print("Insufficient balance.")
    elif option == '2':
        phone_number = input("Enter the mobile number to transfer to: ")
        amount = float(input("Enter the amount to transfer: "))
        pin = input("Enter your 4-digit PIN: ")
        if not validate_pin(account_number, pin):
            print("Invalid PIN. Transfer failed.")
            return
        # Implement logic for mobile transfer (similar to account transfer)
    else:
        print("Invalid option.")

# Main menu
def main():
    print("Welcome to Alpha Bank!")
    print("1. New Account")
    print("2. Existing Account")
    
    account_number = None
    
    # Ask if the user wants a new account or an existing one
    account_choice = input("Choose an option (1 for New Account, 2 for Existing Account): ")
    
    if account_choice == '1':  # New account creation
        account_number = create_user()
    elif account_choice == '2':  # Existing account
        account_number = input("Enter your account number: ")
        pin = input("Enter your 4-digit PIN: ")
        if not validate_pin(account_number, pin):
            print("Invalid PIN. Access denied.")
            return
        print("Account verified successfully.")
    else:
        print("Invalid option. Exiting.")
        return

    # Menu for the existing or new account
    while True:
        print("\n1. Withdraw Amount")
        print("2. Deposit Amount")
        print("3. Transfer Money")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            withdraw(account_number)
        elif choice == '2':
            deposit(account_number)
        elif choice == '3':
            transfer(account_number)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")

# Run the program
if __name__ == "__main__":
    main()

 
