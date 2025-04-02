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
    if len(databaseController.select("shops", f"ShopID = {checkData['shopID']} AND PIB = {checkData['PIB']}")) == 0:
        databaseController.insertInTransaction("shops", 
                                               "PIB, ShopID, Name", 
                                               (checkData["PIB"], checkData['shopID'], checkData['shopName']), 
                                               cursor)
    
    databaseController.insertInTransaction("checks", 
                                           "CheckID, Link, Date, Total, ShopID, PIB, UserID, Bill, UserPaid, CategoryID",
                                            (checkData["id"], link, date, total, checkData["shopID"], checkData["PIB"], 1, checkData['bill'], total, 5), 
                                            cursor)
    
    items = [(checkData["id"], i, ) + checkData['items'][i] for i in range(0, len(checkData['items']))]

    #insert items
    databaseController.insertInTransaction("checkitems", 
                                           "CheckID, CheckItemID, Name, Quantity, PricePerItem, TotalPrice",
                                           items, 
                                           cursor)
    
    return databaseController.commit()
    
def searchChecks (userID, query):
    checks = databaseController.searchChecksWithItems(userID, query)

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks

def updateUserPaid (userID, checkID, userPaid):
    return databaseController.update("checks",
                              "UserPaid",
                              userPaid,
                              f"CheckID = '{checkID}' AND UserID = {userID}")

def updateCategory (userID, checkID, categoryID):
    return databaseController.update("checks",
                              "CategoryID",
                              categoryID,
                              f"CheckID = '{checkID}' AND UserID = {userID}")

def getAnalytics (userID, rangeBegin, rangeEnd):
    return databaseController.select(
        table="categories ca LEFT JOIN checks c ON ca.CategoryID = c.CategoryID" + f" AND c.UserID = {userID} AND c.Date BETWEEN {rangeBegin} AND {rangeEnd if rangeEnd != None else 'CURDATE()'}",
        what="ca.CategoryID, ca.Name, COALESCE(SUM(c.UserPaid), 0) as TotalSpent",
        groupBy="ca.CategoryID"
    )

def getCheckByCategory (userID, categoryID):
    checks = databaseController.select(
        table="checks c JOIN shops s ON c.ShopID = s.ShopID AND c.PIB = s.PIB",
        what="c.CheckID, s.Name, c.Date, c.UserPaid, c.Total",
        where=f"c.CategoryID = {categoryID}"
    )

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks