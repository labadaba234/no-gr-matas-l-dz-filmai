from flask import Flask, render_template
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


def get_db_conenection():
    """
    Izveido un atgriež savienojumu ar SQLitle datubāzi.
    """
    db = Path(__file__).parent / "project.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/romance')
def romantika():
    db = get_db_conenection()
    books = db.execute("SELECT * FROM books WHERE genre = 'Romance'").fetchall()
    movies = db.execute("SELECT * FROM movies WHERE genre = 'Romance'").fetchall()
    return render_template("romance.html", books=books, movies=movies)

@app.route("/Romantika")
def about():
    return render_template("romance.html")

@app.route('/fantasy')
def fantazija():
    db = get_db_conenection()
    books = db.execute("SELECT * FROM books WHERE genre = 'Fantasy'").fetchall()
    movies = db.execute("SELECT * FROM movies WHERE genre = 'Fantasy'").fetchall()
    return render_template("fantasy.html", books=books, movies=movies)

@app.route("/Fantāzija")
def abou():
    return render_template("fantasy.html")

@app.route('/horror')
def sausmas():
    db = get_db_conenection()
    books = db.execute("SELECT * FROM books WHERE genre = 'Horror'").fetchall()
    movies = db.execute("SELECT * FROM movies WHERE genre = 'Horror'").fetchall()
    return render_template("horror.html", books=books, movies=movies)

@app.route("/Šausmene")
def abo():
    return render_template("horror.html")

@app.route('/mystery')
def noslepumi():
    db = get_db_conenection()
    books = db.execute("SELECT * FROM books WHERE genre = 'Mystery'").fetchall()
    movies = db.execute("SELECT * FROM movies WHERE genre = 'Mystery'").fetchall()
    return render_template("mystery.html", books=books, movies=movies)

@app.route("/Mistērija/Detektīvi")
def ab():
    return render_template("mystery.html")

@app.route('/thriller')
def trilleris():
    db = get_db_conenection()
    books = db.execute("SELECT * FROM books WHERE genre = 'Thriller'").fetchall()
    movies = db.execute("SELECT * FROM movies WHERE genre = 'Thriller'").fetchall()
    return render_template("thriller.html", books=books, movies=movies)

@app.route("/Trilleris")
def a():
    return render_template("thriller.html")


@app.route('/reviews')
def show_reviews():
    db = get_db_conenection()
    movies_with_reviews = db.execute("SELECT id, name, review FROM movies WHERE review IS NOT NULL AND review != ''").fetchall()
    return render_template("reviews.html", reviews=movies_with_reviews)

@app.route('/reviews/new', methods=['GET', 'POST'])
def new_review():
    db = get_db_conenection()
    if request.method == 'POST':
        movie_id = request.form['movie_id']
        review = request.form['review']
        db.execute("UPDATE movies SET review = ? WHERE id = ?", (review, movie_id))
        db.commit()
        return redirect('/reviews')
    movies = db.execute("SELECT id, name FROM movies").fetchall()
    return render_template("new_review.html", movies=movies)

@app.route('/reviews/edit/<int:id>', methods=['GET', 'POST'])
def edit_review(id):
    db = get_db_conenection()
    if request.method == 'POST':
        review = request.form['review']
        db.execute("UPDATE movies SET review = ? WHERE id = ?", (review, id))
        db.commit()
        return redirect('/reviews')
    movie = db.execute("SELECT id, name, review FROM movies WHERE id = ?", (id,)).fetchone()
    return render_template("edit_review.html", movie=movie)

@app.route('/reviews/delete/<int:id>', methods=['POST'])
def delete_review(id):
    db = get_db_conenection()
    db.execute("UPDATE movies SET review = NULL WHERE id = ?", (id,))
    db.commit()
    return redirect('/reviews')




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)