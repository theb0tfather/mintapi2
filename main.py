import pandas as pd
import mintapi as mintapi
import datetime


def get_last_monday():
    d = datetime.date.today()
    day_of_week = d.weekday()
    days_since_monday = d - datetime.timedelta(days=day_of_week)
    last_monday_str = days_since_monday.strftime('%Y-%m-%d')
    return last_monday_str


class Bank:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mint_auth = self.mint_authenticate()
        self.accounts = self.get_accounts()

    def mint_authenticate(self):
        # Opens Mint in new browser window through Selenium webdriver.
        mint_auth = mintapi.Mint(
            self.username,
            self.password,
            mfa_method='sms',
            mfa_input_callback=None,
            mfa_token=None,
            intuit_account=None,
            headless=False,
            session_path=None,
            imap_account=None,
            imap_password=None,
            imap_server=None,
            imap_folder='INBOX',
            wait_for_sync=False,
            wait_for_sync_timeout=500,
            use_chromedriver_on_path=False
        )
        return mint_auth

    def get_accounts(self):
        account_data = self.mint_auth.get_account_data()
        ad_df = pd.DataFrame(account_data)
        return ad_df

    def get_account_balance(self, account_id):
        chase_card = self.accounts.loc[self.accounts['id'] == account_id]
        balance = chase_card.iloc[0]['currentBalance']
        return balance

    def get_account_transactions(self, account_id):
        tr_df = pd.DataFrame(self.mint_auth.get_transaction_data(remove_pending=False))
        account_transactions = tr_df.loc[tr_df['accountId'] == account_id]
        return account_transactions

    @staticmethod
    def get_pending_transactions(transactions):
        pending = transactions.loc[transactions['status'] == 'MANUAL']
        pending_sum = pending['amount'].sum()
        return pending_sum

    def get_current_balance(self, account_id):
        transactions = self.get_account_transactions(account_id)
        posted_balance = self.get_account_balance(account_id)
        pending_balance = self.get_pending_transactions(transactions) * -1
        return round(posted_balance + pending_balance, 2)

    def spend_since_monday(self, account_id):
        last_monday = get_last_monday()
        transactions = self.get_account_transactions(account_id)
        monday_transactions = transactions.loc[transactions['date'] >= last_monday]
        spend = monday_transactions['amount'].sum()
        return spend

if __name__ == '__main__':
    username = 'username'
    password = 'password'
    bank = Bank(username,password)
    # chase_balance = bank.get_current_balance('75417769_13615882')
    spend_since_monday = bank.spend_since_monday('75417769_13615882')
    print('asd')

