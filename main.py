import plaid
import os
import pygsheets
from datetime import datetime
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
SERVICE_FILE = os.getenv('SERVICE_FILE')
EMAIL = os.getenv('EMAIL')

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': CLIENT_ID,
        'secret': SECRET,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

request = TransactionsGetRequest(
    access_token=ACCESS_TOKEN,
    start_date=datetime.strptime('2022-05-1', '%Y-%m-%d').date(),
    end_date=datetime.strptime('2022-06-9', '%Y-%m-%d').date(),
    options=TransactionsGetRequestOptions(
        count=20
    )
)
response = client.transactions_get(request)
transactions = response['transactions']
request_account = AccountsBalanceGetRequest(access_token=ACCESS_TOKEN)
response_account = client.accounts_balance_get(request_account)
accounts = response['accounts']

gc = pygsheets.authorize(service_file=SERVICE_FILE)

print('opening sheets')
# Open spreadsheet and then worksheet
sh = gc.open("Running Budget v1")
wks = sh.sheet1
wks.clear(start='A1')

print('creating header values and formatting')

wks.update_col(1, [['Date'], ['Merchant Name'], ['Price'], [''], ['Deposits'], ['Expenses'], ['Saving'],['Balance']])
wks.adjust_column_width(start=1, end=6, pixel_size='150')
master_cell = wks.cell('A1')
master_cell.set_horizontal_alignment(pygsheets.custom_types.HorizontalAlignment.CENTER)

drange = pygsheets.DataRange(start='A1', worksheet=wks)
drange.apply_format(master_cell)

print('inserting data')
for data in transactions:
    if not (data['merchant_name']):
        data['merchant_name'] = 'Unknown'
    cell_list = [str(data['date']), data['merchant_name'], data['amount']]
    wks.append_table(cell_list, start='A2', overwrite=True)

date_unfiltered = [float(*i) for i in wks.get_values(start="C2", end='C{}'.format(len(transactions)))]
deposits = list(filter(lambda money: money < 0, date_unfiltered))
expenses = list(filter(lambda money: money > 0, date_unfiltered))
deposits_cleaned = []
for e in deposits:
    deposits_cleaned.append(abs(e))

deposits_cell = wks.cell('E2')
expenses_cell = wks.cell('F2')
net_gain = wks.cell('G2')
balance = wks.cell('H2')
deposits_cell.set_value(sum(deposits_cleaned))
expenses_cell.set_value(sum(expenses))
checking_balance = accounts[1]['balances']['available']
balance.set_value(checking_balance)
net_gain.set_value(sum(deposits_cleaned) - sum(expenses))

print('cleaning up')
sh.share(EMAIL)
