
import json
from pathlib import Path
from datetime import date

DATA_FILE = Path(__file__).with_name("transactions.json")


def load_transactions():
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            print("Warning: Could not read transaction file.")
    return []


def save_transactions(transactions):
    DATA_FILE.write_text(
        json.dumps(transactions, indent=4),
        encoding="utf-8"
    )


def get_amount():
    try:
        amount = float(input("Enter amount (₹): "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return None
        return round(amount, 2)
    except ValueError:
        print("Please enter a valid amount.")
        return None


def add_transaction(transactions, kind):
    amount = get_amount()
    if amount is None:
        return

    category = input("Enter category: ").strip()
    note = input("Enter description: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    transaction = {
        "type": kind,
        "amount": amount,
        "category": category,
        "description": note,
        "date": date.today().isoformat()
    }

    transactions.append(transaction)
    save_transactions(transactions)
    print("Transaction saved successfully!")


def view_transactions(transactions):
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n--- Transaction History ---")
    for index, item in enumerate(transactions, start=1):
        print(
            f"{index}. {item['date']} | "
            f"{item['type'].upper()} | "
            f"₹{item['amount']:.2f} | "
            f"{item['category']} | "
            f"{item['description']}"
        )


def show_summary(transactions):
    income = sum(
        t["amount"] for t in transactions
        if t["type"] == "income"
    )
    expenses = sum(
        t["amount"] for t in transactions
        if t["type"] == "expense"
    )

    print("\n--- Financial Summary ---")
    print(f"Total income:   ₹{income:.2f}")
    print(f"Total expenses: ₹{expenses:.2f}")
    print(f"Balance:        ₹{income - expenses:.2f}")


def delete_transaction(transactions):
    view_transactions(transactions)
    if not transactions:
        return

    try:
        number = int(input("Enter transaction number to delete: "))
        if 1 <= number <= len(transactions):
            removed = transactions.pop(number - 1)
            save_transactions(transactions)
            print("Deleted:", removed["category"])
        else:
            print("Invalid transaction number.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    transactions = load_transactions()

    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add income")
        print("2. Add expense")
        print("3. View transactions")
        print("4. Financial summary")
        print("5. Delete transaction")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_transaction(transactions, "income")
        elif choice == "2":
            add_transaction(transactions, "expense")
        elif choice == "3":
            view_transactions(transactions)
        elif choice == "4":
            show_summary(transactions)
        elif choice == "5":
            delete_transaction(transactions)
        elif choice == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
