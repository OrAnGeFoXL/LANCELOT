import os

from tinkoff.invest import Client


from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ["INVEST_TOKEN"]

from pprint import pprint


def main():
    with Client(TOKEN) as client:
        r = client.instruments.find_instrument(query="BBG001M2SC01")
        for i in r.instruments:
            pprint(i, indent=1)


if __name__ == "__main__":
    main()
