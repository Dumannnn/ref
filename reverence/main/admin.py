from django.contrib import admin
from .models import Dish, Category, \
    EatingItem, EatingItemDish, ItemImage , DishType


class EatingItemDishInline(admin.TabularInline):
    model = EatingItemDish
    extra = 4


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 4

@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    filter_horizontal = ('types',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(EatingItem)
class EatingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',
                    'available', 'price', 'discount',
                    'created_at', 'updated_at')
    list_filter = ('available', 'category')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    inlines = [EatingItemDishInline, ItemImageInline]
