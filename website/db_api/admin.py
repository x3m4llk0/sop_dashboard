from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Bonus)
admin.site.register(Mistake)
admin.site.register(Like)
admin.site.register(Quarter)