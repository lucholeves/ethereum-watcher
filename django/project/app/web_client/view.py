from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("web_client/index.html")
    context = {}
    return HttpResponse(template.render(context, request))


def block_details(request, block_number):
    template = loader.get_template("web_client/block_transactions.html")
    context = {"block_number": block_number}
    return HttpResponse(template.render(context, request))


def address_history(request, address):
    template = loader.get_template("web_client/address_history.html")
    context = {"address": address}
    return HttpResponse(template.render(context, request))
