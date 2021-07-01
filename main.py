import os
import requests
import time
import pprint

# Coin Rank API Variables
COIN_RANK_URL = "https://api.coinranking.com/v2"
COIN_API = os.environ['coin_rank_api']
GET_HEADERS = {'x-access-token': COIN_API}
# Pretty Print
pp = pprint.PrettyPrinter(indent=1)


def current_unix_time():
    return int(round(time.time()))


def calculate_days_since(day):
    clean_day = int(day)
    current_day = int(round(time.time()))
    day_diff = int((current_day - clean_day)/86400)
    return day_diff


def clean_user_input(string):
    string = string.strip()
    string = string.lower()
    return string


def crypt_get_uuid(symbol):
    url = f"{COIN_RANK_URL}/coins?symbols[]={symbol}"
    response = requests.get(url, headers=GET_HEADERS)
    status_code = response.status_code
    if status_code == 200:
        try:
            uuid = response.json()['data']['coins'][0]['uuid']
            name = response.json()['data']['coins'][0]['name']
            return uuid, name
        except IndexError:
            raise IndexError(f"No Crypto Coin Exists with '{c_symbol}' Symbol") from None
    else:
        print(f"Error in API Call: {status_code} - {response.text}")
        raise IndexError


def get_raw_data(uuid, api_headers):
    url = f"{COIN_RANK_URL}/coin/{uuid}"
    response = requests.get(url, headers=api_headers)
    status_code = response.status_code
    if status_code == 200:
        return response.json()['data']['coin']
    else:
        print(status_code)
        return {}


def parse_coin_data(coin_data):
    try:
        day_since_high = calculate_days_since(coin_data['allTimeHigh']['timestamp'])
        price = round(float(coin_data["price"]), 2)
        perc_change_24 = round(float(coin_data["change"]), 2)
        num_markets = coin_data["numberOfMarkets"]
        vol = round(float(coin_data["24hVolume"]), 2)
        mark_cap = round(float(coin_data["marketCap"]), 2)
        supply = round(float(coin_data['supply']["total"]), 2)
        price_high = round(float(coin_data['allTimeHigh']['price']), 2)
        return {"name_coin": coin_data["name"],
                "symbol_coin": coin_data["symbol"],
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
        return {}
    except TypeError:
        return "Not Enough Data from API"


if __name__ == "__main__":
    print("Welcome to the Crypto/Stock Command Line Tool")
    time.sleep(.2)
    branch_input = str(input("Enter Crypto or Stock: "))
    # Clean the User Input
    branch_input = clean_user_input(branch_input)

    # Crypto Branch
    if branch_input == 'crypto':
        c_symbol = str(input("Please Enter Crypto (Symbol):"))
        # Clean the User Input
        c_symbol = clean_user_input(c_symbol)
        # Get the Crypto UUID from the Symbol
        c_uuid, c_name = crypt_get_uuid(c_symbol)
        # Get Raw Data from API
        print(f"Getting Data For: {c_name}")
        c_raw_data = get_raw_data(c_uuid, GET_HEADERS)
        # Clean Data from API
        c_cleaned_data = parse_coin_data(c_raw_data)
        # Handling for the API not returning enough data
        if type(c_cleaned_data) is str:
            print(f"Not enough data returned from API for {c_name} - {c_symbol} coin")
        else:
            pp.pprint(c_cleaned_data)

    # Stock Market Branch

