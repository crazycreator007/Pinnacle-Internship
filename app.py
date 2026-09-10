import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = "blog.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            published INTEGER DEFAULT 1
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_db()

    posts = conn.execute(
        "SELECT * FROM posts WHERE published = 1 ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("index.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
def create_post():

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        conn = get_db()

        conn.execute(
            "INSERT INTO posts (title, content, published) VALUES (?, ?, 1)",
            (title, content)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    return render_template("create.html")

@app.route("/post/<int:post_id>")
def view_post(post_id):

    conn = get_db()

    post = conn.execute(
        "SELECT * FROM posts WHERE id = ? AND published = 1",
        (post_id,)
    ).fetchone()

    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template("post.html", post=post)

@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):

    conn = get_db()

    post = conn.execute(
        "SELECT * FROM posts WHERE id = ?",
        (post_id,)
    ).fetchone()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        conn.execute(
            "UPDATE posts SET title = ?, content = ? WHERE id = ?",
            (title, content, post_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("home"))

    conn.close()

    return render_template("edit.html", post=post)


@app.route("/delete/<int:post_id>")
def delete_post(post_id):

    conn = get_db()

    conn.execute(
        "DELETE FROM posts WHERE id = ?",
        (post_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)