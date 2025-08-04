from django.contrib import admin

# Register your models here.
from .models import ThemeSetting

@admin.register
class ThemeSettingsAdmin(admin.ModelAdmin):
    list_display = ('current_theme',)