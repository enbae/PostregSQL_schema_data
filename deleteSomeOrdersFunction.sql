CREATE OR REPLACE FUNCTION deleteSomeOrdersFunction(maxOrderDeletions INT)
RETURNS INT AS $$
DECLARE
    total_deleted INT := 0;
    supplier_data RECORD;
    deleted_count INT;
BEGIN
    IF maxOrderDeletions <= 0 THEN
        RETURN -1;
    END IF;

    FOR supplier_data IN
        WITH SupplierStats AS (
            SELECT
                s.supplierID,
                s.supplierName,
                COUNT(*) FILTER (WHERE o.orderDate > DATE '2024-01-05') AS future_orders,
                COUNT(*) FILTER (WHERE o.orderDate <= DATE '2024-01-05' AND o.status = 'cnld') AS cancelled_past_orders
            FROM Supplier s
            JOIN OrderSupply o ON s.supplierID = o.supplierID
            GROUP BY s.supplierID, s.supplierName
        )
        SELECT *
        FROM SupplierStats
        WHERE cancelled_past_orders > 0 AND future_orders > 0
        ORDER BY cancelled_past_orders DESC, supplierName ASC
    LOOP
        IF (total_deleted + supplier_data.future_orders) <= maxOrderDeletions THEN
            DELETE FROM OrderSupply
            WHERE supplierID = supplier_data.supplierID
              AND orderDate > DATE '2024-01-05';

            GET DIAGNOSTICS deleted_count = ROW_COUNT;
            total_deleted := total_deleted + deleted_count;
        ELSE
            RETURN total_deleted;
        END IF;
    END LOOP;

    RETURN total_deleted;
END;
$$ LANGUAGE plpgsql;