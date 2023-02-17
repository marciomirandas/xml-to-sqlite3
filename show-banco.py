import pandas as pd
import sqlite3


con = sqlite3.connect('banco.db')
cur = con.cursor()

cur.execute("SELECT * FROM registros")

resultados = cur.fetchall()

df = pd.DataFrame(resultados)


print(df)

df.to_excel('resultados.xlsx')