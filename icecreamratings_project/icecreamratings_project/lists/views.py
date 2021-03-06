from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.http import HttpRequest
from django.http import HttpResponse

from lists.models import Item, List
from lists.forms import ItemForm, DUPLICATE_ITEM_ERROR, ExistingListItemForm




def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):

    list_ = List.objects.get(id=list_id)
    items = Item.objects.all().filter(list=list_.id)
    form = ExistingListItemForm(for_list=list_, data=request.POST or None)

    if form.is_valid():
        try:
            form.save()
            return redirect(list_)
        except ValidationError:
            form.errors.update({'text': DUPLICATE_ITEM_ERROR})
    return render(request, 'list.html', {'list': list_, 'form': form, 'items': items})


def new_list(request):

    form = ItemForm(data=request.POST)

    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form": form})
