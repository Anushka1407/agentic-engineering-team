class Account:
    def __init__(self, username: str, initial_deposit: float):
        """
        Initializes a new account with a username and an initial deposit.
        
        Parameters:
        username (str): The username of the account holder.
        initial_deposit (float): The initial amount of money to deposit into the account.
        """
        self.username = username
        self.balance = initial_deposit
        self.portfolio = {}  # Stores holdings as {symbol: quantity}
        self.transactions = []  # Stores transaction records as (type, symbol, quantity, price)
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float):
        """
        Deposits funds into the account.
        
        Parameters:
        amount (float): The amount to deposit. Must be positive.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(("deposit", None, amount, None))

    def withdraw(self, amount: float):
        """
        Withdraws funds from the account.
        
        Parameters:
        amount (float): The amount to withdraw. Must not result in negative balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(("withdraw", None, amount, None))

    def buy_shares(self, symbol: str, quantity: int):
        """
        Records the purchase of shares.
        
        Parameters:
        symbol (str): The stock symbol of the share to buy.
        quantity (int): The number of shares to buy. Must be positive and affordable.
        """
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if total_cost > self.balance:
            raise ValueError("Not enough balance to buy shares.")
        
        self.balance -= total_cost        
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self.transactions.append(("buy", symbol, quantity, share_price))

    def sell_shares(self, symbol: str, quantity: int):
        """
        Records the sale of shares.
        
        Parameters:
        symbol (str): The stock symbol of the share to sell.
        quantity (int): The number of shares to sell. Must be available in the portfolio.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if self.portfolio.get(symbol, 0) < quantity:
            raise ValueError("Not enough shares to sell.")
        
        share_price = get_share_price(symbol)
        total_revenue = share_price * quantity
        self.balance += total_revenue
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.transactions.append(("sell", symbol, quantity, share_price))

    def calculate_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.
        
        Returns:
        float: The total value of the portfolio based on current share prices.
        """
        total_value = self.balance
        for symbol, quantity in self.portfolio.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        Returns:
        float: The profit or loss compared to the initial deposit.
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """
        Gets a report of the current holdings in the user's portfolio.
        
        Returns:
        dict: A dictionary containing the holdings as {symbol: quantity}.
        """
        return self.portfolio

    def get_profit_loss(self) -> float:
        """
        Gets the current profit or loss of the user's account.
        
        Returns:
        float: The current profit or loss.
        """
        return self.calculate_profit_loss()

    def get_transactions(self) -> list:
        """
        Lists all transactions made by the user.
        
        Returns:
        list: A list of transactions as tuples (type, symbol, quantity, price).
        """
        return self.transactions

def get_share_price(symbol: str) -> float:
    """
    Mock function to return the share price for given symbols.
    
    Parameters:
    symbol (str): The stock symbol for which to get the price.
    
    Returns:
    float: The price of the share.
    """
    prices = {
        "AAPL": 150.0,
        "TSLA": 800.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol, 0.0)