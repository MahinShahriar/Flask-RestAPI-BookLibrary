import sqlite3

conn = sqlite3.connect("books.sqlite3")

cursor = conn.cursor()
# sql_query = """ INSERT INTO book(name,title,author)
#                 VALUES('The war','Secret tips for destroying war thinking','Mahin')
#             """
# cursor.execute(sql_query)