from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .serializers import GetProductsSerializer,GetOrderSerializer,GetUserCartSerializer,GetUserCartItemSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from menu.models import Product,Cart,Order,OrderItem,Cart_item
from SushiBar.pagination import HeaderLimitOffsetPagination
from SushiBar.pagepagination import HeaderPageNumberPagination


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    try:
        objects = Product.objects.all()
    except Product.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = GetProductsSerializer(objects, many = True)
    return Response (serializer.data)

# @api_view(['POST'])
# def create_product(request):
#         serializer = CreateProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)


@api_view(['DELETE','PUT'])
@permission_classes([IsAdminUser])
def product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetProductsSerializer(product)
        return Response(serializer.data)

    # elif request.method == 'PUT':
    #     serializer = CreateProductSerializer(new,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GetProductsSerializer(product)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail_id(request):
    if request.method == 'GET':
        id = request.GET.get('id','')
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GetProductsSerializer(product)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_orders(request):
    try:
        objects = Order.objects.order_by('status', 'created')
        paginator = HeaderPageNumberPagination()
        context = paginator.paginate_queryset(objects, request)
    except Order.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = GetOrderSerializer(context, many=True)
    return paginator.get_paginated_response(serializer.data)
    # return Response (serializer.data)


@api_view(['GET','DELETE','PUT'])
def get_order_detail(request, id):
    print("Views order id: ", id)
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = GetOrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GetOrderSerializer(order,data=request.data)
        print("Views order id PUT: ", id)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status =status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        order.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


@api_view(['GET','DELETE','PUT','POST'])
@permission_classes([IsAuthenticated])
def user_cart_view(request):
    if request.method == "GET":
        cart = Cart.objects.get(user=request.user)
        cart_products = Cart_item.objects.filter(cart=cart)
        # serializer = GetUserCartItemSerializer(cart_products, many=True)
        serializer = GetUserCartSerializer(cart)
        return Response(serializer.data)
    if request.method == "PUT":
        id = request.POST.get('id','')
        quantity = request.POST.get('quantity', 0)
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=id)
        order_item = Cart_item.objects.filter(cart = cart, product = product)
        item = None
        if order_item.exists():
            item = Cart_item.objects.get(cart = cart, product = product)
            item.quantity += int(quantity)
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        else:
            if int(quantity) > 0:
                item = Cart_item(product = product, cart = cart, quantity = quantity)
                item.save()
        serializer = GetUserCartSerializer(cart)
        return Response(serializer.data)
    if request.method == "DELETE":
        id = request.POST.get('id','')
        quantity = request.POST.get('quantity', 0)
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(id=id)
        order_item = Cart_item.objects.filter(cart = cart, product = product)
        if order_item.exists():
            item = Cart_item.objects.get(cart = cart, product = product)
            item.delete()
        serializer = GetUserCartSerializer(cart)
        return Response(serializer.data)


    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','DELETE','PUT','POST'])
@permission_classes([IsAuthenticated])
def user_cart_product_item_view(request):
    try:
        if request.method == "GET":
            id = request.GET.get('id','')
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(id=id)
            cart_product = Cart_item.objects.get(cart=cart, product=product)
            print(cart_product)
            # serializer = GetUserCartItemSerializer(cart_products, many=True)
            serializer = GetUserCartItemSerializer(cart_product)
            return Response(serializer.data)
    except Cart_item.DoesNotExist:
        pass

    return Response(status=status.HTTP_404_NOT_FOUND)