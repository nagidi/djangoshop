from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from .forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    products1 = Product.objects.filter(translations__slug='point')
    #products1 = Product.objects.get('translations__slug')
    print(products1)
    if category_slug:
        language = request.LANGUAGE_CODE
        category = get_object_or_404(Category,
                                     translations__language_code=language,
                                     translations__slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, id, slug):
    language = request.LANGUAGE_CODE
    product = get_object_or_404(Product,
                                id=id,
                                translations__language_code=language,
                                translations__slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})


def product_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.annotate(
                similarity=TrigramSimilarity('translations__name', query),
            ).filter(similarity__gt=0.3)| Product.objects.annotate(
                similarity=TrigramSimilarity('translations__description', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
            #print(similarity1.filter(similarity__gt=0.3))
           # print(similarity1[1])
            # print(similarity1[2])
    return render(request,
                  'shop/product/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
