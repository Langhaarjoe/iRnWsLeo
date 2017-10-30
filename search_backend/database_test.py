import psycopg2 as sql

conn = sql.connect("dbname=postgres user=postgres password=postgres")
db = conn.cursor()
#db.execute("""INSERT INTO words (word, id, td_idf) VALUES (%s, %s, %s);""", ('test2', 2, 0.01))
db.execute("""INSERT INTO words (word, id, td_idf) VALUES (%s, %s, %s);""", ('test2', 2, 0.01))
#db.execute("SELECT word FROM words;")
db.execute("SELECT word FROM words;")
print(db.fetchall())
conn.commit()
db.close()
conn.close()