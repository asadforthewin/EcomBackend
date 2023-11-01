from django.shortcuts import get_object_or_404 , get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer



@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all() #geting the list of all products 
    # plus selecting related field collection
    serilizer = ProductSerializer(queryset, many=True, context= {'request': request}) 
    #Many to true because serializer can iterate over prod
    return Response(serilizer.data)

@api_view() 
def product_detail(request, id):     

    product= get_object_or_404(Product , pk=id) #getting the product with PK 
    serializer = ProductSerializer(product) #convert our product obj to dictionary 
    return Response(serializer.data) #getting that dictionary 
'''here we are not using JSONRenderer beacuse that process will occur under the hood,at some point django
would create a JSONRenderer object and give it this dictionary and JSON Renderer would convert that
dictionary to JSON object which will end up in a response, all of that is hidden from us '''

@api_view()
def Collection_Details(request,pk):
   return Response('ok')