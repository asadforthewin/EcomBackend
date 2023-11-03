from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serializers import ProductSerializer, COllectionSerializer, ReviewSerializer


# 1 Product List
# since this method is replaced by class based View
'''@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all() #geting the list of all products 
    # plus selecting related field collection
        serilizer = ProductSerializer(queryset, many=True, context= {'request': request}) 
    #Many to true because serializer can iterate over multiple products
        return Response(serilizer.data)
    elif request.method == 'POST':
        serilizer = ProductSerializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        serilizer.save()
        return Response(serilizer.data , status=status.HTTP_201_CREATED)'''


# 2
# since this method is now replaced by GENERIC VIEWS
'''
class ProductList(APIView):

    def get(self, request):
        #geting the list of all products + selecting related field collection
        queryset = Product.objects.select_related('collection').all() 
        #Many=True because serializer can iterate over multiple products
        # for providing the hyperlink of anything in product list we use context={}
        serilizer = ProductSerializer(queryset, many=True, context= {'request': request}) 
        return Response(serilizer.data)
    
    def post(Self, request):
        # deserializing the data we getting from user
        serilizer = ProductSerializer(data=request.data)
        # checking if serializer is valid 
        serilizer.is_valid(raise_exception=True)
        # saving the serializer
        serilizer.save()
        return Response(serilizer.data , status=status.HTTP_201_CREATED)
        

'''

# 3
'''
class ProductList(ListCreateAPIView):

    def get_queryset(self):
        return Product.objects.all() 
    
    def get_serializer_class(self):
        return ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
'''


# 1 Product Detail
# since this is replced by APIVIEW

'''@api_view(['GET' , 'PUT','DELETE']) 
def product_detail(request, id):     
    product= get_object_or_404(Product, pk=id) #getting the product with PK
    if request.method == 'GET': 
        serializer = ProductSerializer(product) #convert our product obj to dictionary 
        return Response(serializer.data) #getting that dictionary 
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if product.orderitems.count() >0:
            return Response({'Error':'You cant delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)'''
'''here we are not using JSONRenderer beacuse that process will occur under the hood,at some point django
would create a JSONRenderer object and give it this dictionary and JSON Renderer would convert that
dictionary to JSON object which will end up in a response, all of that is hidden from us '''


# 2 APIVIEW
'''

class ProductDetail(APIView):
    
    def get(Self,request,id):
        #getting the product with PK 
        product= get_object_or_404(Product, pk=id) 
        #convert our product obj to dictionary 
        serializer = ProductSerializer(product) 
        #getting that dictionary
        return Response(serializer.data)
    
    def put(Self,request,id):
        # Getting the obj with PK
        product= get_object_or_404(Product, pk=id)
        # deserializing the given data for updating the obj
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def delete(Self,request,id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() >0: 
            return Response({'Error':'You cant delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''
    

# 3
# Custom Generic View
'''
    
class ProductDetail(RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        return Product.objects.all( )
    def get_serializer_class(self):
        return ProductSerializer
    

    def delete(self,pk):  
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() >0: 
            return Response({'Error':'You cant delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    '''

# 4
# FOR BOTH ProductDetail and ProductList

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all( )
    serializer_class = ProductSerializer
    def get_serializer_context(self):
        return {'request': self.request}
    

    def destroy(self, request, *args, **kwargs): #method from the base class ModelViewSet 
        # filtering the order items via their PK whose Count is greater than 0
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() >0: 
            return Response({'Error':'You cant delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # if not we are good to delete the product
        return super().destroy(request, *args, **kwargs)
    

# with destroy method implementation we dont need the delete method which was from base class RetriveUpdateDestroyAPIview 
'''
    def delete(self,pk):  
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() >0: 
            return Response({'Error':'You cant delete this product'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
'''


    
    
# 1 Collection detail
'''
@api_view(['GET', 'PUT', 'DELETE'])
def Collection_Details(request,pk):
   collection = get_object_or_404(
       Collection.objects.annotate(products_count = Count('collectionset')),
        pk=pk)
   if request.method == 'GET':
       serializer = COllectionSerializer(collection) 
       return Response(serializer.data)
   elif request.method == 'PUT':
       serializer = COllectionSerializer(collection, data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
   elif request.method == 'DELETE':
       if Collection.collectionset.count()>0:
           return Response({'Error':'You cant delete this collection'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
       else:
           Collection.delete()
           return Response(status=status.HTTP_204_NO_CONTENT)
'''
# 2
# USiNG API VIEWS
'''
class CollectionDetail(APIView):

    def get(self,request,pk):
       collection = get_object_or_404(Collection.objects.annotate(products_count = Count('collectionset')),pk=pk)
       serializer = COllectionSerializer(collection) 
       return Response(serializer.data)
    def put(self,request):
       collection = get_object_or_404(Collection.objects.annotate(products_count = Count('collectionset')),pk=pk)
       serializer = COllectionSerializer(collection, data=request.data)
       serializer.is_valid(raise_exception=True)
       serializer.save()
       return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self,request):
        if Collection.collectionset.count()>0:
            return Response({'Error':'You cant delete this collection'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            Collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

'''




# 3
# USING GENERIC VIEWS WITH CUSTOM GENERIC
'''
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Collection.objects.annotate(products_count = Count('collectionset'))
    def get_serializer_class(self):
        return COllectionSerializer
    
    def delete(self,request,pk):
        collection = get_object_or_404(Collection,pk=pk)
        if Collection.collectionset.count()>0:
            return Response({'Error':'You cant delete this collection'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            Collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
'''
    

   
# 1 Collection List
'''
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count= Count('collectionset')). all()
        serializer =COllectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = COllectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
       
    '''



#  2 
#  Now converted to above Generic view 
'''
class CollectionList(APIVIEW)
    def get(self,request):
        queryset = Collection.objects.annotate(products_count= Count('collectionset')). all()
        serializer =COllectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = COllectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)'''


# 3
'''
class CollectionList(ListCreateAPIView):


    def get_queryset(self):
        return Collection.objects.annotate(products_count= Count('collectionset')). all()
    
    def get_serializer_class(self):
        return COllectionSerializer

'''
# 4
# Both for Collection List and Collection detail

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count= Count('collectionset')). all()
    
    serializer_class = COllectionSerializer



    def destroy(self, request, *args, **kwargs):
        if Product.count()>0:
            return Response({'Error':'You cant delete this collection'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    '''
    def delete(self,request,pk):
        collection = get_object_or_404(Collection,pk=pk)
        if Collection.collectionset.count()>0:
            return Response({'Error':'You cant delete this collection'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            Collection.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    '''


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all() #all the objects/products 
    serializer_class = ReviewSerializer