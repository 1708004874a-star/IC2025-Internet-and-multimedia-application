from django.db.models import Count
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Item
# Create your views here.

def index(request):
    item = Item.objects.all()
    high_price_items = Item.objects.filter(unit_price__gte=4000)
    old_items = Item.objects.filter(created_date__year__lt = datetime.now().year - 5)
    item_summary = Item.objects.values('type').annotate(total_no=Count('id'))
    item_summary2 = Item.objects.values('brand').annotate(total_no=Count('id'))
    context = {
        'item': item,
        'high_price_items': high_price_items,
        'old_items': old_items,
        'item_summary': item_summary,
        'item_summary2': item_summary2,
    }

    return render(request, 'inventory/index.html', context)
