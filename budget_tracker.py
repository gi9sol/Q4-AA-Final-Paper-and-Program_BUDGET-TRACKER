import json

MAX_ATTEMPTS = 3

# Start EMPTY (no default users)
stored_users = {}

weekly_allowance = 0

categories = {
    "cafeteria": 0,
    "co-op": 0,
    "projects": 0,
    "savings": 0
}

transactions = []

# ===== SAFE INPUT =====
def safe_input(prompt):
    try:
        return input(prompt)
    except EOFError:
        print("\nInput error detected.")
        exit()

# ===== SAVE / LOAD DATA =====
def save_data():
    data = {
        "users": stored_users,
        "categories": categories,
        "transactions": transactions
    }
    with open("data.json", "w") as file:
        json.dump(data, file)

def load_data():
    global stored_users, categories, transactions
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            stored_users = data.get("users", {})
            categories = data.get("categories", categories)
            transactions = data.get("transactions", [])
    except:
        pass

# ===== ACCOUNT SYSTEM =====
def create_account():
    print("\n===== CREATE ACCOUNT =====")

    username = safe_input("New username: ")
    password = safe_input("New password: ")

    if username in stored_users:
        print("Username already exists.")
    else:
        stored_users.update({username: password})   # ✅ FIXED
        save_data()
        print("Account created. You can now log in.")

def login():
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        print("\n===== BUDGET TRACKER LOGIN =====")
        print("1 - Login")
        print("2 - Create Account")

        choice = safe_input("Select option: ")

        if choice == "2":
            create_account()
            continue

        if len(stored_users) == 0:
            print("No accounts yet. Please create one first.")
            continue

        username = safe_input("Enter username: ").strip()
        password = safe_input("Enter password: ").strip()

        if username not in stored_users:
            attempts += 1
            print("Username not found.")
            continue

        if stored_users[username] != password:
            attempts += 1
            print("Incorrect password.")
            continue

        print("Login successful!")
        return True

    print("Too many attempts.")
    return False

# ===== BUDGET SETUP =====
def setup_budget():
    global weekly_allowance

    print("\n===== WEEKLY ALLOWANCE =====")

    while True:
        try:
            weekly_allowance = float(safe_input("Enter weekly allowance: "))
            break
        except:
            print("Enter a valid number.")

# ===== CATEGORY =====
def add_category():
    name = safe_input("Category name: ").lower()

    if name in categories:
        print("Already exists.")
        return

    categories[name] = 0
    save_data()
    print("Added.")

def remove_category():
    name = safe_input("Category name: ").lower()

    if name not in categories:
        print("Not found.")
        return

    del categories[name]
    save_data()
    print("Removed.")

# ===== EXPENSE =====
def add_expense():
    print("\nCategories:")
    for c in categories:
        print("-", c)

    category = safe_input("Choose category: ").lower()

    if category not in categories:
        print("Not found.")
        return

    try:
        amount = float(safe_input("Amount: "))
    except:
        print("Invalid.")
        return

    categories[category] -= amount
    transactions.append((category, amount))
    save_data()

    print("Recorded.")

# ===== DELETE EXPENSE =====
def delete_expense():
    if len(transactions) == 0:
        print("No transactions.")
        return

    for i, t in enumerate(transactions):
        print(f"{i+1}. {t[0]} - {t[1]}")

    try:
        choice = int(safe_input("Pick number: ")) - 1
    except:
        print("Invalid.")
        return

    if 0 <= choice < len(transactions):
        category, amount = transactions.pop(choice)
        categories[category] += amount
        save_data()
        print("Deleted.")
    else:
        print("Invalid.")

# ===== BALANCE =====
def view_balance():
    for c in categories:
        print(c, ":", categories[c])

# ===== SAVINGS =====
def savings_tracker():
    if "savings" in categories:
        print("Savings:", categories["savings"])
    else:
        print("No savings category.")

# ===== SUMMARY =====
def balance_summary():
    total = 0
    for c in categories:
        total += categories[c]
    print("Remaining:", total)

# ===== ANALYSIS =====
def spending_analysis():
    analysis = {}

    for t in transactions:
        category, amount = t

        if category not in analysis:
            analysis[category] = 0   

        analysis[category] += amount

    for c in analysis:
        print(c, "spent:", analysis[c])

    if len(analysis) > 0:
        top = max(analysis, key=analysis.get)   
        print("Top spending:", top)

# ===== LOG =====
def trans_log():
    if len(transactions) == 0:
        print("No transactions.")
        return

    for i, t in enumerate(transactions):
        print(f"{i+1}. {t[0]} - {t[1]}")

# ===== RESET =====
def reset_week():
    for c in categories:
        categories[c] = 0

    transactions.clear()
    save_data()

    print("Reset complete.")

# ===== DASHBOARD =====
def dashboard():
    while True:
        print("\n===== DASHBOARD =====")
        print("1 Add Expense")
        print("2 View Balance")
        print("3 Savings")
        print("4 Summary")
        print("5 Analysis")
        print("6 Log")
        print("7 Delete Expense")
        print("8 Add Category")
        print("9 Remove Category")
        print("10 Reset")
        print("11 Logout")

        try:
            choice = int(safe_input("Choice: "))
        except:
            print("Invalid.")
            continue

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_balance()
        elif choice == 3:
            savings_tracker()
        elif choice == 4:
            balance_summary()
        elif choice == 5:
            spending_analysis()
        elif choice == 6:
            trans_log()
        elif choice == 7:
            delete_expense()
        elif choice == 8:
            add_category()
        elif choice == 9:
            remove_category()
        elif choice == 10:
            reset_week()
        elif choice == 11:
            break

# ===== MAIN =====
def main():
    load_data()   
    if login():
        setup_budget()
        dashboard()

main()
