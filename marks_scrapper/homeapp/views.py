from django.shortcuts import render
from .functions.result import process_link

# Create your views here.


def hello_world(request):
    if request.method == "POST":
        link = str(request.POST["link"])
        details = process_link(link)
        return render(
            request,
            "homeapp/result.html",
            details,
        )
    return render(request, "homeapp/hello.html")
