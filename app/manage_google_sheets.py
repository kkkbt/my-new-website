from collections import defaultdict
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

    def get_profits(self):
        work_sheet = self.sheet.worksheet("Sheet-for-website")
        profits = work_sheet.get_all_values()
        length_profits = len(profits)
        for i in range(length_profits // 7):
            profit = profits[i * (length_profits // 7) + 1]
            self.profits_date.append(f"{profit[0]}/{profit[1]}")
            self.profits_value.append(profit[2])
        return

    def get_ranking(self):
        years = [2018, 2019, 2020, 2021, 2022]
        for year in years:
            work_sheet = self.sheet.worksheet(f"{year}-ranking")
            profit_ranking = work_sheet.get_all_values()[1:]
            for p_r in profit_ranking:
                if p_r[0][0] == "#":
                    break
                self.profits_ranking[year].append(p_r)
        return
