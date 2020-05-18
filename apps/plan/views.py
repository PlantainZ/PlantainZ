from django.shortcuts import render

# Create your views here.
from django.views import View

class pickStarView(View):
    def get(self,request):
        return render(request, 'Season_01/06_pickStar.html')