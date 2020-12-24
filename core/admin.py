from django.contrib import admin
from django.contrib.admin.decorators import register
from core.models import Ad, AdImage, AdVideo, Category, City, SponsorContent
from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
admin.site.unregister(User)


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    exclude = ['slug']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_preview']
    readonly_fields = ['image_preview']

    exclude = ['slug']


class RegionInline(admin.TabularInline):
    model = Ad.regions.through
    extra = 0
    verbose_name = "Регион"
    verbose_name_plural = "Регионы (В каких регионах показывать?)"


class AdImageInline(admin.TabularInline):
    model = AdImage
    extra = 0
    readonly_fields = ('image_preview',)
    verbose_name = "Картинки"
    verbose_name_plural = "Картинки"


class AdVideoInline(admin.TabularInline):
    model = AdVideo
    extra = 0
    readonly_fields = ['thumbnailUrl', 'thumbnail_preview']
    verbose_name = "Видео"
    verbose_name_plural = "Видео (Вставить ссылку с YouTube!)"


class AdAdmin(admin.ModelAdmin):
    list_display = ['description', 'phone_number', 'is_whatsapp_number',
                    'category', 'timestamp', 'expire_date', 'days_left', ]
    list_filter = ['category', 'regions']
    inlines = [
        RegionInline,
        AdImageInline,
        AdVideoInline,
    ]
    exclude = ['regions']
    verbose_name = "Объявление"
    verbose_name_plural = "Объявления"


class SponsorAdmin(admin.ModelAdmin):
    list_display = ['sponsor_name', 'phone_number',
                    'description', 'category', 'expire_date', 'days_left', ]
    list_filter = ['category', 'regions']
    inlines = [
        RegionInline,
        AdImageInline,
    ]
    exclude = ['regions']


class AdImageAdmin(admin.ModelAdmin):
    list_per_page = 500


admin.site.register(City, CityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(SponsorContent, SponsorAdmin)
# admin.site.register(AdImage, AdImageAdmin)
