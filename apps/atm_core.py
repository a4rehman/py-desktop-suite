"""Pure banking logic shared by the desktop and web ATM terminals."""


class AtmAccount:
    def __init__(self, pin="1234", balance=2500.0):
        self._pin = str(pin)
        self.balance = float(balance)
        self.transactions = []

    def verify_pin(self, entered):
        return str(entered) == self._pin

    def change_pin(self, new):
        if not (new and len(str(new)) == 4 and str(new).isdigit()):
            return False, "Invalid PIN format. PIN must be 4 digits."
        self._pin = str(new)
        return True, "Security PIN updated."

    def deposit(self, amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return False, "Invalid deposit amount."
        if amount <= 0:
            return False, "Deposit amount must be greater than $0."
        self.balance += amount
        self.transactions.append(f"Deposit: +${amount:,.2f}")
        return True, f"Deposited ${amount:,.2f}."

    def withdraw(self, amount):
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return False, "Invalid withdrawal amount."
        if not (0 < amount <= self.balance):
            return False, "Insufficient balance or invalid amount."
        self.balance -= amount
        self.transactions.append(f"Withdrawal: -${amount:,.2f}")
        return True, f"Withdrawn ${amount:,.2f}."