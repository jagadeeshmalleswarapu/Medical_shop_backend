from flask import request, jsonify, Blueprint
from database import db, CheckOut, UserProduct, Product
from datetime import date

addToCartService = Blueprint('addToCartService', __name__, url_prefix='/cart')


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
    exp_date = request.get_json().get('Exp_date', '')
    original_price = request.get_json().get('Original_price', '')
    discount_price = request.get_json().get('Discount_price', '')
    tablet_quantity = request.get_json().get('Tablet_quantity', '')

    product = Product.query.filter_by(Product_name=product_name).first()
    if product is None:
        return jsonify({"error": "Product is not found"}), 404

    if int(tablet_quantity) > int(product.Tablet_quantity):
        return jsonify({
            "message": f"You entered more tablet quantity - ({tablet_quantity}) than existing tablet quantity - ({product.Tablet_quantity})"})

    # Add validations here
    checkout = CheckOut(Product_name=product_name, Exp_date=exp_date, Original_price=original_price,
                        Discount_price=discount_price, Tablet_quantity=tablet_quantity)
    db.session.add(checkout)
    db.session.commit()

    return jsonify({
        "message": f"{product_name} has been added to cart"
    })


# Last step to print and add user details with product details
@addToCartService.post('/add-user-cart')
def add_items_with_users():
    user_name = request.get_json().get('User_name', '')
    phone_number = request.get_json().get('Phone_number', '')
    recent_date = date.today().strftime('%d-%m-%Y')

    # need to add validations
    view_cart = CheckOut.query.filter_by().all()
    if len(view_cart) <= 0:
        return jsonify({"message": "Cart is empty"}), 404
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
        "message": f"{user_name}-{phone_number} has been added"
    })
