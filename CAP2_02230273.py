import os

# Bank Account
class BankAccount:
    def __init__(self, acc_no, password, acc_type, balance=0):
        self.acc_no = acc_no
        self.pw = password
        self.acc_type = acc_type
        self.bal = balance

    # Depositing Money To Your Bank Account
    def deposit(self, amount):
        self.bal += amount
        self.update_account()
        print(f"Deposited Nu {amount} into account {self.acc_no}. New balance: Nu {self.bal}")

    # Withdrawing Money To Your Bank Account
    def withdraw(self, amount):
        if amount > self.bal:
            print("Insufficient funds!")
        else:
            self.bal -= amount
            self.update_account()
            print(f"Withdrew Nu {amount} from account {self.acc_no}. New balance: Nu {self.bal}")

    # Transfering Money To Existing Personal/Business Account
    def send_money(self, recipient_acc_no, amount):
        if amount > self.bal:
            print("Insufficient funds!")
        else:
            recipient_acc = self.get_acc(recipient_acc_no)
            if recipient_acc:
                self.bal -= amount
                recipient_acc.deposit(amount)
                self.update_account()
                print(f"Sent Nu {amount} to account {recipient_acc_no}. New balance: Nu {self.bal}")
            else:
                print("Recipient account not found!")

    # Updating the account details in accounts.txt
    def update_account(self):
        accounts = []
        if os.path.exists("accounts.txt"):
            with open("accounts.txt", "r") as f:
                accounts = f.readlines()
        with open("accounts.txt", "w") as f:
            for account in accounts:
                acc_no, password, acc_type, balance = account.strip().split(",")
                if acc_no == self.acc_no:
                    f.write(f"{self.acc_no},{self.pw},{self.acc_type},{self.bal}\n")
                else:
                    f.write(account)

    @staticmethod
    def get_acc(acc_no):
        try:
            with open("accounts.txt", "r") as f:
                accounts = f.readlines()
            for account in accounts:
                acc_no_, password, acc_type, balance = account.strip().split(",")
                if acc_no_ == acc_no:
                    return BankAccount(acc_no_, password, acc_type, float(balance))
        except FileNotFoundError:
            return None

# Personal Account Information
class PersonalAccount(BankAccount):
    def __init__(self, acc_no, password, balance=0):
        super().__init__(acc_no, password, "Personal", balance)

# Business Account Information
class BusinessAccount(BankAccount):
    def __init__(self, acc_no, password, balance=0):
        super().__init__(acc_no, password, "Business", balance)

# Creating Bank Account
def create_account(acc_type):
    acc_no = generate_acc_no()
    password = generate_pw()
    balance = 0
    if acc_type == "Personal":
        account = PersonalAccount(acc_no, password, balance)
    elif acc_type == "Business":
        account = BusinessAccount(acc_no, password, balance)
    else:
        print("Invalid account type!")
        return
    with open("accounts.txt", "a") as f:
        f.write(f"{acc_no},{password},{acc_type},{balance}\n")
    print(f"Account created! Account number: {acc_no}, Password: {password}")

# Logging Bank Account 
def login(acc_no, password):
    account = BankAccount.get_acc(acc_no)
    if account and account.pw == password:
        print(f"Logged in to account {acc_no}!")
        return account
    else:
        print("Invalid account number or password!")
        return None

# Generating Account Number (Random)
def generate_acc_no():
    return str(int(os.urandom(4).hex(), 16))

# Generating Password (Random)
def generate_pw():
    return os.urandom(8).hex()

# Main Menu
def main():
    while True:
        print("Banking Application")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            acc_type = input("Enter account type (Personal/Business): ")
            create_account(acc_type)
        elif choice == "2":
            acc_no = input("Enter account number: ")
            password = input("Enter password: ")
            account = login(acc_no, password)
            if account:
                while True:
                    print("Account Menu")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Send Money")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Choose an option: ")
                    if choice == "1":
                         print(f"Account {acc_no} balance: Nu {account.bal}")
                    elif choice == "2":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif choice == "3":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif choice == "4":
                        recipient_acc_no = input("Enter recipient account number: ")
                        amount = float(input("Enter amount to send: "))
                        account.send_money(recipient_acc_no, amount)
                    elif choice == "5":
                        account.del_acc()
                        break
                    elif choice == "6":
                        break
                    else:
                        print("Invalid option!")
        elif choice == "3":
            break
        else:
            print("Invalid option!")

if __name__ == "__main__":
    main()
