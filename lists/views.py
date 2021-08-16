"""view function has two jobs: processing user input, and returning an appropriate response"""

from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']  # var holds POST request or empty string
    #     Item.objects.create(text=new_item_text)  # .objects.create using to create new Item without .save()
    # """:return dictionary which maps template variable names to their values,
    #         so we can use it for the POST case as well as the normal case"""
    # return render(request, 'home.html')

    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world/')
    #
    # items = Item.objects.all()
    # return render(request, 'home.html', {'items': items})

    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world/')
    # return render(request, 'home.html')

    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})


def new_list(request):
    """New list """
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')  # redirect for solve double submit problem


def add_item(request, list_id):
    """Add URLs for adding a new item to an existing list via POST"""
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/') # redirect for solve double submit problem
