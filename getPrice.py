import pyodbc

def get_price_by_barcode(barcode):
    try:
        conn = pyodbc.connect(driver='{SQL Server}', host="192.168.1.220", database="L and N Shoes_Test", user="business", password="system")
        cursor = conn.cursor()
        
        # Query only the price column by filtering on SKU_CODE
        query = "SELECT SKU_E_NAME FROM dbo.SKUMASTER WHERE SKU_CODE = ?"
        cursor.execute(query, (barcode,))
        row = cursor.fetchone()
        if row:
            price = row[0]
            print("Price for barcode", barcode, "is", price)
            return price
        else:
            print("No record found for barcode:", barcode)
            return None

        cursor.close()
        conn.close()
    except pyodbc.Error as e:
        print("Error in connection:", e)
        return None

# Example usage:
get_price_by_barcode("0320007919P")
