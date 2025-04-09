from flask import request, jsonify
from app import app
from service import *
from models import Suppliers, Goods, Orders

@app.route('/suppliers', methods=['GET'])
def route_get_suppliers():
    suppliers = get_all_suppliers()
    return jsonify([{
        'id': s['id'],
        'company_name': s['company_name'],
        'phone_number': s['phone_number'],
        'representative_name': s['representative_name'],
        'goods': s['goods']  
    } for s in suppliers])


@app.route('/login', methods=['POST'])
def route_login():
    print("Login request received")
    
    if not request.is_json:
        print("Request is NOT JSON")
        return jsonify({'message': 'Invalid request format'}), 400

    data = request.get_json()
    print("Request JSON:", data)

    supplier = get_supplier_by_credentials(data['company_name'], data['password'])
    print("supplier", supplier.id)

    if supplier:
        return jsonify({
            'message': 'Login successful',
            'supplier_id': supplier.id,
            'role': supplier.role  
        })
    
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/suppliers', methods=['POST'])
def route_add_supplier():
    data = request.json
    add_supplier(data)
    return jsonify({'message': 'Supplier added successfully'}), 201

@app.route('/goods/<int:supplier_id>', methods=['GET'])

def route_get_goods(supplier_id):
    goods = get_goods_by_supplier(supplier_id)
    return jsonify([{
        'id': g.id,
        'product_name': g.product_name,
        'price_per_item': g.price_per_item,
        'min_quantity': g.min_quantity
    } for g in goods])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json

    supplier_id = data['supplier_id']
    products = data['products']

    # שליפת הספק מהמסד
    supplier = Suppliers.query.get(supplier_id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404

    # יצירת ההזמנה עם פרטי הספק
    new_order = Orders(
        supplier_id=supplier_id,
        status='new',  # או 'new' אם זה השם שבחרת
        products=products,
        company_name=supplier.company_name,
        representative_name=supplier.representative_name,
        phone_number=supplier.phone_number
    )

    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created'}), 201





@app.route('/orders', methods=['GET'])
def route_get_orders():
    orders = get_all_orders()
    print("orders", orders)
    return jsonify([{
        'id': o.id,
        'supplier_id': o.supplier_id,
        'status': o.status,
        'products': o.products,
        'company_name': o.company_name,
        'representative_name': o.representative_name,
        'phone_number': o.phone_number

    } for o in orders])

@app.route('/orders/<int:supplier_id>', methods=['GET'])
def route_get_order_by_id(supplier_id):
    print("enter")
    supplier = Suppliers.query.get(supplier_id)
    if not supplier:
        return jsonify({'message': 'Supplier not found'}), 404

    orders = Orders.query.filter_by(supplier_id=supplier_id).all()
    print("orders", orders)
    return jsonify([{
        'id': o.id,
        'supplier_id': o.supplier_id,
        'status': o.status,
        'products': o.products,
    } for o in orders])



@app.route('/orders/<int:order_id>/approve', methods=['PUT'])
def route_approve_order(order_id):
    order = Orders.query.get(order_id)
    if order:
        status_changed = approve_order_status(order)
        
        if status_changed:
            db.session.commit()
            return jsonify({'message': f'Order status changed to {order.status}'}), 200
        else:
            return jsonify({'message': 'No status change needed'}), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route('/orders/status/<status>', methods=['GET'])
def get_orders_by_status(status):
    orders = Orders.query.filter_by(status=status).all()
    return jsonify([o.to_dict() for o in orders])

