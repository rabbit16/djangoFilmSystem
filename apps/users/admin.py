from django.contrib import admin

# Register your models here.
import users.models


@admin.register(users.models.User)
class userAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'buyManager', 'ticketManager', 'is_superuser', 'is_staff')


@admin.register(users.models.Movie)
class movieAdmin(admin.ModelAdmin):
    list_display = ('Movie_id', 'Movie_name', 'Movie_time', 'Movie_price', "Movie_lasts")

@admin.register(users.models.Studio)
class studioAdmin(admin.ModelAdmin):
    list_display = ('Studio_id', 'Studio_name', 'Studio_type', 'Seating')

@admin.register(users.models.Times)
class sessionAdmin(admin.ModelAdmin):
    list_display = ('Times_id', 'session_time', 'T_movie_id', 'T_studio_id')

@admin.register(users.models.Movie_type)
class movieTypeAdmin(admin.ModelAdmin):
    list_display = ('type_id', 'type_name')

@admin.register(users.models.Seat)
class seatAdmin(admin.ModelAdmin):
    list_display = ('Seat_id', 'Seat_name')

@admin.register(users.models.Ticket)
class ticketAdmin(admin.ModelAdmin):
    list_display = ('Ticket_id', 'Ticket_seat', "Ticket_session", "Ticket_studio", "Ticket_user")

@admin.register(users.models.Comment)
class commentAdmin(admin.ModelAdmin):
    list_display = ('Comment_id', 'Comment_content', "Comment_time", "Comment_likes", "Comment_author", "Comment_movie")



