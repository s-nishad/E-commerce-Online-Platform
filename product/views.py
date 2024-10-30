from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer, CreateStockSerializer


@swagger_auto_schema(method='post', request_body=ProductSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_product_view(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={200: ProductSerializer(many=True)})
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_product_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get', responses={200: ProductSerializer()})
@api_view(['GET'])
@permission_classes([AllowAny])
def product_by_guid(request, guid):
    try:
        product = Product.objects.get(guid=guid)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='put', request_body=ProductSerializer)
@api_view(['PUT'])
@permission_classes([AllowAny])
def update_product_view(request, guid):
    try:
        product = Product.objects.get(guid=guid)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # Supports partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='post', request_body=CreateStockSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_stock_view(request, guid):
    try:
        product = Product.objects.get(guid=guid)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    # Pass the product_guid in the context to the serializer
    serializer = CreateStockSerializer(data=request.data, context={'product_guid': product.guid})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='delete', responses={204: 'Delete Successfully'})
@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_product_view(request, guid):
    try:
        product = Product.objects.get(guid=guid)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
