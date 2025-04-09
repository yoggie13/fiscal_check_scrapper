import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
  "host" : "localhost",
  "user" : os.getenv('DATABASE_USER'),
  "password" : os.getenv('DATABASE_PASS'),
  "database" : "fiscal_check"
}


connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **dbconfig)

def get_connection():
    return 
connection_pool.get_connection()

transactionCheck = True

def start_transaction():
    try:
        conn = connection_pool.get_connection()
        conn.start_transaction()
        return [conn, conn.cursor()]
    except Exception as e:
        return False

def commit(conn):
    global transactionCheck
    
    if transactionCheck:
        try:
            conn.commit()
            return True
        except Exception as e:
            return False
    else:
        conn.rollback()
        conn.close()
        transactionCheck =  True

def insertInTransaction (table, propNames, props, mycursor):
    
    ss = ", ".join(["%s"] * len(propNames.split(", ")))
    sql = f"INSERT INTO {table} ({propNames}) VALUES ({ss})"

    try:
        if type(props) == tuple:
            mycursor.execute(sql, props)
        else:
            mycursor.executemany(sql, props)
        return mycursor.lastrowid
    except Exception as e:
        print(e)
        transactionCheck = False


def insert (table, propNames, propTypes, props):
    conn = connection_pool.get_connection()
    mycursor = conn.cursor()

    sql = f"INSERT INTO {table} ({propNames}) VALUES ({propTypes})" 

    try:
        if type(props) == tuple:
            mycursor.execute(sql, props)
        else:
            mycursor.executemany(sql, props)
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        mycursor.close() 
        conn.close()

def select (table,  where = None, what="*", groupBy=None):
    try:
        with connection_pool.get_connection() as conn:
            with conn.cursor(dictionary=True) as mycursor:
                sql = f"SELECT {what} FROM {table} {f'WHERE {where}' if where != None else ''} {f'GROUP BY {groupBy}' if groupBy != None else ''}"
                mycursor.execute(sql)
                return mycursor.fetchall()

    except Exception as e:
        print(e)
        return []


def searchChecksWithItems(userID, search, what="*"):
    try:
        with connection_pool.get_connection() as conn:
            with conn.cursor() as mycursor: 
                mycursor.execute("SHOW COLUMNS FROM checks")
                checkColumns = [col[0] for col in mycursor.fetchall()]
            
            checkColumns.remove("UserID")
                
            with conn.cursor() as mycursor: 
                mycursor.execute("SHOW COLUMNS FROM checkitems")
                checkItemsColumns = [col[0] for col in mycursor.fetchall()]

            where_clause = " OR ".join([f"c.{col} LIKE LOWER(%s)" for col in checkColumns])
            where2_clause = " OR ".join([f"ci.{col} LIKE LOWER(%s)" for col in checkItemsColumns])

            where = where_clause + " OR " + where2_clause

            sql = f"SELECT DISTINCT c.CheckID, c.Date, c.UserPaid, c.Total, s.Name as ShopName, ca.CategoryID, ca.Name as CategoryName FROM checks as c JOIN checkitems as ci ON c.CheckID = ci.CheckID JOIN shops as s ON c.ShopID = s.ShopID AND c.PIB = s.PIB JOIN categories ca on c.CategoryID = ca.CategoryID WHERE c.UserID = {userID} AND ({where})"
            search = f"%{search}%".lower()

            with conn.cursor(dictionary=True) as mycursor:
                mycursor.execute(sql, [search] * (len(checkColumns)+len(checkItemsColumns)))
                sqlReturn = mycursor.fetchall()

            return sqlReturn
    except Exception as e:
        print(e)
        return False


def update (table, what, value, where):
    try:
        with connection_pool.get_connection() as conn:
            with conn.cursor() as mycursor:
                sql = f"UPDATE {table} SET {what} = {value} WHERE {where}"
                mycursor.execute(sql)
                conn.commit()

        return True
    except Exception as e:
        print(e)
        return False

def delete (table, where):
    try:
        with connection_pool.get_connection() as conn:
            with conn.cursor() as mycursor:
                sql = f"DELETE FROM {table} WHERE {where}"
                mycursor.execute(sql)
                conn.commit()

        return True
    except Exception as e:
        print(e)
        return False
