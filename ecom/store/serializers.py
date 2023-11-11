from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection,Review, Cart, CartItem, Customer
from django.db.models import Count


class COllectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
        # the products_count is read-only so we dont have to update it each time we are creating a collection
    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta: #Inner class for Copying the data of Models
        model = Product #the model which we are refering
        fields = ['id', 'title','slug', 'unit_price','inventory', 'price_with_tax' ,'collection'] #The fields from models
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
    collection = serializers.PrimaryKeyRelatedField( #for primary key related representation
        queryset = Collection.objects.all() )
    # # collection = COllectionSerializer() Nested Object in the productSerializer
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail')
    # ) #This one takes 2 arguments, for linking the object in views

    def taxes(self,Product): 
        return Product.unit_price * Decimal(1.1) #converting the float to decimal
    


class ReviewSerializer(serializers.ModelSerializer):
    class Meta: #inner class that is taking data from Models
        model = Review
        fields= ['id','date','name','description' ]

    '''Serializer have a save method that will create an object or update it, so with create method the serializer
will create all the fields that we defined above, we dont have a product_id here so we are getting an error 'Product_id 
cant be null', to solve this problem we need to give the product_id to context object 
    '''

    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id= product_id, **validated_data)
    


class SimpleProductSerializer(serializers.ModelSerializer): #serializer that will have only title and unit price
    class Meta:
        model = Product
        fields = ['title', 'unit_price']
    

    
class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price 

    class Meta:
        model = CartItem
        fields = ['id', 'product','quantity', 'total_price']


    
class CartSerialzer(serializers.ModelSerializer):

    id =serializers.UUIDField(read_only= True) #read only return it from the server 
    cartitems = CartItemSerializer(many=True, read_only=True)
    cart_price = serializers.SerializerMethodField()

    def get_cart_price(Self, cart):
        return sum([i.quantity * i.product.unit_price for i in cart.cartitems.all() ])
    class Meta:
        model = Cart
        fields = ['id', 'cartitems', 'cart_price']



class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()
    class Meta: 
        model = CartItem
        fields = ['id', 'product_id' , 'quantity']

    def validate_product_id(self,value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('This product doesnt exist')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity= self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(product_id= product_id, cart_id=cart_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    

class UpdateCartItemSerializer(serializers.Serializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(read_only = True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id' , 'birth_date', 'phone', 'membership']


    
