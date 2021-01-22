from flask import render_template
from flask import request
from models import Book
from database import app,db
from flask import redirect
from flask_graphql import GraphQLView
from schema import schema

@app.route("/", methods=["GET"])
def get_books():
    books = Book.query.all()
    return render_template("home.html",books= books)


@app.route("/created", methods=[ "POST"])
def post_books():
    if request.form:
        book = Book(title=request.form.get("title"))
        db.session.add(book)
        db.session.commit()
        books = Book.query.all()
        return render_template("home.html",books= books)


@app.route("/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    book = Book.query.filter_by(title=oldtitle).first()
    book.title = newtitle
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)

if __name__ == '__main__':
     app.run(host='0.0.0.0')