from django.contrib import admin
from reps.models import State, LGA, Constituency,\
    District, Representative, Senator


class LGAAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'constituency', 'district')
    list_filter = ('state',)
    search_fields = ['name']


class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ['name']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ['name']


class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('name', 'constituency')
    list_filter = ('constituency__state',)
    search_fields = ['name']


class SenatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    list_filter = ('district__state',)
    search_fields = ['name']


admin.site.register(State)
admin.site.register(LGA, LGAAdmin)
admin.site.register(Constituency, ConstituencyAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(Senator, SenatorAdmin)
