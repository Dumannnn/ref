from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import EatingItem, EatingItemDish, \
    Dish


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, item_id):
    cart = Cart(request)
    eating_item = get_object_or_404(EatingItem, id=item_id)
    dish = request.POST.get('dish')

    if dish:
        try:
            dish_obj = Dish.objects.get(name=dish)
            eating_item_dish = EatingItemDish.objects.get(eating_item=eating_item,
                                                              dish=dish_obj)
            if not eating_item_dish.available:
                return redirect('cart:cart_detail')
        except Dish.DoesNotExist:
            return redirect('cart:cart_detail')
        except EatingItemDish.DoesNotExist:
            return redirect('cart:cart_detail')
    else:
        available_dishes = eating_item.dishes.filter(eatingitemdish__available=True)
        if available_dishes.exists():
            dish_obj = available_dishes.first()
            dish = dish_obj.name
        else:
            return redirect('cart:cart_detail')

    cart.add(eating_item, dish)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    eating_item = get_object_or_404(EatingItem, id=item_id)
    cart.remove(eating_item)
    return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = Cart(request)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        eating_item = get_object_or_404(EatingItem, id=item_id)

        if quantity > 0:
            cart.add(eating_item, cart.cart[str(item_id)]['dish'], quantity)
        else:
            cart.remove(eating_item)

        return redirect('cart:cart_detail')
    