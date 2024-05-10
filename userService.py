from flask import Blueprint, jsonify, request
from database import UserProduct
from datetime import datetime

# import random

userService = Blueprint('userService', __name__, url_prefix='/user')


@userService.post('/report')
def report_with_date():
    temp_start_date = request.get_json().get('start_date', '')
    temp_end_date = request.get_json().get('end_date', '')

    if len(temp_start_date) < 1 or len(temp_end_date) < 1:
        return jsonify({"error": "Please enter the valid start date and end date"}), 400

    start_temp = str(temp_start_date).split('-')
    end_temp = str(temp_start_date).split('-')

    for i in start_temp:
        if len(i) > 4:
            print(i)
            return jsonify({"error": "Invalid start date entered"}), 400
    for j in end_temp:
        if len(j) > 4:
            print(j)
            return jsonify({"error": "Invalid end date entered"}), 400

    start_date = datetime.strptime(temp_start_date, '%Y-%m-%d')
    end_date = datetime.strptime(temp_end_date, '%Y-%m-%d')

    data = []
    is_data_exists = False
    original_total = 0
    discount_total = 0
    user_data = UserProduct.query.filter_by().all()
    for user in user_data:
        # user.Recent_date = f"{random.randint(2023, 2024)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
        # db.session.commit()
        if start_date <= datetime.strptime(user.Recent_date, '%Y-%m-%d') <= end_date:
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
        return jsonify({"error": "Data not exists"}), 404


@userService.post('/get-all-old-users')
def get_user_items():
    phone_number = request.get_json().get('Phone_number', '')
    if len(phone_number) < 1:
        return jsonify({"error": "please enter the required details"}), 400

    user_products = UserProduct.query.filter_by().all()
    if len(user_products) < 1:
        return jsonify({"error": "Database table is empty"}), 404
    temp_user_product = []
    is_user_found = False
    for up in user_products:
        if str(up.Phone_number) == str(phone_number):
            is_user_found = True
            temp = {
                "User_name": up.User_name,
                "Phone_number": up.Phone_number,
                "Product_name": up.Product_name,
                "Exp_date": up.Exp_date,
                "Original_price": up.Original_price,
                "Discount_price": up.Discount_price,
                "Tablet_quantity": up.Tablet_quantity,
                "Recent_date": up.Recent_date
            }
            temp_user_product.append(temp)

    if is_user_found:
        return jsonify({"data": temp_user_product}), 200
    else:
        return jsonify({"error": "user not found"}), 404


@userService.post('/get-all-old-users-with-date')
def get_phone_items():
    phone_number = request.get_json().get('Phone_number', '')
    recent_date = request.get_json().get('Recent_date', '')
    r_date = datetime.strptime(recent_date, '%Y-%m-%d')
    if len(recent_date) == 3 or len(phone_number) < 1:
        return jsonify({"error": "please enter the required details"}), 400

    user_products = UserProduct.query.filter_by().all()
    if len(user_products) < 1:
        return jsonify({"error": "Database table is empty"}), 404

    temp_user_product = []
    is_user_found = False
    for up in user_products:
        if (str(up.Phone_number) == str(phone_number)
                and datetime.strptime(up.Recent_date, '%Y-%m-%d') == r_date):
            is_user_found = True
            temp = {
                "User_name": up.User_name,
                "Phone_number": up.Phone_number,
                "Product_name": up.Product_name,
                "Exp_date": up.Exp_date,
                "Original_price": up.Original_price,
                "Discount_price": up.Discount_price,
                "Tablet_quantity": up.Tablet_quantity,
                "Recent_date": up.Recent_date
            }
            temp_user_product.append(temp)

    if is_user_found:
        return jsonify({"data": temp_user_product}), 200
    else:
        return jsonify({"error": "user not found"}), 404
