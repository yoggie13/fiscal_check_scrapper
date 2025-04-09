import databaseController
import scrapper
from datetime import datetime
import base64
import pprint

def insertCheck (userID, link, category, favorite):
    checkData = scrapper.scrape_web_page(link)

    #conversion to suitable formats
    date = datetime.strptime(checkData["date"], "%d.%m.%Y. %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
    total = float(checkData['total'].replace(".","").replace(",","."))

    [conn, cursor] = databaseController.start_transaction()

    #insert check
    if len(databaseController.select("shops", f"ShopID = {checkData['shopID']} AND PIB = {checkData['PIB']}")) == 0:
        databaseController.insertInTransaction("shops", 
                                               "PIB, ShopID, Name", 
                                               (checkData["PIB"], checkData['shopID'], checkData['shopName']), 
                                               cursor)
    pprint.pprint(checkData['QR'])
    databaseController.insertInTransaction("checks", 
                                           "CheckID, Link, Date, Total, ShopID, PIB, UserID, Bill, UserPaid, CategoryID, Favorite, QR",
                                            (checkData["id"], link, date, total, checkData["shopID"], 
                                             checkData["PIB"], 1, checkData['bill'], total, category, favorite, base64.b64decode(checkData['QR'])), 
                                            cursor)
    
    items = [(checkData["id"], i, ) + checkData['items'][i] for i in range(0, len(checkData['items']))]

    #insert items
    databaseController.insertInTransaction("checkitems", 
                                           "CheckID, CheckItemID, Name, Quantity, PricePerItem, TotalPrice",
                                           items, 
                                           cursor)
    
    return databaseController.commit(conn)
    
def searchChecks (userID, query):
    checks = databaseController.searchChecksWithItems(userID, query)

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks

def getCheck(check_id):
    checkData = databaseController.select("checks c JOIN shops s on c.ShopID = s.ShopID AND c.PIB = s.PIB JOIN categories ca on c.CategoryID = ca.CategoryID", 
                                     f"CheckID = '{check_id}'",
                                     "c.CheckID, c.UserPaid, c.Date, c.Link, c.Bill, c.Favorite, s.Name as ShopName, c.QR, ca.CategoryID, ca.Name as CategoryName")
    if(len(checkData) == 0): return {}

    else: 
        checkData = checkData[0]
        checkData['QR'] = 'data:image/gif;base64,' + base64.b64encode(checkData['QR']).decode('utf-8')
        checkData['Date'] = checkData['Date'].isoformat()

        checkData['CheckItems'] = databaseController.select("checkitems", f"CheckID = '{check_id}'")
        
        return checkData

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

def updateFavorite (userID, checkID, favorite):
    return databaseController.update("checks",
                              "Favorite",
                              favorite,
                              f"CheckID = '{checkID}' AND UserID = {userID}")

def getAnalytics (userID, rangeBegin, rangeEnd):
    return databaseController.select(
        table="categories ca LEFT JOIN checks c ON ca.CategoryID = c.CategoryID" + f" AND c.UserID = {userID} AND c.Date >= {rangeBegin} AND c.Date <= {'DATE_ADD('+rangeEnd+', INTERVAL 1 DAY)' if rangeEnd != None else 'DATE_ADD(CURDATE(), INTERVAL 1 DAY)'}",
        what="ca.CategoryID, ca.Name, COALESCE(SUM(c.UserPaid), 0) as TotalSpent",
        groupBy="ca.CategoryID"
    )

def getChecksByCategory (userID, categoryID):
    checks = databaseController.select(
        table="checks c JOIN shops s ON c.ShopID = s.ShopID AND c.PIB = s.PIB",
        what="c.CheckID, s.Name, c.Date, c.UserPaid, c.Total",
        where=f"c.CategoryID = {categoryID}"
    )

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks

def getRecentChecks(userID):
    checks = databaseController.select(
            table="checks c JOIN shops s ON c.ShopID = s.ShopID AND c.PIB = s.PIB JOIN categories ca on c.CategoryID = ca.CategoryID",
            what="c.CheckID, s.Name as ShopName, c.Date, c.UserPaid, c.Total, ca.Name as CategoryName, ca.CategoryID",
            where=f"c.UserID = {userID} AND c.Date >= NOW() - INTERVAL 7 day"
    )

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks

def getChecks(userID):
    checks = databaseController.select(
            table="checks c JOIN shops s ON c.ShopID = s.ShopID AND c.PIB = s.PIB JOIN categories ca on c.CategoryID = ca.CategoryID",
            what="c.CheckID, s.Name as ShopName, c.Date, c.UserPaid, c.Total, ca.Name as CategoryName, ca.CategoryID",
            where=f"c.UserID = {userID} ORDER BY c.DATE"
    )

    for i in range(0, len(checks)):
        checks[i]['Date'] = checks[i]['Date'].isoformat()

    return checks

def deleteACheck(userID, checkID):
    return databaseController.delete("checks", f"CheckID = '{checkID}' AND UserID = {userID}")

def getCategories():
    return databaseController.select("categories")