from django.contrib import admin

# Register your models here.
import online_help.models


@admin.register(online_help.models.Problems)
class userAdmin(admin.ModelAdmin):
    list_display = ('Problems_id', 'Problems_contain')

@admin.register(online_help.models.Problems_type)
class userAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'type_name')