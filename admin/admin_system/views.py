from django.shortcuts import render

def dashboard(request):
    return render(request, 'admin_pages/index.html')

def documentation(request):
    return render(request, 'admin_pages/documentation.html')
