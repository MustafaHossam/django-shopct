from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product
from .products import products
from .serializers import ProductSerializer

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes= [
        '/api/products/',
        '/api/products/create/',

        '/api/products/upload/',

        '/api/products/<id>/reviews/',

        '/api/products/top/',
        '/api/products/<id>/',

        '/api/products/delete/<id>/',
        '/api/products/<update>/<id>/',
    ]
    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    query = request.GET.get('keyword')
    print("_____________query_________", query)
    if query == None:
        query = ''
    #products = Product.objects.filter(name__icontains=query)
    products = Product.objects.all()
    page = request.GET.get('page')
    print("_______________ page ____________", page )
    paginator = Paginator(products, 2 )

    try: 
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1 
    page = int(page)

    serializer = ProductSerializer(products, many=True)
    #return Response(serializer.data)
    return Response({'products':serializer.data, 'page':page, 'pages':paginator.num_pages})


@api_view(['GET'])
def getProduct(request, pk):
    product = Product.objects.get(_id=pk)

    
    serializer = ProductSerializer(product, many=False)
    #for i in products:
    #    if i['_id'] == pk:
    #        product = i
    #        break
    return Response(serializer.data)