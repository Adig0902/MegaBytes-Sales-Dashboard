from flask import Blueprint, redirect, render_template, url_for, request
from sqlalchemy import func 
from .models import DailyStats
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/add",methods=["POST"])
def add():
    # try:
        day_name=request.form.get("day_name")
        total_income=request.form.get("total_income",type = float)
        highest_spend = request.form.get("highest_spend",type = float)
        best_selling_item=request.form.get("best_selling_item")
        worst_selling_item=request.form.get("worst_selling_item")
        mvp_staff_member=request.form.get("mvp_staff_member")
        average_basket_spend=request.form.get("average_basket_spend")
        new_daily_stats=DailyStats(total_income=total_income,highest_spend=highest_spend,best_selling_item=best_selling_item,worst_selling_item=worst_selling_item,mvp_staff_member=mvp_staff_member,day_name=day_name,average_basket_spend=average_basket_spend)
        db.session.add(new_daily_stats)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    # except:
    #     message="There was an error, make sure all the values are entered"
    #     return redirect(url_for("my_view.home",message=message))


@my_view.route("/")
def home():
    daily_stats = DailyStats.query.all()
    return render_template('home.html', daily_stats=daily_stats)
    


@my_view.route("/monday")
def monday():
    return render_template("monday.html")

@my_view.route("/tuesday")
def tuesday():
    return render_template("tuesday.html")

@my_view.route("/wednesday")
def wednesday():
    return render_template("wednesday.html")

@my_view.route("/thursday")
def thursday():
    return render_template("thursday.html")

@my_view.route("/friday")
def friday():
    return render_template("friday.html")

@my_view.route("/saturday")
def saturday():
    return render_template("saturday.html")

@my_view.route("/sunday")
def sunday():
    return render_template("sunday.html")

@my_view.route("/plot")
def plot():
    # Display charts
    return render_template("plot.html")

@my_view.route("/void")
def void_data():
    # Display void transaction data
    return render_template("void.html")