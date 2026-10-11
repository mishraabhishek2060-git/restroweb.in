from decimal import Decimal
from urllib.parse import quote

from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactMessageForm
from .models import MenuItem, Order, OrderItem

def home(request):
    return render(request, 'index.html')

def menu(request):
    items = MenuItem.objects.all()
    errors = []

    if request.method == 'POST':
        name = request.POST.get('customer_name', '').strip()
        phone = request.POST.get('customer_phone', '').strip()
        phone_digits = ''.join(char for char in phone if char.isdigit())
        selected = []

        if not name:
            errors.append('Please enter your name.')
        if not 7 <= len(phone_digits) <= 15:
            errors.append('Please enter a valid phone number.')

        for item in items:
            try:
                quantity = int(request.POST.get(f'quantity_{item.pk}', '0'))
            except (TypeError, ValueError):
                errors.append(f'Enter a valid quantity for {item.name}.')
                continue
            if quantity < 0 or quantity > 50:
                errors.append(f'Quantity for {item.name} must be between 0 and 50.')
                continue
            if quantity == 0:
                continue
            plate_size = request.POST.get(f'plate_{item.pk}', 'full')
            if plate_size not in OrderItem.PlateSize.values:
                errors.append(f'Choose a valid plate size for {item.name}.')
                continue
            if plate_size == OrderItem.PlateSize.HALF and item.effective_half_price is None:
                errors.append(f'The half plate price for {item.name} has not been set yet.')
                continue
            unit_price = item.effective_half_price if plate_size == OrderItem.PlateSize.HALF else item.price
            selected.append((item, plate_size, quantity, unit_price))

        if not selected:
            errors.append('Choose at least one menu item to order.')

        if not errors:
            total = sum((price * quantity for _, _, quantity, price in selected), Decimal('0.00'))
            with transaction.atomic():
                order = Order.objects.create(customer_name=name, customer_phone=phone, total=total)
                OrderItem.objects.bulk_create([
                    OrderItem(
                        order=order,
                        item_name=item.name,
                        plate_size=plate_size,
                        quantity=quantity,
                        unit_price=price,
                        line_total=price * quantity,
                    )
                    for item, plate_size, quantity, price in selected
                ])
            return redirect('order_detail', public_id=order.public_id)

    return render(request, 'menu.html', {'items': items, 'errors': errors})


def order_detail(request, public_id):
    order = get_object_or_404(Order.objects.prefetch_related('items'), public_id=public_id)
    number = ''.join(char for char in settings.RESTAURANT_WHATSAPP_NUMBER if char.isdigit())
    lines = [f"Order #{order.pk} — {order.customer_name}"]
    lines.extend(
        f"{item.quantity} x {item.item_name} ({item.get_plate_size_display()}) — ₹{item.line_total:.2f}"
        for item in order.items.all()
    )
    lines.extend((f"Total: ₹{order.total:.2f}", 'Gokul Sweet & Restaurant, Maharajganj, Hanuman Gari, near petrol pump'))
    whatsapp_url = f"https://wa.me/{number}?text={quote(chr(10).join(lines))}" if number else ''
    return render(request, 'order_detail.html', {'order': order, 'whatsapp_url': whatsapp_url})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactMessageForm()

    return render(request, 'contact.html', {'form': form})


def contact_success(request):
    return render(request, 'contact.html', {'form': ContactMessageForm(), 'success': True})
