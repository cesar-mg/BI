from utils.file_util import cargar_datos

# city insertion
def insert_query_city(**kwargs):
    insert = f"INSERT INTO city (City_Key,City,State_Province,Country,Continent,Sales_Territory,Region,Subregion,Latest_Recorded_Population) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"({row.City_Key},\'{row.City}\',\'{row.State_Province}\',\'{row.Country}\',\'{row.Continent}\',\'{row.Sales_Territory}\',\'{row.Region}\',\'{row.Subregion}\',{row.Latest_Recorded_Population});\n"
    return insertQuery

# customer insertion
def insert_query_customer(**kwargs):
    insert = f"INSERT INTO customer (Customer_Key,Customer,Bill_To_Customer,Category,Buying_Group,Primary_Contact,Postal_Code) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"({row.Customer_Key},\'{row.Customer}\',\'{row.Bill_To_Customer}\',\'{row.Category}\',\'{row.Buying_Group}\',\'{row.Primary_Contact}\',{row.Postal_Code});\n"
    return insertQuery

# date insertion
def insert_query_date(**kwargs):
    insert = f"INSERT INTO date_table (Date_key,Day_Number,Day_val,Month_val,Short_Month,Calendar_Month_Number,Calendar_Year,Fiscal_Month_Number,Fiscal_Year) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"(\'{row.Date_key}\',{row.Day_Number},{row.Day_val},\'{row.Month_val}\',\'{row.Short_Month}\',{row.Calendar_Month_Number},{row.Calendar_Year},{row.Fiscal_Month_Number},{row.Fiscal_Year});\n"
    return insertQuery
# employee insertion
def insert_query_employee(**kwargs):
    insert = f"INSERT INTO employee (Employee_Key,Employee,Preferred_Name,Is_Salesperson) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"({row.Employee_Key},\'{row.Employee}\',\'{row.Preferred_Name}\',{row.Is_Salesperson});\n"
    return insertQuery

# stock item insertion
def insert_query_stock(**kwargs):
    insert = f"INSERT INTO stockitem (Stock_Item_Key,Stock_Item,Color,Selling_Package,Buying_Package,Brand,Lead_Time_Days,Quantity_Per_Outer,Is_Chiller_Stock,Tax_Rate,Unit_Price,Recommended_Retail_Price,Typical_Weight_Per_Unit) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"({row.Stock_Item_Key},\'{row.Stock_Item}\',\'{row.Color}\',\'{row.Selling_Package}\',\'{row.Buying_Package}\',\'{row.Brand}\',{row.Lead_Time_Days},{row.Quantity_Per_Outer},{row.Is_Chiller_Stock},{row.Tax_Rate},{row.Unit_Price},{row.Recommended_Retail_Price},{row.Typical_Weight_Per_Unit} );\n"
    return insertQuery
# fact order insert
def insert_query_fact_order(**kwargs):
    insert = f"INSERT INTO fact_order (Order_Key,City_Key,Customer_Key,Stock_Item_Key,Order_Date_Key,Picked_Date_Key,Salesperson_Key,Picker_Key,Package,Quantity,Unit_Price,Tax_Rate,Total_Excluding_Tax,Tax_Amount,Total_Including_Tax) VALUES "
    insertQuery = ""
    dataframe = cargar_datos(kwargs['csv_path'])
    for index, row in dataframe.iterrows():
        insertQuery += insert + f"({row.Order_Key},{row.City_Key},{row.Customer_Key},{row.Stock_Item_Key},\'{row.Order_Date_Key}\',\'{row.Picked_Date_Key}\',{row.Salesperson_Key},{row.Picker_Key},\'{row.Package}\',{row.Quantity},{row.Unit_Price},{row.Tax_Rate},{row.Total_Excluding_Tax},{row.Tax_Amount}, {row.Total_Including_Tax});\n"

    return insertQuery