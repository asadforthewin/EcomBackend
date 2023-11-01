from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection


class COllectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.ModelSerializer):
    class Meta: #Inner class for Copying the data of Models
        model = Product #the model which we are refering
        fields = ['id', 'title', 'unit_price', 'price_with_tax' ,'collection'] #The fields from models
        '''Note that the fields like price_with tax are not in the Model class so we have 
        defined them here also by default the modelserializer takes the related field PK but 
        here we have given it hyperlink by defining hyperlink below'''

    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length = 255)
    # unit_price = serializers.DecimalField( max_digits=6 , decimal_places=2) 
    # '''in case the unit price and the price defined in product model, these vars are not the same
    # than we need to give another argument in the unit_price field that is 'source = unit_price' that
    # refer to the var in product model'''
    price_with_tax = serializers.SerializerMethodField(method_name='taxes') #custom Serializer
    # # collection = serializers.PrimaryKeyRelatedField( for primary key related representation
    #     # queryset = Collection.objects.all() )
    # # collection = COllectionSerializer() Nested Object in the productSerializer
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name='collection-detail')
    # ) #This one takes 2 arguments, for linking the object in views

    def taxes(self,Product): 
        return Product.unit_price * Decimal(1.1) #converting the float to decimal