from django.contrib import admin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models
from chat.models import ChatRoom, Messages


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_display = ['id', ]

    class Meta:
        model = ChatRoom


admin.site.register(ChatRoom, ChatRoomAdmin)


class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self, "_count"):
            self._count = None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(
                    hash(self.object_list.query.__str__()))
                self._count = cache.get(key, -1)
                if self._count == -1:
                    self._count = super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)

        return self._count

    count = property(_get_count)


class MessageAdmin(admin.ModelAdmin):
    list_filter = ['room', 'user', 'created_date']
    list_display = ['room', 'user', 'created_date', 'content']
    search_fields = ['room__name', 'user__username', 'content']
    readonly_fields = ['id', 'user', 'room', 'created_date']

    show_full_result_count = False
    paginator = CachingPaginator

    class Meta:
        model = Messages


admin.site.register(Messages, MessageAdmin)
