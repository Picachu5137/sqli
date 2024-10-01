import os
from flask import render_template, session, request, redirect, url_for, flash

from . import app
from . import captcha
from .config import *
from .utils import *


@app.route("/")
def index():
    images = os.listdir(os.path.join(os.path.abspath(os.curdir), "vulnsite", "static", "images"))
    print(images)
    return render_template("index.html", images=images)


@app.route("/login", methods=["POST", "GET"])
def login():
    if session.get("authorized"):
        return redirect(url_for("index"))

    captcha_count = session.get("captcha_count", None)
    if session.get("captcha_count", None) is None:
        session["captcha_count"] = CAPTCHA_COUNT
        captcha_count = CAPTCHA_COUNT

    image, value = captcha.generate_captcha()
    session["value"] = value
    if request.method == "POST":
        if captcha_count <= 0:
            if request.form["login"] == "admin" and request.form["pass"] == "robotboy":
                session["authorized"] = True
                return redirect(url_for('index'))
            elif request.form["login"] != "admin":
                flash("неверный логин")
            else:
                flash("неверный пароль")

    return render_template("login.html", captcha_count=captcha_count, image=image)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route("/check_captcha", methods=["POST"])
def check_captcha():
    req = request.form["value"]
    val = session["value"]
    print(f"{req=}, {val=}")
    if request.form["value"] == session["value"]:
        session["captcha_count"] -= 1
    return redirect(url_for("login"))


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("profile.html")


@app.context_processor
def inject_session():
    return session
