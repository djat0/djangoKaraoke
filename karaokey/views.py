from django.shortcuts import render


def songbook(request):
    return render(request, "karaokey/songbook.html")


def songlyrics(request):
    return render(request, "karaokey/songlyrics.html")
