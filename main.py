import os
import sys
import datetime
import time
import pprint
import requests

# Pretty Print
pp = pprint.PrettyPrinter(indent=1)


def current_unix_time():
    return int(round(time.time()))


def yesterday_date():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday


def calculate_days_since(day):
    clean_day = int(day)
    current_day = int(round(time.time()))
    day_diff = int((current_day - clean_day) / 86400)
    return day_diff


def clean_user_input(string):
    string = string.strip()
    string = string.lower()
    return string


class CryptoData:
    def __init__(self):
        self.api_url = "https://api.coinranking.com/v2"
        self.api_key = os.environ['coin_rank_api']
        self.get_headers = {'x-access-token': self.api_key}
        self.crypto_uuid = None
        self.crypto_name = None
        self.raw_data = None
        self.clean_data = None

    def get_uuid(self, symbol):
        url = f"{self.api_url}/coins?symbols[]={symbol}"
        response = requests.get(url, headers=self.get_headers)
        status_code = response.status_code
        if status_code == 200:
            try:
                uuid = response.json()['data']['coins'][0]['uuid']
                name = response.json()['data']['coins'][0]['name']
                self.crypto_uuid = uuid
                self.crypto_name = name
            except IndexError:
                self.crypto_uuid = None
                self.crypto_name = None
        else:
            print(f"Error in API Call: {status_code} - {response.text}")
            raise IndexError

    def get_raw_data(self):
        url = f"{self.api_url}/coin/{self.crypto_uuid}"
        response = requests.get(url, headers=self.get_headers)
        status_code = response.status_code
        if status_code == 200:
            self.raw_data = response.json()['data']['coin']
        else:
            print(status_code)
            self.raw_data = {}

    def parse_coin_data(self):
        try:
            day_since_high = calculate_days_since(self.raw_data['allTimeHigh']['timestamp'])
            price = round(float(self.raw_data["price"]), 2)
            perc_change_24 = round(float(self.raw_data["change"]), 2)
            num_markets = self.raw_data["numberOfMarkets"]
            vol = round(float(self.raw_data["24hVolume"]), 2)
            mark_cap = round(float(self.raw_data["marketCap"]), 2)
            supply = round(float(self.raw_data['supply']["total"]), 2)
            price_high = round(float(self.raw_data['allTimeHigh']['price']), 2)
            self.clean_data = {"name_coin": self.raw_data["name"],
                               "symbol_coin": self.raw_data["symbol"],
                               "price": f'{price:,}',
                               "percent_change_24hr": perc_change_24,
                               "number_of_markets": f'{num_markets:,}',
                               "volume": f'{vol:,}',
                               "market_cap": f'{mark_cap:,}',
                               "total_supply": f'{supply:,}',
                               "all_time_high": f'{price_high:,}',
                               "days_since_all_time_high": day_since_high,
                               "timestamp": current_unix_time()}
        except KeyError as e:
            print(e)
            self.clean_data = {}
        except TypeError:
            self.clean_data = "Not Enough Data from API"


class PolyFinData:
    def __init__(self):
        self.api_url = "https://api.polygon.io/v1/open-close/"
        self.api_key = os.environ['polygon_api']
        self.raw_data = None
        self.clean_data = None

    def call_api(self, symb, yes_date):
        fin_api_url = f"{self.api_url}{symb}/{yes_date}?adjusted=true&apiKey={self.api_key}"


if __name__ == "__main__":
    print("Welcome to the Crypto/Stock Command Line Tool - type exit to leave")
    time.sleep(.2)
    while 1:
        branch_input = str(input("Enter Crypto or Stock: "))
        # Clean the User Input
        branch_input = clean_user_input(branch_input)

        # Crypto Branch
        if branch_input == 'crypto':
            crypto = CryptoData()
            c_symbol = str(input("Please Enter Crypto (Symbol):"))
            # Clean the User Input
            c_symbol = clean_user_input(c_symbol)
            # Get the Crypto UUID from the Symbol
            crypto.get_uuid(c_symbol)
            c_uuid = crypto.crypto_uuid
            c_name = crypto.crypto_name
            if c_uuid is None and c_name is None:
                print(f"There is no Coin with the Symbol '{c_symbol}'. Please try again.")
            else:
                # Get Raw Data from API
                print(f"Getting Data For: {c_name}")
                crypto.get_raw_data()
                c_raw_data = crypto.raw_data
                # Clean Data from API
                crypto.parse_coin_data()
                c_cleaned_data = crypto.clean_data
                # Handling for the API not returning enough data
                if isinstance(c_cleaned_data, str):
                    print(f"Not enough data returned from API for {c_name} - {c_symbol} coin")
                else:
                    pp.pprint(c_cleaned_data)

        # Stock Market Branch
        elif branch_input == 'stock':
            print("Stock work done here")

        # Allows user to exit program
        elif branch_input == 'exit':
            sys.exit("Thank you")

        # Handling for a response other than expected
        else:
            print("Command not recognized - enter Crypto or Stock")
