import pandas as pd

def cargar_datos(name):
    df = pd.read_csv("./data/" + name + ".csv", sep=',', encoding = 'latin1', index_col=False)
    return df

def guardar_datos(df, nombre):
    df.to_csv("./data/" + nombre + ".csv" , encoding = 'latin1', sep=',', index=False)

def leer_datos():

    ## Dimension city
    city = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/dimension_city.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False) # recuerden cambiar XX por el número de su grupo
    guardar_datos(city, "dimension_city_no_procesados")
    
    ## Dimension Customer
    customer = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/dimension_customer.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False)
    guardar_datos(customer, "dimension_customer_no_procesados")
    
    ## Dimension Date
    date = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/dimension_date.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False)
    guardar_datos(date, "dimension_date_no_procesados")

    ## Dimension Employee
    employee = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/dimension_employee.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False)
    guardar_datos(employee, "dimension_employee_no_procesados")

    ## Dimension Stock item
    stock_item = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/dimension_stock_item.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False)
    guardar_datos(stock_item, "dimension_stock_item_no_procesados")
    
    ## Fact Table
    fact_order = pd.read_csv("http://bigdata-cluster4-01.virtual.uniandes.edu.co:50070/webhdfs/v1/user/monitorbi/datalakeBI/fact_order.csv?op=OPEN&user.name=cursobi25", sep=',', encoding = 'latin1', index_col=False)
    guardar_datos(fact_order, "fact_order_no_procesados")

def procesar_datos():
    
    # Llamar a la funcion auxiliar de leer datos
    leer_datos()

    ## Dimension city:
        # Datos vacios procesados.
        # Datos sin errores
        # Columnas con unico valor descartadas
        # No vemos duplicados.
    datos_dim_city = cargar_datos('dimension_city_no_procesados')
    datos_dim_city = datos_dim_city.dropna()
    datos_dim_city = datos_dim_city.drop(["row ID"],axis = 1)
    guardar_datos(datos_dim_city, "dimension_city")
    
    ## Dimension Customer:
        # Datos vacios procesados.
        # Datos sin errores.
        # No vemos duplicados.
        # Cambiamos los codigos postales a enteros.
    datos_dim_customer = cargar_datos('dimension_customer_no_procesados')
    datos_dim_customer = datos_dim_customer.dropna()
    datos_dim_customer["Postal_Code"] = datos_dim_customer["Postal_Code"].astype("int64")
    datos_dim_customer["Customer"] = datos_dim_customer["Customer"].astype("string").apply(lambda x: x.replace("'",""))
    guardar_datos(datos_dim_customer, "dimension_customer")
    
    ## Dimension Date:
        # No hay datos vacios.
        # No hay columnas con unico valor.
        # Datos sin errores.
        # No vemos duplicados.
       
    datos_dim_date = cargar_datos('dimension_date_no_procesados')
    guardar_datos(datos_dim_date, "dimension_date")
    
    ## Dimension Employee:
        # Datos vacios procesados
        # No hay columnas con unico valor.
        # Datos sin errores.
        # Vemos una mayoria de datos duplicados, pero decidimos no eliminarlos por la consisntencia de la tabla de hechos.
    datos_dim_employee = cargar_datos('dimension_employee_no_procesados')
    datos_dim_employee = datos_dim_employee.dropna()
    guardar_datos(datos_dim_employee, "dimension_employee")
    
    ## Dimension Stock item:
        # Datos vacios procesados
        # No hay columnas con unico valor.
        # Datos sin errores.
        # Vemos una mayoria de datos duplicados, donde realizamos el manejo mencionado previamente.
    datos_dim_stock_item = cargar_datos('dimension_stock_item_no_procesados')
    datos_dim_stock_item["Stock_Item"] = datos_dim_stock_item["Stock_Item"].astype("string").apply(lambda x: x.replace("'",""))
    cols = ["Color","Selling_Package","Buying_Package","Brand","Size_val"]
    for col in cols:
        datos_dim_stock_item[col] = datos_dim_stock_item[col].fillna("Not Provided")
    cols = ['Tax_Rate','Unit_Price', 'Recommended_Retail_Price', 'Typical_Weight_Per_Unit']
    for col in cols:
        datos_dim_stock_item[col] = datos_dim_stock_item[col].apply(lambda x: x.replace(',','.')).astype("float64")
    guardar_datos(datos_dim_stock_item, "dimension_stock_item")
    
    
    ## Fact table:
    fact_order = cargar_datos('fact_order_no_procesados')
    fact_order['order_date_key'] = pd.to_datetime(fact_order["order_date_key"])
    fact_order['picked_date_key'] = pd.to_datetime(fact_order["picked_date_key"])
    fact_order['package'] = fact_order['package'].astype("string")
    fact_order.columns = fact_order.columns.str.title()
    guardar_datos(fact_order, "fact_order")
