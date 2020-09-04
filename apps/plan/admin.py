from django.contrib import admin
from apps.plan.models import plan,plan_section,plan_comment

@admin.register(plan,plan_section,plan_comment)
class planAdmin(admin.ModelAdmin):
    pass



# 犯过的错：切记admin.py是在app目录下才有
# 不是工程同名的目录！