import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.user_private.models import user_private
from apps.plan.models import plan, plan_section,plan_finish
import datetime


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday

def getPreDay(preNum):
    today = datetime.date.today()
    preday = datetime.timedelta(days=preNum)
    rst = today - preday
    return rst




class pickStarView(View):
    def get(self, request):
        # Review中，展示昨天所完成的内容

        # 获取用户对象
        user = request.user
        user_obj = user_private.objects.get(username = user.username)
        # 用户完成列表中，获取昨天情况
        plan_fin_pre1 = plan_finish.objects.filter(user_id=user_obj.id,date=getPreDay(2))
        print('得到的plan_fin记录日期：',plan_fin_pre1[0].date)

        # 昨天完成第一项任务的章节数
        chapter = plan_fin_pre1[0].finish_cpt
        section = plan_fin_pre1[0].finish_sct
        print("得到用户这一天完成的cpt & sct：",chapter,section)

        # 准备模板所需数据
        send_obj = []
        for var in plan_fin_pre1: # 遍历每一个【用户完成列表plan_finish】中，昨天的完成情况
            # 根据【用户完成列表】的记录，取出【任务详细列表 plan_section】的对应数据。
            record = plan_section.objects.get(user_id=var.user_id,pj_id=var.plan_id,
                                                   chapter=var.finish_cpt,section=var.finish_sct)
            send_obj.append(record)

        print("send_obj内容：",send_obj)
        context={
            "yesterday":send_obj,
        }

        return render(request, 'Season_01/06_pickStar.html',context)


class daySwitchView(View):
    def post(self,request):
        if self.request.is_ajax:
            # 获取传过来的日期
            user = request.user
            r_year = request.POST.get("r_year")
            r_month = request.POST.get("r_month")
            r_day = request.POST.get('r_day')
            r_date = r_year+'-'+r_month+'-'+r_day
            print('requestDate收到：',r_date)

            # 根据日期查找用户的【计划完成表】
            try: # 根据用户名找到用户id
                user_obj= user_private.objects.get(username=user.username)
                # 根据用户id，找到用户在这一天完成了多少项事情
                r_query = plan_finish.objects.filter(user_id=user_obj.id,date=r_date)
            except Exception as e:
                print('aaaa数据库没找到！！')
                r_query=None


            print('r_query最后:',r_query)
            json_obj = serializers.serialize('json', r_query)
            # print('r_query 强制转成list:',a)
            # for x in a:
            #     print('list里面取内容：',x.plan_id,x.finish_cpt)
        # result = {'status':'eeeeee','rst':a}
        return HttpResponse(json_obj)