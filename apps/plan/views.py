import json
import time

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection

# Create your views here.
from django.views import View

from apps.user_private.models import user_private
from apps.plan.models import plan, plan_section,plan_comment
from django.forms.models import model_to_dict
import datetime

def getPreday(days):
    sec = 60 * 60 * 24 * days
    print('前%d天的秒数：%d' %(days,sec))
    rst = time.strftime('%Y-%m-%d', time.localtime(time.time() - sec))
    return rst # 返回的是字符串格式

def dayDistance(now,to):
    date1 = time.strptime(now, "%Y-%m-%d")
    date2 = time.strptime(to, "%Y-%m-%d")

    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    return date2 - date1



class pickStarView(View):
    def get(self, request):
        # 获得昨天的日期
        # now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        yesterday = getPreday(2)
        yesterday_cover = getPreday(1)
        # 存在细节问题！
        # __lte选的是在yesterday之前的记录，yesterday默认是从0点开始，那么yesterday当天0点后的，都不算之前。
        # 所以要用yesterday_cover，把在yesterday 24:00以前的算进来。
        print('获得昨天的日期是：',yesterday)

        # 获取用户对象
        user = request.user
        user_obj = user_private.objects.get(username = user.username)
        print('获取到user_obj的id:',user_obj.id)

        # 根据用户id和昨天的日期，查找对应的记录
        plan_fin_pre1 = plan_section.objects.filter(user_id = user_obj.id,
                                                    finish_start__lte=yesterday_cover,
                                                    finish_end__gte=yesterday)

        # 查看检索到哪些章节
        for x in plan_fin_pre1:
            chapter = x.chapter
            section = x.section
            print("得到用户这一天完成的cpt & sct：",chapter,section)
            #################################################
            # 存在问题：要对这些章节进行排序！！！还没做。
            #################################################

        # 准备模板所需数据
        send_obj = []
        for var in plan_fin_pre1:
            send_obj.append(var)
        context={ "yesterday":send_obj, }

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
                print('为了查询评论，先查询user_obj:',user_obj.id)
                # 根据用户id，找到用户在这一天有多少条评论
                r_query = plan_comment.objects.filter(user_id=user_obj.id,
                                                      datetime__year=r_year,
                                                      datetime__month=r_month,
                                                      datetime__day=r_day)
                print('r_query有检测到！：',r_query)
                r_query = serializers.serialize('json',r_query)

            except Exception as e:
                print('aaaa数据库没找到！！')
                r_query = None

            print('r_query最后:',r_query)

            # return JsonResponse(query_dict)
            return HttpResponse(r_query, content_type='application/json')

class planAddView(View):
    def get(self,request):
        return render(request,'Season_01/07_planAdd.html')