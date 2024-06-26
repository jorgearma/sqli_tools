### SQL Injection Tool
This repository hosts a Python script designed for automating and exploring SQL Injections in web applications. The project's motivation was threefold: to gain a deeper understanding of MySQL technology, to learn task automation using Python, and to delve into the concept of SQL injections.

### important
To use this SQL injection script, it is necessary to know the content length. Additionally, the login system must be vulnerable to SQL injection attacks, and the database should be MySQL.

#### Purpose
The primary purpose of this script is educational, enabling users to:
- Dynamically determine the number of columns in a database table using SQL injection techniques.
- Perform SQL injection attacks to extract sensitive information from the database, such as database versions, schema names, tables, and columns.
- Extract specific data from database tables, such as user credentials, using advanced SQL injection techniques.

#### Features
- **Column Inference**: Uses a brute-force strategy to determine the number of columns in the target table.
- **SQL Injection Attacks**: Implements union-based SQL attacks to extract confidential information from the database.
- **Dynamic Input**: Accepts command-line arguments to specify the target URL, expected content length, keyword for filtering the response, and form field names (`email` and `password`).

#### Usage Instructions
1. **Setup**: Ensure Python is installed along with the `requests` library.
2. **Determining Content-Length**: Utilize the --content option to specify the expected length of the response during a typical login attempt on the target URL, achievable through tools like Burp Suite.
3. **Executing the Script**: Run the script with appropriate arguments from the command line:


```
python s9.py http://example.com/login --content 33490 --keyword Welcome 
```


- `http://example.com/login`: URL of the vulnerable login page.
- `--content 33490`: Expected length of the response body during a normal login attempt,  achievable through tools like Burp Suite.
- `--keyword Welcome`: Optional keyword to filter the response content  If not filtered, the script retrieves the full HTML content of the page, including all visible and hidden elements. This can be overwhelming and may include unnecessary information for the purpose.

4. **Output**: The script will display discovered information such as the number of columns, database version, schema names, table names, column names, and extracted data based on user input.

#### Considerations
- **Security and Legality**: Ensure proper permissions before testing and demonstrating SQL injection vulnerabilities.
- **Educational Use**: This tool is created for educational purposes to showcase Python programming skills and understanding of SQL injection vulnerabilities.

#### Author
- **Name**: jorgearma
- **Contact**: batman signal
- **GitHub Repository**: github.com/jorgearma






