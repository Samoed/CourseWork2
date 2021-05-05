import sqlite3
import pandas as pd

conn = sqlite3.connect("bd.db")
cursor = conn.cursor()

sql = "SELECT * FROM vkrShort"
for row in cursor.execute(sql):
    print(row)

df = pd.read_csv('data/vkrTextShort.csv')
print(df.shape)

arr = []
for i in df.index:
    # print(df.loc[i,:])
    s = f"INSERT INTO vkrShort VALUES ('{df.loc[i, 'Unnamed: 0']}','{df.loc[i, 'link_vkr']}', '{str(df.loc[i, 'name_vkr'])}','{df.loc[i, 'name_student']}','{df.loc[i, 'name_prof']}','{df.loc[i, 'campus']}','{df.loc[i, 'programm']}', '{df.loc[i, 'grade']}','{df.loc[i, 'year']}','{df.loc[i, 'link_file']}','{str(df.loc[i, 'shortText'])}')"
    # print(s)
    try:
        cursor.execute(s)
        conn.commit()
    except:
        arr.append(str(i))

conn.close()
