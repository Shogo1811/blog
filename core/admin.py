from django.contrib import admin

from core.models import (
    Tag,
    Entry
)


class TagAdmin(admin.ModelAdmin):
    pass


class EntryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Entry, EntryAdmin)