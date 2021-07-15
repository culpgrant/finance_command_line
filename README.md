# Finance Command Line
Finance Command Line Python Program where you can type in a Crypto Currency Symbol or a Stock Ticker and get the most recent financial data on that entity.


## API Connections
The program uses [Coinranking Api](https://developers.coinranking.com/api/documentation) for all Crypto related data and the program uses [Polygon API](https://polygon.io/) for all Stock Market related data. All the API keys are stored in the environment variables, so to run it on your own you would need to sign up for your own API's with both of the services. Both services have free tiers and I recommend them. The environment variables are called 'coin_rank_api' and 'polygon_api'

## Usage
After cloning the git repo, update the environment variables, and then just start the program. It will ask for either 'Crypto' or 'Stock' if you want to check a Cryptocurrency type 'Crypto' and the same for 'Stock'. From there it will ask for a Crypto Symbol or a Stock Ticker. If the symbol entered is not correct it will handle that response and ask for a new one. Anytime you can type 'exit' to leave the program. The program will only ever exit from an error if there is a bad API request.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
