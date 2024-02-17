from flask import Blueprint, redirect, render_template, url_for, request
from sqlalchemy import func
from .models import DailyStats
from . import db
import pandas as pd
import matplotlib
import os

matplotlib.use("Agg")
import matplotlib.pyplot as plt



id_for_day = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday",
}
my_view = Blueprint("my_view", __name__)

def weekly_summary(daily_stats, df):
    summary = {}
    summary["total_income"] = sum([d.total_income for d in daily_stats])
    summary["highest_spend"] = max([d.highest_spend for d in daily_stats])
    summary["best_selling_item"] = max(
        set([d.best_selling_item for d in daily_stats]),
        key=lambda x: [d.best_selling_item for d in daily_stats].count(x),
    )
    summary["worst_selling_item"] = min(
        set([d.worst_selling_item for d in daily_stats]),
        key=lambda x: [d.worst_selling_item for d in daily_stats].count(x),
    )
    summary["mvp_staff_member"] = max(
        set([d.mvp_staff_member for d in daily_stats]),
        key=lambda x: [d.mvp_staff_member for d in daily_stats].count(x),
    )
    # Calculate the overall weekly average basket spend from df
    summary["average_basket_spend"] = df["average_basket_spend"].mean()
    return summary


@my_view.route("/add", methods=["POST"])
def add():
    try:
        day_name = request.form.get("day_name").title()
        total_income = request.form.get("total_income", type=float)
        highest_spend = request.form.get("highest_spend", type=float)
        best_selling_item = request.form.get("best_selling_item").title()
        worst_selling_item = request.form.get("worst_selling_item").title()
        mvp_staff_member = request.form.get("mvp_staff_member").title()
        average_basket_spend = request.form.get("average_basket_spend", type=float)
        new_daily_stats = DailyStats(
            total_income=total_income,
            highest_spend=highest_spend,
            best_selling_item=best_selling_item,
            worst_selling_item=worst_selling_item,
            mvp_staff_member=mvp_staff_member,
            day_name=day_name,
            average_basket_spend=average_basket_spend,
        )
        db.session.add(new_daily_stats)
        db.session.commit()
        return redirect(url_for("my_view.home"))
    except Exception as e:
        print(f"Error:{e}")
        message = "There was an error, make sure all the values are entered"
        return redirect(url_for("my_view.home", message=message))


@my_view.route("/")
def home():
    message = request.args.get("message", None)
    daily_stats = DailyStats.query.all()

    if len(daily_stats) > 0:
        df = pd.DataFrame(
            [
                (
                    r.id,
                    r.day_name,
                    r.total_income,
                    r.highest_spend,
                    r.best_selling_item,
                    r.worst_selling_item,
                    r.mvp_staff_member,
                    r.average_basket_spend,
                )
                for r in daily_stats
            ],
            columns=[
                "id",
                "day_name",
                "total_income",
                "highest_spend",
                "best_selling_item",
                "worst_selling_item",
                "mvp_staff_member",
                "average_basket_spend",
            ],
        )
        weekly_stats = weekly_summary(daily_stats,df)
        # Calculate weekly income and update the graph
        days_of_week = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        weekly_income = [
            df[df["day_name"] == day]["total_income"].sum() for day in days_of_week
        ]

        # Plot the weekly income graph
        plt.style.use("ggplot")
        plt.bar(days_of_week, weekly_income)
        plt.xlabel("Day of the Week")
        plt.ylabel("Total Income")
        plt.title("Weekly Income Summary")
        plt.xticks(rotation=45, ha="right")
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

        # Save the plot to a BytesIO object
        # img = BytesIO()
        plt.savefig("website/static/images/dynamic_graph.png", format="png")
        # img.seek(0)
        plt.close()

        # Encode the image as base64
        # img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")

        mvp_name = df["mvp_staff_member"].mode()[0]
        max_spend = df["total_income"].max()
        highest_spend = df["highest_spend"].max()
        highest_spend_day = df.loc[df["highest_spend"].idxmax(), "day_name"]
        best_selling_item = df["best_selling_item"].mode()[0]
        worst_selling_item = df["worst_selling_item"].mode()[0]

        days = [id_for_day.get(r.id) for r in daily_stats]
        profit = df["total_income"].values

        return render_template(
            "home.html",
            daily_stats=daily_stats,
            weekly_stats=weekly_stats,
            days=days,
            profit=profit,
            mvp_name=mvp_name,
            max_spend=max_spend,
            highest_spend=highest_spend,
            highest_spend_day=highest_spend_day,
            best_selling_item=best_selling_item,
            worst_selling_item=worst_selling_item,
            message=message,
            # img_base64=img_base64,
        )
    else:
        return render_template("home.html", daily_stats=daily_stats, message=message)




@my_view.route("/monday")
def monday():
    monday_data = DailyStats.query.filter_by(day_name="Monday").first()
    return render_template("monday.html", figures=monday_data)


@my_view.route("/tuesday")
def tuesday():
    tuesday_data = DailyStats.query.filter_by(day_name="Tuesday").first()
    return render_template("tuesday.html", figures=tuesday_data)


@my_view.route("/wednesday")
def wednesday():
    wednesday_data = DailyStats.query.filter_by(day_name="Wednesday").first()
    return render_template("wednesday.html", figures=wednesday_data)


@my_view.route("/thursday")
def thursday():
    thursday_data = DailyStats.query.filter_by(day_name="Thursday").first()
    return render_template("thursday.html", figures=thursday_data)


@my_view.route("/friday")
def friday():
    friday_data = DailyStats.query.filter_by(day_name="Friday").first()
    return render_template("friday.html", figures=friday_data)


@my_view.route("/saturday")
def saturday():
    saturday_data = DailyStats.query.filter_by(day_name="Saturday").first()
    return render_template("saturday.html", figures=saturday_data)


@my_view.route("/sunday")
def sunday():
    sunday_data = DailyStats.query.filter_by(day_name="Sunday").first()
    return render_template("sunday.html", figures=sunday_data)


@my_view.route("/void")
def void():
    # Assuming the text file is named "void_transaction_data_week.txt" and is in the "static/data_results/week_insight_folder" directory
    file_path = os.path.join("website","static", "data_results", "week_insight_folder", "void_transaction_data_week.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()
    except FileNotFoundError:
        # Handle the case where the file is not found
        text_content = "Weekly transaction data not available."

    return render_template("void.html", text=text_content)