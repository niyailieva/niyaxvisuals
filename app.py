# YouTube walkthrough video:
# https://www.youtube.com/

# Render link:
#https://niyaxvisuals.onrender.com

import os
from pathlib import Path
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from db import (
    init_db,
    seed_admin,
    get_admin_by_username,
    add_portfolio_item,
    list_portfolio_items,
    save_booking,
    list_bookings,
)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
WORK_DIR = BASE_DIR / "static" / "img" / "work"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")
app.config["UPLOAD_FOLDER"] = str(UPLOAD_DIR)


def is_allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


@app.cli.command("init-db")
def init_db_command():
    init_db()
    seed_admin("admin", generate_password_hash("admin123"))
    print("Database initialized. Admin user: admin / admin123")


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/work")
def work():
    images = []
    if WORK_DIR.exists():
        for p in sorted(WORK_DIR.iterdir()):
            if p.is_file() and p.suffix.lower() in ALLOWED_EXTENSIONS:
                if p.name.lower() not in {"background.jpg", "me.jpg", "logo.png"}:
                    images.append(url_for("static", filename=f"img/work/{p.name}"))
    return render_template("work.html", images=images)


@app.get("/portfolio")
def portfolio():
    items = list_portfolio_items()
    return render_template("portfolio.html", items=items)


@app.route("/admin/portfolio/new", methods=["GET", "POST"])
@admin_required
def admin_portfolio_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip().lower()
        event_name = request.form.get("event_name", "").strip() or None
        description = request.form.get("description", "").strip()
        file = request.files.get("image")

        valid_categories = {"car", "detail", "night", "event", "rolling"}

        if len(title) < 2:
            flash("Title is too short.", "error")
            return redirect(url_for("admin_portfolio_new"))

        if category not in valid_categories:
            flash("Choose a valid category.", "error")
            return redirect(url_for("admin_portfolio_new"))

        if len(description) < 10:
            flash("Description is too short.", "error")
            return redirect(url_for("admin_portfolio_new"))

        if not file or file.filename.strip() == "":
            flash("Please upload an image.", "error")
            return redirect(url_for("admin_portfolio_new"))

        filename = secure_filename(file.filename)
        if not is_allowed(filename):
            flash("Only jpg, png, jpeg and webp are allowed.", "error")
            return redirect(url_for("admin_portfolio_new"))

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        save_name = f"{os.urandom(8).hex()}_{filename}"
        file.save(str(UPLOAD_DIR / save_name))

        add_portfolio_item(
            title=title,
            category=category,
            description=description,
            image_filename=save_name,
            event_name=event_name,
        )

        flash("Portfolio item added.", "ok")
        return redirect(url_for("portfolio"))

    return render_template("admin_portfolio_new.html")


@app.get("/about")
def about():
    return render_template("about.html")


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        shoot_type = request.form.get("shoot_type", "").strip()
        video_style = request.form.get("video_style", "").strip() or None
        message = request.form.get("message", "").strip()

        if len(name) < 2:
            flash("Name is too short.", "error")
            return redirect(url_for("book"))
        if "@" not in email or "." not in email:
            flash("Please enter a valid email.", "error")
            return redirect(url_for("book"))
        if len(shoot_type) < 2:
            flash("Please choose a shoot type.", "error")
            return redirect(url_for("book"))
        if len(message) < 10:
            flash("Message is too short.", "error")
            return redirect(url_for("book"))

        save_booking(
            name=name,
            email=email,
            shoot_type=shoot_type,
            video_style=video_style,
            message=message,
        )
        flash("Booking request sent.", "ok")
        return redirect(url_for("book"))

    return render_template("book.html")


@app.get("/requests")
@admin_required
def requests_page():
    bookings = list_bookings()
    return render_template("requests.html", bookings=bookings)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_admin_by_username(username)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Wrong username or password.", "error")
            return redirect(url_for("login"))

        session["is_admin"] = True
        session["username"] = username
        flash("Logged in.", "ok")
        return redirect(url_for("portfolio"))

    return render_template("login.html")


@app.get("/logout")
def logout():
    session.clear()
    flash("Logged out.", "ok")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)