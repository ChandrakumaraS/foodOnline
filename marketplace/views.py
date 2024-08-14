from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor, openingHour
from django.db.models import Prefetch
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import date, datetime

# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count' : vendor_count,
    }
    return render(request, 'marketplace/listing.html',context)


def vendor_details(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    opening_hour = openingHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')

    # Check current day's opening hours
    today_date = date.today()
    today = today_date.isoweekday()
    current_opening_hour = openingHour.objects.filter(vendor=vendor, day=today)



    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories': categories,
        'cart_items' : cart_items,
        'opening_hour': opening_hour,
        'current_opening_hour': current_opening_hour,
    }
    return render(request, 'marketplace/vendor_details.html',context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                print(fooditem, food_id)

                # check if the user already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    
                    # increase cart quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased the cart quantity', 'cart_counter':get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'Added Food to the cart', 'cart_counter':get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})

        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request!'})
    else:   
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # check if the food item exist
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                print(fooditem, food_id)

                # check if the user already added that food to the cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity >= 1:
                        # Decrease the cart quantity
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status':'Success', 'cart_counter':get_cart_counter(request), 'qty': checkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed', 'message':'We do not have this item in your cart'})
            except:
                return JsonResponse({'status':'Failed', 'message':'This food does not exist'})

        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request!'})
    else:   
        return JsonResponse({'status':'login_required', 'message':'Please login to continue'})

@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # check if the cart item is exist
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success', 'message':'Cart Item has been deleted', 'cart_counter':get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed', 'message':'Cart item does not exist'})
        else:
            return JsonResponse({'status':'Failed', 'message': 'Invalid Request!'})

def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    keyword = request.GET['keyword']

    # Get vendor id that has the food the user is looking for
    fetch_vendors_by_fooditem = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
    vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditem) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
    
    vendor_count = vendors.count()
    context ={
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/listing.html', context)