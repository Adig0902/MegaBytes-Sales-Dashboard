from flask import Blueprint, redirect, render_template, url_for, request
from sqlalchemy import func 
from .models import DailyStats
from . import db

my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def index():
    daily_stats = DailyStats.query.all()
    return render_template('index.html', daily_stats=daily_stats)

# def index():
#     # Calculate the total income, highest spend, best-selling item, worst-selling item,
#     # MVP staff member, and average basket spend
#     total_income = db.session.query(func.sum(DailyStats.total_income)).scalar()
#     highest_spend = db.session.query(func.max(DailyStats.highest_spend)).scalar()
#     best_selling_item = db.session.query(DailyStats.best_selling_item).order_by(DailyStats.total_income.desc()).first()
#     worst_selling_item = db.session.query(DailyStats.worst_selling_item).order_by(DailyStats.total_income.asc()).first()
#     mvp_staff_member = db.session.query(DailyStats.mvp_staff_member).order_by(DailyStats.total_income.desc()).first()
#     average_basket_spend = db.session.query(func.avg(DailyStats.average_basket_spend)).scalar()

#     return render_template(
#         'index.html',
#         total_income=total_income,
#         highest_spend=highest_spend,
#         best_selling_item=best_selling_item,
#         worst_selling_item=worst_selling_item,
#         mvp_staff_member=mvp_staff_member,
#         average_basket_spend=average_basket_spend
#     )


@my_view.route("/add/monday", methods=['POST'])
def add_monday():    
    return redirect(url_for('my_view.index'))


@my_view.route("/plot")
def plot():
    # Display charts
    return render_template("plot.html")

@my_view.route("/void")
def void_data():
    # Display void transaction data
    return render_template("void.html")