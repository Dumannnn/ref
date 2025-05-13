from django.views.generic import ListView, DetailView
from .models import EatingItem, Category, Dish, DishType, \
    EatingItemDish, Dish, EatingItem, EatingItemDish
from django.db.models import Q


class MenuView(ListView):
    model = EatingItem
    template_name = 'main/product/list.html'
    context_object_name = 'eating_items'


    def get_queryset(self):
        queryset = super().get_queryset()
        category_slugs = self.request.GET.getlist('category')
        size_names = self.request.GET.getlist('dish')
        type_ids = self.request.GET.getlist('type') 
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        search_query = self.request.GET.get('q')

        if category_slugs: 
            queryset = queryset.filter(category__slug__in=category_slugs)

        if size_names:
            queryset = queryset.filter(
                Q(sizes__name__in=size_names) & Q(sizes__clothingitemsize__available=True)
            ).distinct()

        if type_ids:
            queryset = queryset.filter(
                dishes__types__id__in=type_ids
            ).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['dishes'] = Dish.objects.all()
        context['dish_types'] = DishType.objects.all()  
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_dishes'] = self.request.GET.getlist('dish')
        context['selected_dish_types'] = self.request.GET.getlist('type') 
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')

        return context
    
class EatingItemDetailView(DetailView):
    model = EatingItem
    template_name = 'main/product/detail.html'
    context_object_name = 'eating_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eating_item = self.object
        available_dishes = EatingItemDish.objects.filter(eating_item=eating_item,
                                                           available=True)
        context['available_dishes'] = available_dishes
        return context
