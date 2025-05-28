import gradio as gr
from accounts import Account, get_share_price

account = None

def create_account(username, initial_deposit):
    global account
    account = Account(username, float(initial_deposit))
    return f"Account created for {username} with initial deposit of ${initial_deposit}."

def deposit_funds(amount):
    global account
    account.deposit(float(amount))
    return f"Deposited ${amount}. Current balance: ${account.balance}."

def withdraw_funds(amount):
    global account
    try:
        account.withdraw(float(amount))
        return f"Withdrew ${amount}. Current balance: ${account.balance}."
    except ValueError as e:
        return str(e)

def buy_shares(symbol, quantity):
    global account
    try:
        account.buy_shares(symbol, int(quantity))
        return f"Bought {quantity} shares of {symbol}. Current holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def sell_shares(symbol, quantity):
    global account
    try:
        account.sell_shares(symbol, int(quantity))
        return f"Sold {quantity} shares of {symbol}. Current holdings: {account.get_holdings()}"
    except ValueError as e:
        return str(e)

def portfolio_value():
    global account
    return f"Total portfolio value: ${account.calculate_portfolio_value()}"

def profit_loss():
    global account
    return f"Profit/Loss: ${account.calculate_profit_loss()}"

def transactions():
    global account
    return f"Transactions: {account.get_transactions()}"

iface = gr.Interface(
    fn=create_account,
    inputs=["text", "number"],
    outputs="text",
    title="Trading Account Management",
    description="Create an account and manage your trading activities."
)

deposit_iface = gr.Interface(
    fn=deposit_funds,
    inputs="number",
    outputs="text",
    title="Deposit Funds"
)

withdraw_iface = gr.Interface(
    fn=withdraw_funds,
    inputs="number",
    outputs="text",
    title="Withdraw Funds"
)

buy_iface = gr.Interface(
    fn=buy_shares,
    inputs=["text", "number"],
    outputs="text",
    title="Buy Shares"
)

sell_iface = gr.Interface(
    fn=sell_shares,
    inputs=["text", "number"],
    outputs="text",
    title="Sell Shares"
)

value_iface = gr.Interface(
    fn=portfolio_value,
    inputs=None,
    outputs="text",
    title="Portfolio Value"
)

profit_loss_iface = gr.Interface(
    fn=profit_loss,
    inputs=None,
    outputs="text",
    title="Profit/Loss"
)

transactions_iface = gr.Interface(
    fn=transactions,
    inputs=None,
    outputs="text",
    title="Transactions"
)

app = gr.TabbedInterface([iface, deposit_iface, withdraw_iface, buy_iface, sell_iface, value_iface, profit_loss_iface, transactions_iface], ["Create Account", "Deposit", "Withdraw", "Buy Shares", "Sell Shares", "Portfolio Value", "Profit/Loss", "Transactions"])

if __name__ == "__main__":
    app.launch()