from models import db, Suppliers, Goods, Orders
from sqlalchemy.orm import joinedload


def get_all_suppliers():
    # נשתמש ב-joinedload כדי לטעון גם את המוצרים יחד עם הספקים
    suppliers = Suppliers.query.filter_by(role='supplier').options(joinedload(Suppliers.goods)).all()
    
    result = []  # מִתחילים רשימה ריקה
    for supplier in suppliers:
        goods_list = [{
            'product_name': g.product_name,
            'price_per_item': g.price_per_item,  # הוסף את המחיר לכל מוצר
            'min_quantity': g.min_quantity  # הוסף את הכמות המינימלית לכל מוצר
        } for g in supplier.goods]  # בדוק אם יש את המאפיינים הללו
        result.append({
            'id': supplier.id,
            'company_name': supplier.company_name,
            'phone_number': supplier.phone_number,
            'representative_name': supplier.representative_name,
            'goods': goods_list
        })
    
    return result

    


def get_supplier_by_credentials(company_name, password):
    return Suppliers.query.filter_by(company_name=company_name, password=password).first()

def add_supplier(data):
    new_supplier = Suppliers(**data)
    db.session.add(new_supplier)
    db.session.commit()

def get_goods_by_supplier(supplier_id):
    return Goods.query.filter_by(supplier_id=supplier_id).all()

def create_order(supplier_id):
    new_order = Orders(supplier_id=supplier_id)
    db.session.add(new_order)
    db.session.commit()

def get_all_orders():
    return Orders.query.all()

def get_orders_by_supplier_id(supplier_id):
    if supplier_id == 28:
        suppliers = Suppliers.query.filter(Suppliers.id != 28).all()
        
        result = []
        for s in suppliers:
            goods = Goods.query.filter_by(supplier_id=s.id).all()
            goods_list = [g.name for g in goods]  
            
            result.append({
                'id': s.id,
                'company_name': s.company_name,
                'phone_number': s.phone_number,
                'representative_name': s.representative_name,
                'goods': goods_list
            })
        
        return result
    else:
        return Orders.query.filter_by(supplier_id=supplier_id).all()

def approve_order_status(order):
    if order.status == 'new':
        order.status = 'Pending'
        return True
    elif order.status == 'Pending':
        order.status = 'Completed'
        return True
    else:
        return False