import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientAmount

@pytest.fixture
def zero_bank_account():
    print("Setting up a zero BankAccount")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("Setting up BankAccount")
    return BankAccount(50)

@pytest.mark.parametrize("a, b, expected", [
    (3, 5, 8),
    (2, 4, 6),
    (1, 9, 10),
    (12, 45, 57),
])

def test_add(a, b, expected):
    print("Testing add()")
    assert add(a, b) == expected

def test_subtract():
    print("Testing subtract()")
    assert subtract(7, 3) == 4

def test_multiply():
    print("Testing multiply()")
    assert multiply(2, 3) == 6

def test_divide():
    print("Testing divide()")
    assert divide(6, 3) == 2

def test_bank_default(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

def test_bank_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 3) == 55

@pytest.mark.parametrize("deposit, withdraw, expected", [
    (300, 50, 250),
    (275, 175, 100),
    (1000, 690, 310),
    (100, 45, 55),
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected

def test_bank_insufficient_funds(bank_account):
    with pytest.raises(InsufficientAmount):
        bank_account.withdraw(100)

if __name__ == '__main__':
    test_add()