import sqlite3
import pandas as pd

conn = sqlite3.connect("bd.db")
cursor = conn.cursor()

sql = "SELECT * FROM People"
for row in cursor.execute(sql):
    print(row)

df = pd.read_csv('data/people.csv')
for i in df.index:
    cursor.execute(
        f"INSERT INTO People VALUES ('{df.loc[i, 'Unnamed: 0']}','{df.loc[i, 'name']}', '{df.loc[i, 'link']}')")
conn.commit()
conn.close()
