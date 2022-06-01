from django.contrib import admin

# Register your models here.
import administer.models


@admin.register(administer.models.Carousel_figure)
class userAdmin(admin.ModelAdmin):
    list_display = ('Figure_id', 'Figure_img')
