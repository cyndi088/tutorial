from django.contrib import admin
from .models import Snippet
# Register your models here.


admin.site.site_title = '后台管理系统'  # 页面标题

admin.site.site_header = '后台管理'  # 登录页导航条和首页导航条标题

admin.site.index_title = '欢迎登录'  # 主页标题

admin.site.register(Snippet)
