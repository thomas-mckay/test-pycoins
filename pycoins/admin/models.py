from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from pycoins.models import Alert, Symbol


class AlertAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'coin_admin', 'currency_admin', 'user_admin',
                    'trigger_type', 'amount', 'evolution', 'evolution_period', 'activated')
    list_filter = ('coin', 'currency', 'trigger_type', 'activated')
    raw_id_fields = ('user',)

    def get_queryset(self, request):
        return (super(AlertAdmin, self)
                .get_queryset(request)
                .select_related('coin', 'currency')
                .prefetch_related('user'))

    def coin_admin(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:pycoins_symbol_change', kwargs={'object_id': obj.coin_id}),
            obj.coin))

    def currency_admin(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:pycoins_symbol_change', kwargs={'object_id': obj.currency_id}),
            obj.currency))

    def user_admin(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse('admin:auth_user_change', kwargs={'object_id': obj.user_id}),
            obj.user.username))


class SymbolAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'type')
    list_filter = ('type',)


admin.site.register(Alert, AlertAdmin)
admin.site.register(Symbol, SymbolAdmin)
