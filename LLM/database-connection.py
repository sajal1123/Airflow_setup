import psycopg2

# Define your connection parameters
db_params = {
    'host': 'localhost',
    'database': 'postgres',
    'user': 'airflow',
    'password': 'airflow',
    'port': '5432',  # Default PostgreSQL port is usually 5432
}

# Establish a connection
connection = psycopg2.connect(**db_params)

# Create a cursor object
cursor = connection.cursor()

# Example: Retrieve data from your table
select_query = "SELECT * FROM news_headlines"

# Execute the select query
cursor.execute(select_query)

# Fetch all rows
rows = cursor.fetchall()

# Print or process the retrieved data
for idx, row in enumerate(rows):
# Create a filename based on the row index or a specific column value
    filename = f'article_{idx + 1}.txt'

    # Open the file in write mode and save row data
    with open('./data/'+filename, 'w') as file:
        for value in row:
            file.write(str(value) + '\n')
# Close the cursor and connection
cursor.close()
connection.close()