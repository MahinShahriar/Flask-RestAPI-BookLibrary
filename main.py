from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='tmplate')
app.secret_key = "super-secret-key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@0.0.0.0:3306/Mahin_web"
db = SQLAlchemy(app)

class Book_list(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)

def book_list():
  all_books = []
  books = Book_list.query.filter_by().all()
  if books:
    for book in books:
      all_books.append({
              "id" : book.id,
              "name" : book.name,
              "title": book.title,
              "author": book.author
            })
    return all_books
  else:
    return False


@app.route("/books", methods=["GET","POST"])
def books():
  book_l = book_list()
  if request.method=='GET':
    if book_l: return jsonify(book_list())
    else: return  "Nothing Found", 404
  
  if request.method=="POST":
    name   = request.form['name']
    title  = request.form['title']
    author = request.form['author']
    new_obj = Book_list(name=name,title=title,author=author)
    db.session.add(new_obj)
    db.session.commit()
    return jsonify(book_list()), 201

@app.route("/books/<int:id>", methods=["GET","PUT","DELETE"])
def single_book(id):
  book = Book_list.query.filter_by(id=id).first()
  if book:
    if request.method=="GET":
      return jsonify({
                "id" : book.id,
                "name" : book.name,
                "title": book.title,
                "author": book.author
               })
    if request.method=="PUT":
      if request.form['name']: book.name = request.form['name'] 
      if request.form['title']: book.title = request.form['title'] 
      if request.form['author']:book.author = request.form['author'] 
      db.session.commit()    
      updated_obj = {
                "id" : id,
                "name" : book.name,
                "title": book.title,
                "author": book.author
                }
      return jsonify(updated_obj)
      
    if request.method=="DELETE":
      db.session.delete(book)
      db.session.commit()
      return jsonify(book_list())
  
  else:
    return "Book Not Found", 404

if __name__ == '__main__':
    with app.app_context():
      db.create_all()
    app.run(debug= True, port=6969) 