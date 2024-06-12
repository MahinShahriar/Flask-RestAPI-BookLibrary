from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import sqlite3

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = "super-secret-key"
  
def db_connection():
  conn = None
  try:
    conn = sqlite3.connect('books.sqlite3')
  except sqlite.error as e:
    print(e)
  return conn

Admin = {"admin" : "1234"} # this data should be fetch from database on production.
@auth.verify_password
def verify(username, password):
  if not (username and password):
    return False
  try:
    return Admin.get(username)==password
  except:
    return False

#============= Unprotected ===============
@app.route("/api/books", methods=["GET"])
def books():
  conn = db_connection()
  cursor = conn.cursor()
  if request.method=='GET':
    cursor = conn.execute("SELECT * FROM book")
    books = [
      dict(id=row[0],name=row[1], title=row[2], author=row[3]) for row in cursor.fetchall()
      ]
    if books:
      return jsonify(books)
    else:
      return jsonify({"message":"No books available in library  !"})

@app.route("/api/books/<int:id>", methods=["GET"])
def single_book(id):
  conn = db_connection()
  cursor = conn.cursor()
  if request.method=="GET":
    cursor = conn.execute(f"SELECT * FROM book WHERE id={id}")
    book = [
      dict(id=row[0],name=row[1], title=row[2], author=row[3]) for row in cursor.fetchall()
      ]
    if book:
      return jsonify(book)
    else:
      return jsonify({"message":f"No books available with id : {id} !"})

#=========== Protected ==============
@app.route("/api/books/dashboard", methods=["POST"])
@auth.login_required
def book_post():
  conn = db_connection()
  cursor = conn.cursor()
  if request.method=="POST":
    name   = request.form['name']
    title  = request.form['title']
    author = request.form['author']
    sql = """ INSERT INTO book(name,title,author) VALUES(?, ?, ?) """
    cursor = cursor.execute(sql, (name,title,author))
    conn.commit()
    return jsonify({'message': f'Book: {name} added successfully !'})

@app.route("/api/books/dashboard/<int:id>", methods=["PUT","DELETE"])
@auth.login_required
def s_book(id):
  conn = db_connection()
  cursor = conn.cursor()
  cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id ={id})")
  result = cursor.fetchone()[0]
  if result:
    if request.method=="PUT":
        if request.form['name']:
          name = request.form['name']
          sql = """ UPDATE book SET name=? WHERE id=?"""
          cursor = cursor.execute(sql, (name,id))
          conn.commit()
          
        if request.form['title']:
          title = request.form['title']
          sql = """ UPDATE book SET title=? WHERE id=?"""
          cursor = cursor.execute(sql, (title,id))
          conn.commit()
        
        if request.form['author']:
          author = request.form['author']
          sql = """ UPDATE book SET author=? WHERE id=?"""
          cursor = cursor.execute(sql, (author,id))
          conn.commit()
        return jsonify({'message':'Updated successfully !'})
        
    if request.method=="DELETE":
      sql = """ DELETE FROM book WHERE id=? """
      cursor = cursor.execute(sql,(id,))
      conn.commit()
      return jsonify({'message': f'Book no :{id} successfully deleted from library !'})
  
  else:
    return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug= True) 
