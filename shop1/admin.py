import admin_thumbnails
from django.contrib import admin
from .models import Category, Product, Images
from parler.admin import TranslatableAdmin


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated', 'image_tag']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    inlines = [ProductImageInline]
    readonly_fields = ('image_tag',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
