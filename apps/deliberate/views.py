from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from utils.mixin import LoginRequiredMixin

# Create your views here.
class dlbr_detailView(LoginRequiredMixin,View):
    def get(self, request):
        return render(request, 'Season_01/05_deliberate.html')
