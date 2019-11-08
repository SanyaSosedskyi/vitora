from django.contrib import admin
from .models import Board, Topic, Post


def make_boards_disable(modeladmin, request, queryset):
    for board in queryset:
        board.is_active = False
        board.save()


make_boards_disable.short_description = 'Make boards disable'


class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    actions = [make_boards_disable, ]


admin.site.register(Board, BoardAdmin)
admin.site.register(Topic)
admin.site.register(Post)
