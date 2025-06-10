from .cart import CartSession

def cart_processor(request):
    cart = CartSession(session=request.session)
    return{"cart":cart}