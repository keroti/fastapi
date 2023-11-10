def add(a : int, b : int) -> int:
    return a + b

def subtract(a : int, b : int) -> int:
    return a - b

def multiply(a : int, b : int) -> int:
    return a * b

def divide(a : int, b : int) -> float:
    return a / b

class InsufficientAmount(ValueError):
    pass

class BankAccount:
    def __init__(self, balance = 0):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientAmount("Insufficient funds")
        self.balance -= amount
        
    def collect_interest(self):
        self.balance *= 1.1

    def __str__(self) -> str:
        return f"{self.name} has {self.balance} in their account"    