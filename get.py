import os
from dotenv import load_dotenv
import requests, json
from bs4 import BeautifulSoup

load_dotenv()
URL = os.environ["URL"]
USER_DATA = {"username": os.environ["USERNAME"], "password": os.environ["PASSWORD"]}

session = requests.Session()

# Get siteId and xsrf token
response = session.get(f"{URL}/login")

soup = BeautifulSoup(response.text, "html.parser")
next_data = soup.find(id="__NEXT_DATA__")
data = json.loads(next_data.string)

XSRF_TOKEN = response.cookies["XSRF-TOKEN"]
SITEID = data["props"]["siteContext"]["siteId"]

session.headers.update({"app-siteId": SITEID, "origin": URL, "X-XSRF-TOKEN": XSRF_TOKEN})

# Login
response = session.post(f"{URL}/api/v1/auth/login", json=USER_DATA)

# Get total counts
response = session.get(f"{URL}/home/my-loans")
soup = BeautifulSoup(response.text, "html.parser")
next_data = soup.find(id="__NEXT_DATA__")
data = json.loads(next_data.string)

totalCount = {}
for query in data["props"]["pageProps"]["dehydratedState"]["queries"]:
    if query["queryKey"][0] == "loanHistory":
        loanType = query["queryKey"][1]["loanFormat"]
        totalCount[loanType] = query["state"]["data"]["totalCount"][loanType]

# Get the data!
loan_history = {}
for loanType in totalCount.keys():
    response = session.post(
        f"{URL}/api/v1/loans/historical/products?loanFormat={loanType}&limit={totalCount[loanType]}"
    )
    data = json.loads(response.text)
    loan_history[loanType] = data["loans"]

print(json.dumps(loan_history, indent=2))
