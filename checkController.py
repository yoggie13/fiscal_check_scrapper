import databaseController
import scrapper
from datetime import datetime
import pprint
def insertCheck (userID, link):
    checkData = scrapper.scrape_web_page(link)

    #conversion to suitable formats
    date = datetime.strptime(checkData["date"], "%d.%m.%Y. %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    total = float(checkData['total'].replace(".","").replace(",","."))

    cursor = databaseController.start_transaction()

    #insert check
    checkID = databaseController.insertInTransaction("checks", "Link, Date, Total, ShopID, UserID, Bill, UserPaid, CategoryID",
                               "%s, %s, %s, %s, %s, %s, %s, %s",
                               (link, date, total, 1, 1, checkData['bill'], total, None), cursor)
    
    items = [(checkID, i, ) + checkData['items'][i] for i in range(0, len(checkData['items']))]

    #finish category insert algorithm!

    #insert items
    databaseController.insertInTransaction("checkitems", "CheckID, CheckItemID, Name, Quantity, PricePerItem, TotalPrice",
                                           "%s, %s, %s, %s, %s, %s",
                                           items, cursor)
    return databaseController.commit()
    
def returnCheck (userID, query):
    pprint.pprint(databaseController.selectCheckWithItems(userID, query))

