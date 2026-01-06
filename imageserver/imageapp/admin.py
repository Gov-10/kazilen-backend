from django.contrib import admin
from .models import Profile, ProfileImage

class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'uniqueID')
    inlines = [ProfileImageInline]

@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'isPrimary', 'uploadedAt')
