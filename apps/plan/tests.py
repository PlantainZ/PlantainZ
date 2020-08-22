import datetime

from django.test import TestCase

# Create your tests here.
# def dataTest():
import time


def dayDistance(now, to):
    date1 = time.strptime(now, "%Y-%m-%d")
    # date2 = time.strptime(to, "%Y-%m-%d")
    #
    # date1 = datetime.datetime(date1[0], date1[1], date1[2])
    # date2 = datetime.datetime(date2[0], date2[1], date2[2])
    # 返回两个变量相差的值，就是相差天数
    # return date1 - date2


print (time.time())
# 格式化时间戳为标准格式
print (time.strftime('%Y.%m.%d',time.localtime(time.time())))

# 获取30天前的时间（通过加减秒数来获取现在或者未来某个时间点）
preDay = 30
sec = 60*60*24*preDay
print('1个月的秒数：',sec)
print (time.strftime('%Y.%m.%d',time.localtime(time.time()-sec)))

a = dayDistance('2020-05-23','2020-05-18')
print(a)