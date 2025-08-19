import json
import os
from datetime import datetime
import matplotlib.pyplot as plt


class FinanceTracker:
    def __init__(self, filename="transactions.json"):
        self.transactions = []
        self.filename = filename
        self.load_data()

    #Add transaction
    def add_transaction(self, date, t_type, amount, category, note=""):
        transaction = {
            "date": date,
            "type": t_type,
            "amount": amount,
            "category": category,
            "note": note
        }
        self.transactions.append(transaction)
        self.save_data()
        print(f"Transaction added: {t_type} of ${amount} on {date}")

    #transactions display
    def display_transactions(self):
        if not self.transactions:
            print("No Transactions Found.")
            return
        print("\nAll Transactions")
        print("-" * 70)
        for t in self.transactions:
            print(f"{t['date']} | {t['type']} | ${t['amount']} | {t['category']} | {t['note']}")
        print("-" * 70)

    #Search transactions
    def search_transactions(self, keyword):
        keyword = keyword.lower()
        results = [t for t in self.transactions if keyword in t['category'].lower() or keyword in t['note'].lower()]
        if not results:
            print("No Matching Transactions.")
            return
        print(f"\nSearch Results for '{keyword}':")
        for t in results:
            print(f"{t['date']} | {t['type']} | ${t['amount']} | {t['category']} | {t['note']}")

    # Filter expenses above a limit
    def filter_expenses(self, min_amount=100):
        results = [t for t in self.transactions if t['type'].lower() == "expense" and t['amount'] >= min_amount]
        if not results:
            print(f"No Expenses over ${min_amount}.")
            return
        print(f"\n Expenses over ${min_amount}:")
        for t in results:
            print(f"{t['date']} | ${t['amount']} | {t['category']} | {t['note']}")

    # Sort transactions
    def sort_transactions(self, by="amount"):
        if by == "amount":
            self.transactions.sort(key=lambda x: x['amount'])
        elif by == "date":
            self.transactions.sort(key=lambda x: x['date'])
        else:
            print(" Invalid sort key.")
            return
        print(f"\nTransactions sorted by {by}:")
        self.display_transactions()

    # monthly Spending Bar Chart
    def monthly_spending_chart(self):
        spending = {}
        for t in self.transactions:
            if t['type'].lower() == "expense":
                month = t['date'][:7]
                spending[month] = spending.get(month, 0) + t['amount']

        if not spending:
            print("No expenses to show in chart")
            return

        months = list(spending.keys())
        totals = list(spending.values())

        plt.figure(figsize=(8, 5))
        plt.bar(months, totals, color="skyblue", edgecolor="black")
        plt.title("Monthly Spending Chart")
        plt.xlabel("Month (YYYY-MM)")
        plt.ylabel("Total Expenses ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Category-wise Spending Pie Chart
    def category_pie_chart(self):
        categories = {}
        for t in self.transactions:
            if t['type'].lower() == "expense":
                categories[t['category']] = categories.get(t['category'], 0) + t['amount']

        if not categories:
            print("No expenses to show in chart")
            return

        labels = list(categories.keys())
        sizes = list(categories.values())

        plt.figure(figsize=(7, 7))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Expenses by Category")
        plt.show()

    #Savedata
    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump(self.transactions, f, indent=4)

    # loaddata
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.transactions = json.load(f)
                except json.JSONDecodeError:
                    self.transactions = []
        else:
            self.transactions = []

# menu
def main():
    tracker = FinanceTracker()

    while True:
        print("\n====== Personal Finance Tracker ======")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Search Transactions")
        print("4. Filter Expenses Over $100")
        print("5. Sort Transactions")
        print("6. Monthly Spending Bar Chart")
        print("7. Category-wise Spending Pie Chart")
        print("8. Exit")
        choice = input("Enter Choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            t_type = input("Enter type (Income/Expense): ")
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            category = input("Enter category (Food, Salary, etc.): ")
            note = input("Enter note: ")
            tracker.add_transaction(date, t_type, amount, category, note)

        elif choice == "2":
            tracker.display_transactions()

        elif choice == "3":
            keyword = input("Enter keyword (category/note): ")
            tracker.search_transactions(keyword)

        elif choice == "4":
            tracker.filter_expenses(100)

        elif choice == "5":
            sort_by = input("Sort by (amount/date): ")
            tracker.sort_transactions(sort_by)

        elif choice == "6":
            tracker.monthly_spending_chart()

        elif choice == "7":
            tracker.category_pie_chart()

        elif choice == "8":
            print("Saving & exiting...")
            tracker.save_data()
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
