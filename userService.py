from flask import Blueprint, jsonify, request
from database import UserProduct, db
from datetime import datetime
import random

userService = Blueprint('userService', __name__, url_prefix='/user')


@userService.post('/report')
def report_with_date():
    temp_start_date = request.get_json().get('start_date', '')
    temp_end_date = request.get_json().get('end_date', '')

    if len(temp_start_date) and len(temp_end_date) is 3:
        return jsonify({"error": "Please enter the start date and end date"}), 400

    start_date = datetime.strptime(temp_start_date, '%d-%m-%Y')
    end_date = datetime.strptime(temp_end_date, '%d-%m-%Y')

    data = []
    is_data_exists = False
    original_total = 0
    discount_total = 0
    user_data = UserProduct.query.filter_by().all()
    for user in user_data:
        # user.Recent_date = f"{random.randint(1, 28)}-{random.randint(1, 12)}-{random.randint(2023, 2024)}"
        # db.session.commit()
        if start_date <= datetime.strptime(user.Recent_date, '%d-%m-%Y') <= end_date:
            is_data_exists = True
            original_total = original_total + int(user.Original_price)
            discount_total = discount_total + int(user.Discount_price)
            temp = {
                "User_name": user.User_name,
                "Phone_number": user.Phone_number,
                "Product_name": user.Product_name,
                "Exp_date": user.Exp_date,
                "Original_price": user.Original_price,
                "Discount_price": user.Discount_price,
                "Tablet_quantity": user.Tablet_quantity,
                "Recent_date": user.Recent_date
            }
            data.append(temp)

    if is_data_exists:
        return jsonify({
            "data": data,
            "original_total": original_total,
            "discount_total": discount_total
        }), 200
    else:
        return jsonify({"message": "not found"}), 404
