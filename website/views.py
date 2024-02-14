from flask import Blueprint, redirect, render_template, url_for, request
from .models import DailyStats
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def index():
    return render_template("index.html")


@my_view.route("/days")
def daily_stats():
    # Display daily stats
    return render_template("days.html")

@my_view.route("/plot")
def plot():
    # Display charts
    return render_template("plot.html")

@my_view.route("/void")
def void_data():
    # Display void transaction data
    return render_template("void.html")