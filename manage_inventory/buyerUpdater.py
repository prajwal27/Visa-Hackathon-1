import uuid
def updateBuyerInventory(mysql,orderID,buyerMerchantID):
    query = "SELECT Name , Description,Price,ProductCart.Quantity as Quantity,Category FROM Orders,ProductCart,Product WHERE OrderID = '{}' AND Orders.CartID = ProductCart.CartID AND ProductCart.ProductID = Product.ProductID".format(orderID)

    cur = mysql.connection.cursor()
    cur.execute(query)
    res = list(cur.fetchall())
    
    for i in range(len(res)):
        name = res[i]["Name"]
        cur.execute("SELECT * FROM Product WHERE Name = '{}' AND MerchantID = '{}'".format(name,buyerMerchantID))
        product = list(cur.fetchall())
        if not product:
            # no matching result
            uid = uuid.uuid1()
            insertQuery = "INSERT INTO Product VALUES('{}','{}','{}','{}','{}','{}','{}','{}')".format(uid,name,res[i]["Description"],res[i]["Price"],res[i]["Quantity"],res[i]["Category"],buyerMerchantID,"0")
            cur.execute(insertQuery)
            mysql.connection.commit()
        else:
            # matching result
            quantity = str(int(product[0]["Quantity"]) + int(res[i]["Quantity"]))
            updateQuery = "Update Product SET Quantity = '{}' WHERE ProductID = '{}'".format(quantity,product[0]["ProductID"])
            cur.execute(updateQuery)
            mysql.connection.commit()
    cur.close()
    return "Success"