import yfinance as yf


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


def getCompanyStockInfo(tickersSymbol):
    company = yf.Ticker(tickersSymbol)
    basicInfo = extractBasicInfo(company.info)
    print(basicInfo)


getCompanyStockInfo("MSFT")
