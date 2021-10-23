from django.shortcuts import render

def take_photo(request):
    return render(request, 'filming/take_photo.html')
