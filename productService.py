from flask import request, Blueprint, jsonify
from database import db, Product
import validators

productService = Blueprint('productService', __name__, url_prefix='/product')


# Add products
@productService.post('/add_items')
def add_items_into_db():
    inv_no = request.get_json().get('inv_no', '')
    inv_date = request.get_json().get('inv_date', '')
    product_name = request.get_json().get('product_name', '')
    batch_no = request.get_json().get('batch_no', '')
    exp_date = request.get_json().get('exp_date', '')
    or_price = request.get_json().get('or_price', '')
    dc_price = request.get_json().get('dc_price', '')
    sheet_qty = request.get_json().get('sheet_qty', '')
    tablet_qty = request.get_json().get('tablet_qty', '')
    sheet_tablet_qty = request.get_json().get('sheet_tablet_qty', '')

    # Validation
    if (len(inv_no) < 1 or len(inv_date) < 1 or len(product_name) < 1 or len(batch_no) < 1
            or len(exp_date) < 1 or len(or_price) < 1 or len(dc_price) < 1
            or len(sheet_qty) < 1 or len(tablet_qty) < 1 or len(sheet_tablet_qty) < 1):
        return jsonify({"error": "Some required fields are empty, please fill it"}), 400

    if Product.query.filter_by(Product_name=product_name).first():
        return jsonify({"error": "Product already exists, please add new one..."}), 409

    # Adding products into Product table
    products_ref = Product(Invoice_number=inv_no, Invoice_date=inv_date, Product_name=product_name,
                           Batch_no=batch_no, Exp_date=exp_date, Original_price=or_price,
                           Discount_price=dc_price, Sheet_quantity=sheet_qty, Tablet_quantity=tablet_qty,
                           Sheet_tablet_count_default=sheet_tablet_qty)
    db.session.add(products_ref)
    db.session.commit()

    return jsonify({
        "inv_no": inv_no,
        "inv_date": inv_date,
        "productName": product_name,
        "batchNo": batch_no,
        "exp_date": exp_date,
        "original": or_price,
        "discount": dc_price,
        "sheetQTY": sheet_qty,
        "TabletQTY": tablet_qty,
        "Sheet_tablet_count_default": sheet_tablet_qty
    }), 201


# Getting all products
@productService.get('/get_all')
def get_all():
    data = []
    products = Product.query.filter_by().all()

    for i in products:
        temp = {
            "id": i.id,
            "Invoice_number": i.Invoice_number,
            "Invoice_date": i.Invoice_date,
            "Product_name": i.Product_name,
            "Batch_no": i.Batch_no,
            "Exp_date": i.Exp_date,
            "Original_price": i.Original_price,
            "Discount_price": i.Discount_price,
            "Sheet_quantity": i.Sheet_quantity,
            "Tablet_quantity": i.Tablet_quantity,
            "Sheet_tablet_count_default": i.Sheet_tablet_count_default,
            "Created_at": i.Created_at,
            "Updated_at": i.Updated_at
        }
        data.append(temp)
    return jsonify(data), 200


# Getting single product with product name
@productService.get('/<string:pro_name>')
def get_product_with_name(pro_name):
    if pro_name is None:
        return jsonify({"error": "Product name is missing, please enter..."}), 400

    product = Product.query.filter_by(Product_name=pro_name).first()
    # if Product.query.filter_by(Product_name=pro_name).first() is not None:
    if product is None:
        return jsonify({"error": "Product is not found"}), 404

    return jsonify(
        {
            "id": product.id,
            "Invoice_number": product.Invoice_number,
            "Invoice_date": product.Invoice_date,
            "Product_name": product.Product_name,
            "Batch_no": product.Batch_no,
            "Exp_date": product.Exp_date,
            "Original_price": product.Original_price,
            "Discount_price": product.Discount_price,
            "Sheet_quantity": product.Sheet_quantity,
            "Tablet_quantity": product.Tablet_quantity,
            "Sheet_tablet_count_default": product.Sheet_tablet_count_default,
            "Created_at": product.Created_at,
            "Updated_at": product.Updated_at
        }
    )
