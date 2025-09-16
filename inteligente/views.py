from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "inteligente/index.html")

def farmer_template(request):
    return render(request, "inteligente/farmer_template")