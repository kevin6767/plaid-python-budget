
# Budget Creator with Plaid-Python

When researching how to learn Python coming from a JS/React frontend background, 
I found myself entertaining the idea of creating tools to help me in my 
everyday life. This was the first step in improving myself and my coding skills
by creating a budget that pulls in real-time financial data and organizes it in a Google Sheet
that is then shared (emailed) to me. 

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`CLIENT_ID` 

`SECRET`

`ACCESS_TOKEN`

`SERVICE_FILE`

`EMAIL`


## FAQ

Before doing anything, you should first follow these two setup guides
- https://plaid.com/docs/quickstart/ 
    - this will give you access to `CLIENT_ID` and `SECRET` and `ACCESS_TOKEN` that is gained through allowing access to your bank
- https://pygsheets.readthedocs.io/en/stable/index.html
    - install pygsheets and follow the authorization guide. This will give you access to download the JSON file `service_account_credentials` that is used for our `.env` variable `SERVICE_FILE`
    

## Run Locally

Clone the project

```bash
  git clone https://github.com/kevin6767/plaid-python-budget.git
```

Go to the project directory

```bash
  cd running_budget_plaid
```

If all of your setup is complete with the enviroment variables, then you can

```bash
    python main.py 
```



## Roadmap

- Currently the dates are hardcoded, so figure out a way to dynamically fill the budget with the latest data and ignore past data that is no longer revelant

- Think about merging the quickstart plaid process into the app as well. if the `access_token` doesn't exist for a user, then prompt them to add their bank and programmically get the access_token that way

- Add more functionality to the spreadsheet. This was the most rushed part of the whole project and could use some proper love. Pygsheets wasn't the most enjoyable to use, but maybe in the future I'll circle back to this. 

