# PostregSQL_schema_data


This project defines a mini pharmacy management database in PostgreSQL and a Python application that interacts with it. It demonstrates:

- SQL schema design (customers, pharmacies, drugs, suppliers, purchases, orders)
- Loading data with `COPY`
- A PL/pgSQL stored function to delete orders under constraints
- Python functions for querying and updating the database using `psycopg2`

---

## 1. Database Schema & Data

- `lab4_create.sql`  
  - Creates schema `Lab4` and tables: `Customer`, `Pharmacy`, `Drug`, `Supplier`, `Purchase`, `DrugsInPurchase`, `OrderSupply`.  
- `load_lab4.sql`  
  - Populates those tables with sample data for customers, pharmacies, drugs, purchases, and supply orders.

## 2. PL/pgSQL Function: `deleteSomeOrdersFunction`

- `deleteSomeOrdersFunction.sql`  
  - Defines:

    ```sql
    deleteSomeOrdersFunction(maxOrderDeletions INT) RETURNS INT
    ```

  - Logic:
    - Computes, per supplier, how many past cancelled orders (status `cnld` on or before `2024-01-05`) and how many future orders (after `2024-01-05`) they have.
    - Considers only suppliers with both cancelled past orders and future orders.
    - Orders them by `cancelled_past_orders DESC, supplierName ASC`.
    - Iterates through that list, deleting future orders for each supplier while the total deleted rows stay ≤ `maxOrderDeletions`.
    - Returns the total number of deleted orders, or `-1` if `maxOrderDeletions <= 0`.

## 3. Python Application

- `runPharmacyApplication.py`  
  - Connects to PostgreSQL using `psycopg2` and defines three main functions:

    ```python
    countNumberOfCustomers(myConn, thePharmacyID)
    updateOrderStatus(myConn, currentYear)
    deleteSomeOrders(myConn, maxOrderDeletions)
    ```

  - **`countNumberOfCustomers`**
    - Checks if a pharmacy with the given ID exists.
    - If not, returns `-1`.
    - Otherwise, returns the number of distinct customers who made purchases at that pharmacy.

  - **`updateOrderStatus`**
    - Accepts a `currentYear` argument.
    - If `currentYear` is not between 2000 and 2030, returns `-1`.
    - Otherwise, updates `OrderSupply.status` for rows whose status is `'pndg'` or `'dlvd'` by appending `' AS OF <currentYear>'`.
    - Returns the number of rows updated.

  - **`deleteSomeOrders`**
    - Calls the PostgreSQL function `deleteSomeOrdersFunction(maxOrderDeletions)`.
    - Returns the integer result from the function (number of deleted rows, or `-1` on error/invalid input).

  - `main()` runs small test loops for each function and prints the results.

---

## How to Run

  - \i lab4_create.sql;
  - \i load_lab4.sql;
  - \i deleteSomeOrderFunction.sql;
- Install python dependencie
  - pip install psycopg2-binary
