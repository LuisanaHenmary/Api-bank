class CIExist(Exception):
    def __init__(self, ci) -> None:
        self.ci = ci

    def __str__(self) -> str:
        return f"{self.ci} Already exist"

class CIDontExist(Exception):
    def __init__(self, ci) -> None:
        self.ci = ci

    def __str__(self) -> str:
        return f"{self.ci} does not exist"

class AccountDontExist(Exception):
    def __init__(self, num_account) -> None:
        self.num_account = num_account

    def __str__(self) -> str:
        return f"{self.num_account} does not exist"

class InsufficientBalance(Exception):
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return "Insufficient balance"
