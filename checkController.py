import databaseController
import scrapper
from datetime import datetime

def insertCheck (userID, link):
    checkData = scrapper.scrape_web_page(link)

    #conversion to suitable formats
    date = datetime.strptime(checkData["date"], "%d.%m.%Y. %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    total = float(checkData['total'].replace(".","").replace(",","."))

    cursor = databaseController.start_transaction()

    #insert check
    checkID = databaseController.insertInTransaction("checks", "Link, Date, Total, ShopID, UserID, Bill",
                               "%s, %s, %s, %s, %s, %s",
                               (link, date, total, 1, 1, checkData['bill']), cursor)
    
    items = [(checkID, i, 1, ) + checkData['items'][i] for i in range(0, len(checkData['items']))]

    #finish category insert algorithm!

    #insert items
    databaseController.insertInTransaction("checkitems", "CheckID, CheckItemID, CategoryID, Name, Quantity, PricePerItem, TotalPrice",
                                           "%s, %s, %s, %s, %s, %s, %s",
                                           items, cursor)
    return databaseController.commit()
    
