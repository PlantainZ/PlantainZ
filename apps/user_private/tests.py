from django.http import HttpResponse
from django.test import TestCase
from django.contrib.auth.hashers import check_password,make_password
# Create your tests here.

def dataTest(request):
    a = '123456'
    rst = check_password(a,make_password(a))
    print(rst)
    return HttpResponse(rst)