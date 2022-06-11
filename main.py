from datetime import datetime
import plaid
from plaid.api import plaid_api
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
import pygsheets
import numpy as np

# Available environments are
# 'Production'
# 'Development'
# 'Sandbox'
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

configuration = plaid.Configuration(
    host=plaid.Environment.Development,
    api_key={
        'clientId': "6261ad2ca538fb001a150a6a",
        'secret': "ebaadda6199f7aa1348d24ce920439",
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

request = TransactionsGetRequest(
    access_token="access-development-e9bedab4-46af-48d4-8117-d556447927a1",
    start_date=datetime.strptime('2022-05-1', '%Y-%m-%d').date(),
    end_date=datetime.strptime('2022-06-9', '%Y-%m-%d').date(),
    options=TransactionsGetRequestOptions(
        count=20
    )
)
response = client.transactions_get(request)
transactions = response['transactions']
request_account = AccountsBalanceGetRequest(access_token="access-development-e9bedab4-46af-48d4-8117-d556447927a1")
response_account = client.accounts_balance_get(request_account)
accounts = response['accounts']

gc = pygsheets.authorize(service_file='service_account_credentials.json')

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
sh.share("kevin.eslick4156@gmail.com")

# {'account_id': 'RXN3yXrL6EH7O0ZabgvaTKNo1Ad4MmU5JwR3n',
#  'account_owner': None,
#  'amount': 74.83,
#  'authorized_date': None,
#  'authorized_datetime': None,
#  'category': ['Shops', 'Supermarkets and Groceries'],
#  'category_id': '19047000',
#  'check_number': None,
#  'date': datetime.date(2022, 5, 2),
#  'datetime': None,
#  'iso_currency_code': 'USD',
#  'location': {'address': None,
#               'city': 'Newark',
#               'country': None,
#               'lat': None,
#               'lon': None,
#               'postal_code': None,
#               'region': 'DE',
#               'store_number': None},
#  'merchant_name': 'Acme Markets',
#  'name': 'CHECKCARD 0429 ACME 2680 NEWARK DE XXXXX5221XXXXXXXXXX0298',
#  'payment_channel': 'in store',
#  'payment_meta': {'by_order_of': None,
#                   'payee': None,
#                   'payer': None,
#                   'payment_method': None,
#                   'payment_processor': None,
#                   'ppd_id': None,
#                   'reason': None,
#                   'reference_number': None},
#  'pending': False,
#  'pending_transaction_id': None,
#  'personal_finance_category': None,
#  'transaction_code': None,
#  'transaction_id': 'vbzZabKNmeH8R49YOXvYi4ZgqPDvweHJDQzoL',
#  'transaction_type': 'place',
#  'unofficial_currency_code': None}
