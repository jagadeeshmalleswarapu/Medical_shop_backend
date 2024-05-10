from flask import Flask, jsonify
from flask_cors import CORS
from addToCartService import addToCartService
from database import db
from productService import productService
from userService import userService

app = Flask(__name__)
CORS(app=app, origins=['*'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productDB.db'


@app.get('/')
def test():
    # db.create_all()
    return jsonify({
        "message": "Welcome to the add product"
    })


app.register_blueprint(productService)
app.register_blueprint(addToCartService)
app.register_blueprint(userService)

db.app = app
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=1234)
