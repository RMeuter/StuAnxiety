from django.shortcuts import render

def FAQ(request):
    return render(request, 'FAQ.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')

def choix(request):
    return render(request, 'choix.html')

#def handler404(request):
#    return render(request, 'error/404.html', {}, status=404)
