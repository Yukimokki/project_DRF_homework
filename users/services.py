import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product(name):
    """Creates product in stripe"""
    product = stripe.Product.create(name=name)
    return product


def create_price(price, name):
    """creates products price"""
    product_id = create_product(name).id
    response = stripe.Price.create(
        currency="rub",
        unit_amount=int(price * 100),
        product=product_id
    )
    return response


def create_session(price, name):
    """Creates session in Stripe and returns session ID and URL"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/courses/",
        line_items=[{"price": create_price(price, name), "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
