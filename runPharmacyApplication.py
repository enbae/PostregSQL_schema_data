#! /usr/bin/env python

import psycopg2, sys, datetime

def countNumberOfCustomers (myConn, thePharmacyID):
    try:
        cursor = myConn.cursor()
        cursor.execute("SELECT 1 FROM Pharmacy WHERE pharmacyID = %s", (thePharmacyID,))
        if cursor.fetchone() is None:
            cursor.close()
            return -1
        
        count_sql = "SELECT COUNT(DISTINCT customerID) FROM Purchase WHERE pharmacyID = %s;"
        cursor.execute(count_sql, (thePharmacyID,))
        customer_count = cursor.fetchone()[0]
        # returns the final count
        return customer_count

    finally:
        cursor.close()

# end countNumberOfCustomers


def updateOrderStatus (myConn, currentYear):
    if not (2000 <= currentYear <= 2030):
        return -1
    
    try:
        cursor = myConn.cursor()
        update_sql = """ UPDATE OrderSupply SET status = status || ' AS OF ' || %s WHERE status IN ('pndg', 'dlvd'); """
        cursor.execute(update_sql, (str(currentYear),))

        myConn.commit()
        return cursor.rowcount
    
    finally:
        cursor.close()
# end updateOrderStatus


# deleteSomeOrders (myConn, maxOrderDeletions):
# Besides the database connection, this Python function has one other parameter,
# maxOrderDeletions, which is an integer.



def deleteSomeOrders (myConn, maxOrderDeletions):

        
    try:
        myCursor = myConn.cursor()
        sql = "SELECT deleteSomeOrdersFunction(%s)"
        myCursor.execute(sql, (maxOrderDeletions, ))
    except:
        print("Call of deleteSomeOrdersFunction with argument", maxOrderDeletions, "had error", file=sys.stderr)
        myCursor.close()
        myConn.close()
        sys.exit(-1)
    
    row = myCursor.fetchone()
    myCursor.close()
    return(row[0])

#end deleteSomeOrders


def main():
    port = "5432"
    userID = "cse182"
    pwd = "database4me"

    try:
        myConn = psycopg2.connect(port=port, user=userID, password=pwd)
    except:
        print("Connection to database failed", file=sys.stderr)
        sys.exit(-1)
        
    
    myConn.autocommit = True


    print("countNumberOfCustomers Test")
    for pid in [11, 17, 44, 66]:
        result = countNumberOfCustomers(myConn, pid)
        #reports customer number if the pharmacy exists
        if result >= 0:
            print(f"Number of customers for pharmacy {pid} is {result}")
        else:
            print(f"Error: Pharmacy {pid} does not exist.")
        print()
    
    print("updateOrderStatus Test")
    #Checks for valid year and invalid years
    for year in [1999, 2025, 2035]:
        result = updateOrderStatus(myConn, year)
        if result >= 0:
            print(f"Number of orders whose status values were updated by updateOrderStatus is {result}")
        else:
            print(f"Error: {year} is not a valid year for updateOrderStatus.")
        print()  

    print("deleteSomeOrders Test")
    for maxDel in [2, 4, 3, 1]:
        result = deleteSomeOrders(myConn, maxDel)
        #prints number of deletions if successful
        if result >= 0:
            print(f"Number of orders which were deleted for maxOrderDeletions value {maxDel} is {result}")
        else:
            print(f"Error: Invalid maxOrderDeletions value {maxDel}.")
        print()

  
  
    myConn.close()
    sys.exit(0)
#end

#------------------------------------------------------------------------------
if __name__=='__main__':

    main()

# end
