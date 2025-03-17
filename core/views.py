from django.shortcuts import render, redirect
from .forms import ItemForm
from .models import Item


def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a list view or confirmation page after saving
            return redirect('item_list')  # Ensure you have an URL named 'item_list'
    else:
        form = ItemForm()
    
    return render(request, 'core/create_item.html', {'form': form})

def item_list(request):
    items = Item.objects.all()
    return render(request, 'core/item_list.html', {'items': items})