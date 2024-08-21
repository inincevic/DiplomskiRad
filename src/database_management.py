import psycopg2


# Connecting to the database using my connection string
CONNECTION = "postgres://tsdbadmin:icpv9i2l4ewanuzw@nc0exan2js.pephiae70q.tsdb.cloud.timescale.com:30892/tsdb?sslmode=require"
conn = psycopg2.connect(CONNECTION)
cursor = conn.cursor()

table_name = "temperatures_IPv6"

# Dropping tables
# sql = """DROP TABLE recorded_temperatures_IPv4"""
# cursor.execute(sql)
# conn.commit()

# Creating tables
cursor.execute(f"""
    CREATE TABLE {table_name} (
        id SERIAL PRIMARY KEY,
        device VARCHAR(100),
        time TIMESTAMP,
        temperature FLOAT(1)
        );
        """)
conn.commit()
print(f"Table '{table_name}' created successfully.")

#     # Read data from the table
#     cursor.execute(f"SELECT * FROM {table_name};")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)


# Closing the connection
if conn:
    cursor.close()
    conn.close()


# # connection string for postgredb ----- DELETE BEFORE PUSHING TO GIT
# # postgres://tsdbadmin:icpv9i2l4ewanuzw@nc0exan2js.pephiae70q.tsdb.cloud.timescale.com:30892/tsdb?sslmode=require