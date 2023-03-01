# BorrowBox History Export

This simple script is a start at a rough and ready way to export your loan history from a Library [BorrowBox](https://www.borrowbox.com) account.

## Usage
Update the `env-example` with your BorrowBox instance url, username (often your Library card barcode number) and password (often just a 4-digit PIN). Save as `.env`.

Create a python virtual environment and install the required packages:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Get all your historical BorrowBox data as a `json` file:
```
python ./get.py > loan_history.json
```

At the moment an `output.csv` is created that can be imported into BookWyrm - **NOTE** this should be used at your own risk and sanity checked first!

## Contributing
Ideas, issues, enhancements, PRs etc are very welcome and very needed!
