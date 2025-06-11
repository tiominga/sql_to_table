from django.shortcuts import render

# Create your views here.
def home_index(request):
    """
    Render the home page.
    """
    return render(request, 'home/index.html')