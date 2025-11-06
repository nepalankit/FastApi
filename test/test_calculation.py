from app.calculations import add,BankAccount


def test_add():
    print("testing function")
    sum=add(2,3)
    assert sum==5
    
    
    print("test passed")

def test_bank_account_initial_amount():
    account=BankAccount(100)
    assert account.balance==100
    
def test_inital_amount_default():
    account=BankAccount()
    assert account.balance==0

def test_withdraw():
    account=BankAccount(200)
    account.withdraw(50)
    assert account.balance==150
    
def test_deposit():
    account=BankAccount(200)
    account.deposit(100)
    assert account.balance==300
    
def test_interest():
    account=BankAccount(100)
    account.collect_interest()
    assert round(account.balance)==110