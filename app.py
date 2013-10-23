from flask import Flask, render_template, request, redirect, session, url_for, flash
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/")
def index():
    if session.get("user_id"):

        model.connect_to_db()
        user_id = session.get('user_id')
        username = model.get_username_by_user_id(user_id)
        model.CONN.close()
        return redirect(url_for("view_user", username=username))
    else:
        return render_template("index.html")


@app.route("/", methods=["POST"])
def process_login():
    model.connect_to_db()

    submitted_username = request.form.get('username')
    submitted_password = request.form.get("password")

    my_id = model.authenticate(submitted_username, hash(submitted_password))

    if my_id != None:
        session['user_id'] = my_id
        model.CONN.close()
        return redirect(url_for("view_user", username=submitted_username))
    else:
        flash("Incorrect username or password")
        return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out.")
    return redirect(url_for("index"))
  

@app.route("/user/<username>")
def view_user(username):

    model.connect_to_db()

    owner_id = model.get_user_id_by_username(username)
    posts = model.get_posts_by_user_id(owner_id)
    if owner_id != None:
        model.CONN.close()
        return render_template("view_user.html", username = username,
                                                posts = posts)
    else:
        flash("User not found")
        return redirect(url_for("index"))


@app.route("/user/<username>", methods = ["POST"])
def view_post(username):

    model.connect_to_db()
    post_text = request.form.get('post_text')
    author_id = session.get('user_id')
    owner_id = model.get_user_id_by_username(username)
    model.insert_post(owner_id, author_id, post_text)
    model.CONN.close()

    return redirect(url_for("view_user", username = username))


@app.route("/register", methods = ["POST"])
def register():
    model.connect_to_db()
    #check if username already exists in db
        #throw and error
    submitted_username = request.form.get('username')
    submitted_password = request.form.get('password')
    submitted_password_verify = request.form.get('password_verify')
    if model.get_user_id_by_username(submitted_username) != None:
        flash("Username already exists")
        model.CONN.close()
        return render_template('register.html')
    else:
        if submitted_password != submitted_password_verify:
            flash("Passwords do not match")
            model.CONN.close()
            return render_template('register.html')
        else: 
            model.insert_user(submitted_username, hash(submitted_password))
            model.CONN.close()
            return render_template(url_for("view_user", username=submitted_username))




if __name__ == "__main__":
    app.run(debug = True)
