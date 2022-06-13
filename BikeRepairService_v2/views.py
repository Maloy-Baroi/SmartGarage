from django.shortcuts import render


def developersView(request):
    return render(request, 'Developers.html')


