from django.shortcuts import render, redirect
from .models import Entry
from .forms import EntryForm
# Create your views here.

def index(request):
    return render(request, 'blog/index.html')

def blog(request):
    entries = Entry.objects.order_by('-date_posted')
    context = {'entries' : entries}
    return render(request, 'blog/blog.html', context)

def add(request):
    if request.method=='POST':         # POST request
        form = EntryForm(request.POST) # request.Post contains the data
        
        if form.is_valid():
            form.save() # Save the data in the database
            return redirect('/blog/blog/') # Blog main page
    
    else: # Not POST request
        form = EntryForm() # Create empty EntryForm
    
    context = {'form' : form} # Pass the form to template
    return render(request, 'blog/add.html', context)