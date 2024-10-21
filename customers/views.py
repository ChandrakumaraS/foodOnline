from venv import logger
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
import simplejson as json

from orders.models import Order, OrderedFood


import logging

logger = logging.getLogger(__name__)

@login_required(login_url='login')
def cprofile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # profile = get_object_or_404(UserProfile, user = request.user)
    
    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        print(request.FILES)
        user_form = UserInfoForm(request.POST, instance=request.user)
        
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile Updated")
            logger.debug(f"Uploaded files: {request.FILES}")
            logger.debug(f"Profile picture: {profile_form.cleaned_data.get('profile_picture')}")
            logger.debug(f"Cover photo: {profile_form.cleaned_data.get('cover_photo')}")
            return redirect('cprofile')

            
        else:
            logger.error(profile_form.errors)
            logger.error(user_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'profile': profile,
    }
    
    return render(request, 'customers/cprofile.html', context)

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'customers/my_orders.html', context)

@login_required(login_url='login')
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order': order,
            'ordered_food': ordered_food,
            'subtotal': subtotal,
            'tax_data': tax_data,
        }

        return render(request, 'customers/order_details.html', context)

    except:
        return redirect('customer')

    