from collections import defaultdict
from datetime import datetime
import os

import gspread

TYPE = "service_account"
PROJECT_ID = os.getenv("PROJECT_ID")
PRIVATE_KEY_ID = os.getenv("PRIVATE_KEY_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY").replace("\\n", "\n")
CLIENT_EMAIL = os.getenv("CLIENT_EMAIL")
CLIENT_ID = os.getenv("CLIENT_ID")
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL = "https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL = os.getenv("CLIENT_X509_CERT_URL")

CREDENTIALS = {
    "type": TYPE,
    "project_id": PROJECT_ID,
    "private_key_id": PRIVATE_KEY_ID,
    "private_key": PRIVATE_KEY,
    "client_email": CLIENT_EMAIL,
    "client_id": CLIENT_ID,
    "auth_uri": AUTH_URI,
    "token_uri": TOKEN_URI,
    "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url": CLIENT_X509_CERT_URL
}


class ManageGoogleSheets:

    def __init__(self):
        service_account = gspread.service_account_from_dict(CREDENTIALS)

        self.sheet = service_account.open("investment_statistics")
        self.profits_date: list = []
        self.profits_value: list = []
        self.profits_ranking: defaultdict = defaultdict(list)
        now = datetime.now()

        self.start_year = 2018
        self.current_year = now.year
        self.current_month = now.month
        self.years = [year for year in range(self.current_year, self.start_year - 1, -1)]

    def get_profits(self):

        if self.profits_date:
            return

        range_sheet = (self.current_year - self.start_year) * 12 + (self.current_month - 11) + 2

        work_sheet = self.sheet.worksheet("Sheet-for-website")
        profits = work_sheet.get_all_values()[1:range_sheet]
        length_profits = len(profits)
        for i in range(0, length_profits, 3):
            profit = profits[i]
            self.profits_date.append(f"{profit[0]}/{profit[1]}")
            self.profits_value.append(int(profit[2]))
        print(self.profits_date)
        return

    def get_ranking(self):

        if len(self.profits_ranking) == self.current_year - self.start_year + 1:
            return
        else:
            self.profits_ranking = defaultdict(list)

        for year in self.years:
            work_sheet = self.sheet.worksheet(f"{year}-ranking")
            profit_ranking = work_sheet.get_all_values()[1:]
            for p_r in profit_ranking:
                if p_r[0][0] == "#":
                    break
                self.profits_ranking[year].append(p_r)
        return
