from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(listings)
admin.site.register(bid)
admin.site.register(category)
admin.site.register(comment)


