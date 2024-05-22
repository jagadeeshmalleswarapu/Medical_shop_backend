from flask import request, jsonify, Blueprint
from database import db, CheckOut, UserProduct, Product
from datetime import date

addToCartService = Blueprint('addToCartService', __name__, url_prefix='/cart')


# Remove one item from the cart
@addToCartService.post('/remove-one')
def remove_one():
    product_name = request.get_json().get('Product_name', '')
    if len(product_name) < 1:
        return jsonify({
            "error": "please enter the product"
        }), 400
    view_cart = CheckOut.query.filter_by().all()
    is_found = False
    if len(view_cart) <= 0:
        return jsonify({"message": "Cart is empty"}), 404
    for item in view_cart:
        if item.Product_name == product_name:
            is_found = True
            db.session.delete(item)
            db.session.commit()
            break
    if is_found:
        return jsonify({"message": f"{product_name} has been removed from the Cart!!!"}), 200
    else:
        return jsonify({"error": "Item not found"})


# Removing all items from cart
@addToCartService.get('/remove-all-items')
def remove_all_items():
    view_cart = CheckOut.query.filter_by().all()
    if len(view_cart) <= 0:
        return jsonify({"message": "Cart is empty"}), 404

    for item in view_cart:
        db.session.delete(item)
        db.session.commit()
    return jsonify({"message": "All the items has been removed from the Cart!!!"}), 200


# Adding items to Cart
@addToCartService.post('/add-to-cart')
def adding_item_to_cart():
    product_name = request.get_json().get('Product_name', '')
    tablet_quantity = request.get_json().get('Tablet_quantity', '')

    if len(product_name) < 1 or int(tablet_quantity) == 0 or tablet_quantity == '':
        return jsonify({"error": "Please enter valid quantity"}), 400

    product = Product.query.filter_by(Product_name=product_name).first()
    if product is None:
        return jsonify({"error": "Product is not found"}), 404
    view_product_cart = CheckOut.query.filter_by(Product_name=product_name).first()
    if view_product_cart is not None:
        return jsonify({
            "error": f"{product_name} is already exists in the Cart, please remove from cart to add more quantity"}), 400

    if int(tablet_quantity) > int(product.Tablet_quantity):
        return jsonify({
            "error": f"You entered more tablet quantity - ({tablet_quantity}) than existing tablet quantity - ({product.Tablet_quantity})"}), 400
    exp_date = product.Exp_date
    original_price = product.Original_price
    discount_price = product.Discount_price
    total_discount_price = str(int(discount_price) * int(tablet_quantity))
    total_original_price = str(int(original_price) * int(tablet_quantity))

    # Add validations here
    checkout = CheckOut(Product_name=product_name, Exp_date=exp_date, Original_price=total_original_price,
                        Discount_price=total_discount_price, Tablet_quantity=tablet_quantity)
    db.session.add(checkout)
    db.session.commit()

    return jsonify({
        "message": f"{product_name} has been added to cart"
    })


# Get all items from cart
@addToCartService.get('/get-cart')
def get_cart():
    view_cart = CheckOut.query.filter_by().all()
    if len(view_cart) <= 0:
        return jsonify({"message": "Cart is empty"}), 404
    a = 0
    data = []
    for items in view_cart:
        a = a + 1
        temp = {
            "id": items.id,
            "Product_name": items.Product_name,
            "Exp_date": items.Exp_date,
            "Original_price": items.Original_price,
            "Discount_price": items.Discount_price,
            "Tablet_quantity": items.Tablet_quantity
        }
        data.append(temp)
    return jsonify({
        "cart": data,
        "cart_total": f"{a}"
    }), 200


# Last step to print and add user details with product details
@addToCartService.post('/add-user-cart')
def add_items_with_users():
    user_name = request.get_json().get('User_name', '')
    user_name = str(user_name).lower()
    phone_number = request.get_json().get('Phone_number', '')
    recent_date = date.today().strftime('%Y-%m-%d')

    # need to add validations
    if len(user_name) < 1 or len(phone_number) < 1:
        return jsonify({"error": "Please enter Customer name and phone no."}), 400
    view_cart = CheckOut.query.filter_by().all()
    if len(view_cart) <= 0:
        return jsonify({"error": "Cart is empty"}), 404
    data = []
    total = 0
    count = 0
    for it in view_cart:
        temp = {
            "id": it.id,
            "Product_name": it.Product_name,
            "Exp_date": it.Exp_date,
            "Original_price": it.Original_price,
            "Discount_price": it.Discount_price,
            "Tablet_quantity": it.Tablet_quantity
        }
        total = total + int(it.Discount_price)
        count = count + int(it.Tablet_quantity)
        data.append(temp)

    for item in view_cart:
        user_product = UserProduct(User_name=user_name, Phone_number=phone_number, Recent_date=recent_date,
                                   Product_name=item.Product_name, Exp_date=item.Exp_date,
                                   Original_price=item.Original_price,
                                   Discount_price=item.Discount_price, Tablet_quantity=item.Tablet_quantity)
        db.session.add(user_product)
        db.session.commit()

    # Need to subtract the tablet qty
    for item_subtract in view_cart:
        temp_tablet_qty = item_subtract.Tablet_quantity
        product = Product.query.filter_by(Product_name=item_subtract.Product_name).first_or_404()
        sub_val = abs(int(temp_tablet_qty) - int(product.Tablet_quantity))
        product.Tablet_quantity = str(sub_val)
        product.Sheet_quantity = str(sub_val / int(product.Sheet_tablet_count_default))
        db.session.commit()

    # Need to delete the record if it has value '0'.
    products = Product.query.filter_by().all()
    for pro in products:
        tablet_num = int(pro.Tablet_quantity)
        if tablet_num <= 0:
            db.session.delete(pro)
            db.session.commit()

    # Need to delete one by one
    for item_del in view_cart:
        delete_single_product = CheckOut.query.filter_by(Product_name=item_del.Product_name).first_or_404()
        db.session.delete(delete_single_product)
        db.session.commit()

    return jsonify({
        "data": data,
        "User_name": user_name,
        "Phone_number": phone_number,
        "Recent_date": recent_date,
        "total": str(total),
        "count": str(count)
    }), 200
