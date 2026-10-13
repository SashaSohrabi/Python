from flask import Flask, render_template

# To run the Flask app in development, use the command: flask --app server run [--debug]
app = Flask(__name__)
print(__name__)

app_name = "Flask Web Server"


@app.route("/<username>/<int:post_id>")
def hello_world(username: str | None = None, post_id: int | None = None) -> str:
    return render_template(
        "index.html", app_name=app_name, username=username, post_id=post_id
    )


@app.route("/about")
def about() -> str:
    return render_template("about.html", app_name=app_name)
