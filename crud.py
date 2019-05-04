from model import db,Customer,Product,Order, ProductStatusEnum

def new_cusotmer(email,password,address,phone,name,data):
    existing_user = Customer.query.filter_by(email=email).first()
    if existing_user:
        return "Email already exist"
    customer = Customer(email,password,address,phone,name)
    customer.fb_link = data.get('fb_link')

    db.session.add(customer)
    db.session.commit()

        # uid = unique id
def new_product(order_id,link,description,quantity):

    product = Product(order_id,link,description,quantity)

    db.session.add(product)
    db.session.commit()


def new_order(customer_id,product_list):

    order = Order(customer_id)

    db.session.add(order)
    db.session.commit() # order id has to be generated first to add products in order

    for product in product_list:

        link = product.get('link')
        description = product.get('description')
        quantity = product.get('quantity')

        new_product(order.id,link,description,quantity)


def get_all_products():
    return Product.query.all()

def get_all_orders():
    return Order.query.all()

def update_product(product_id,data):

    product = Product.query.get(product_id)

    product.link = data.get('link') or product.link
    product.description = data.get('description') or product.description
    product.quantity = data.get('quantity',product.quantity)
    product.name =  data.get('name',product.name)
    product.price = data.get('price',product.price)
    product.shipping_charge = data.get('shipping_charge',product.shipping_charge)
    product.tax = data.get('tax', product.tax)
    product.weight_charge = data.get('weight_charge',product.weight_charge)

    for status in ProductStatusEnum:
        if(data.get('status') == ProductStatusEnum.status.value()):
            product.status = ProductStatusEnum(status) or product.status


    db.session.add(product)
    db.session.commit()

def add_new_product_order(order_id,data):
    link = data.get('link')
    description = data.get('description')
    quantity = data.get('quantity')

    new_product(order_id,link,description,quantity)

def delete_product(product_id):
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()


def delete_order(order_id):
    order = Product.query.get(order_id)
    db.session.delete(order)
    db.session.commit()










