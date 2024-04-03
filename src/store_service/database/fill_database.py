
from database.models.models import Product
from sqlmodel import Session, select

products = [
    Product(name="Product 1", category="Category 1",
            price=10, available_stock=100),
    Product(name="Product 2", category="Category 1",
            price=20, available_stock=200),
    Product(name="Product 3", category="Category 2",
            price=30, available_stock=300),
]


def fill_products(engine):
    with Session(engine) as session:
        for product in products:
            q = select(Product).where(Product.name == product.name)
            
            user = session.execute(q).first()

            if not user:
                session.add(product)
                session.commit()


def fill_database(engine):
    fill_products(engine)
