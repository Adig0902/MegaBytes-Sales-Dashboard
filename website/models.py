from . import db

class DailyStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_name = db.Column(db.String(10), nullable=False)
    total_income = db.Column(db.Float, nullable=False)
    highest_spend = db.Column(db.Float, nullable=False)
    best_selling_item = db.Column(db.String(50), nullable=False)
    worst_selling_item = db.Column(db.String(50), nullable=False)
    mvp_staff_member = db.Column(db.String(50), nullable=False)
    average_basket_spend = db.Column(db.Float, nullable=False)
    