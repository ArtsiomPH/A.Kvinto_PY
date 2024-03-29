from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Medcine)
class MedcineAdmin(admin.ModelAdmin):
    list_display = ["international_name", "general_info", "general_url_name", "general_documentation", "formula",
                    "pub_date",
                    "pub_update"]
    list_display_links = ["international_name"]
    search_fields = ["international_name", "pub_date"]
    list_filter = ["pub_date"]
    prepopulated_fields = {'general_url_name': ('international_name',)}


@admin.register(Synonyms)
class SynonymsAdmin(admin.ModelAdmin):
    list_display = ["comm_name", "url_name", "medcine", "pub_date", "pub_update"]
    list_display_links = ["comm_name"]
    search_fields = ["comm_name", "medcine__international_name"]
    list_filter = ["pub_date"]
    prepopulated_fields = {'url_name': ('comm_name',)}


@admin.register(GeneralSources)
class GeneralSourcesAdmin(admin.ModelAdmin):
    list_display = ["source_name", "medcine"]
    list_display_links = ["source_name"]
    search_fields = ["source_name", "medcine__international_name"]


@admin.register(RequestCounter)
class RequestCounterAdmin(admin.ModelAdmin):
    list_display = ["synonym", "count", "date"]
    list_display_links = ["synonym"]
    search_fields = ["synonym", "date"]
