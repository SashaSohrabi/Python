import csv
from pathlib import Path

from flask import Flask, redirect, render_template, request
from flask.typing import ResponseReturnValue

# To run the Flask app in development, use the command: flask --app server run [--debug]
app = Flask(__name__)

path: Path = Path(__file__).resolve().parent
form_submission_path: Path = path / "form_submissions"


def write_to_file(data: dict[str, str]) -> None:
    with open(form_submission_path / "submitted_form.txt", mode="a") as database:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        database.write(f"\n email: {email}, subject: {subject}, message: {message}")


def write_to_csv(data: dict[str, str]) -> None:
    with open(
        form_submission_path / "submitted_form.csv", mode="a", newline=""
    ) as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]

        csv_writer = csv.writer(
            database2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )

        # Write the header only if the file is empty.
        if database2.tell() == 0:
            csv_writer.writerow(["email", "subject", "message"])

        csv_writer.writerow([email, subject, message])


@app.route("/")
def my_home() -> str:
    return render_template("index.html")


@app.route("/<string:page_name>")
def about(page_name: str) -> str:
    return render_template(f"{page_name}.html")


@app.route("/submit_form", methods=["GET", "POST"])
def submit_form() -> ResponseReturnValue:
    if request.method == "POST":
        try:
            data = request.form.to_dict()
            form_submission_path.mkdir(parents=True, exist_ok=True)
            # write_to_file(data)
            write_to_csv(data)
            return redirect("thankyou", code=303)

        except (KeyError, OSError, csv.Error):
            app.logger.exception("Failed to save form submission")
            return "Could not save your message. Please try again!", 500
    else:
        return "Something went wrong. Please try again!"
