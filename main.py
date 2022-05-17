import requests
import smtplib
import dotenv

config = dotenv.dotenv_values(".env")
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY = config["API_KEY"]
NEWS_API = config["NEWS_API"]
EMAIL = config["EMAIL"]
SEND_MAIL = config["SENDTO"]
PASSWORD = config["PASSWORD"]

params = {"function": "TIME_SERIES_DAILY",
          "symbol": STOCK,
          "apikey": API_KEY, }

news_params = {"q": "tesla",
               "apiKey": NEWS_API, }  # insert from param to get appropriate results

a = requests.get("https://www.alphavantage.co/query", params=params)
data = a.json()['Time Series (Daily)']
data = [(a, b) for (a, b) in data.items()][0]
change = (float(data[1]["4. close"]) - float(data[1]["1. open"])) * 100 / float(data[1]["1. open"])

if -5 >= change or change <= 5:
    news = requests.get("https://newsapi.org/v2/everything", params=news_params)
    send_articles = news.json()["articles"][:3]
    msg = f"Subject:{STOCK} change is {change}% \n\n"
    # print(send_articles)
    for i in range(0, len(send_articles)):
        msg += f"{i + 1}. ({send_articles[i]['publishedAt'].split('T')[0]}) {send_articles[i]['title']}\n {send_articles[i]['url']}\n"
    msg.encode('utf-8')

    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=SEND_MAIL, msg=msg)
