import yfinance as yf
import requests
from datetime import datetime


def extractBasicInfo(data):
    keystoExcract = [
        "longName",
        "website",
        "sector",
        "fullTimeEmployees",
        "marketCap",
        "totalRevenue",
        "trailingEps",
    ]
    basicInfo = {}
    for key in keystoExcract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""

    return basicInfo


def getPriceHistory(company):
    historyDf = company.history(period="12mo")
    prices = historyDf["Open"].tolist()
    dates = historyDf.index.strftime("%Y-%m-%d").tolist()

    return {"price": prices, "dates": dates}


def getEarningsDates(company):
    earningsDatesDF = company.earnings_dates
    allDates = earningsDatesDF.index.strftime("%Y-%m-%d").tolist()
    datesObjects = [datetime.strptime(date, "%Y-%m-%d") for date in allDates]
    currentDate = datetime.now()
    futureDates = [
        date.strftime("%Y-%m-%d") for date in datesObjects if date > currentDate
    ]
    return futureDates


def getCompanyNews(company):
    newslist = company.news
    allNewsArticles = []
    for newsDict in newslist:
        newsDictToAdd = {
            "title": newsDict["content"]["title"],
            "URL": newsDict["content"]["canonicalUrl"]["url"],
        }
        allNewsArticles.append(newsDictToAdd)
    # print( allNewsArticles)
    return allNewsArticles


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


def extractCompanyNewsArticles(newsArticles):
    url = newsArticles[0]["URL"]
    page = requests.get(url, headers=headers)
    print(page)


def getCompanyStockInfo(tickersSymbol):
    # Get data from Yahoo Finance
    company = yf.Ticker(tickersSymbol)

    # Get basic info from company
    basicInfo = extractBasicInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureearningsDates = getEarningsDates(company)
    companyNews = getCompanyNews(company)
    newsArticles = getCompanyNews(company)
    extractCompanyNewsArticles(newsArticles)


getCompanyStockInfo("MSFT")
