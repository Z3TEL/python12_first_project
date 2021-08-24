from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, mixins
from product.models import *
from product.permissions import IsAuthorOrIsAdmin
from product.serializers import ProductsSerializer, ProductDetailsSerializer, CreateProductSerializer, ReviewSerializer
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

# Create your views here.
def test_view(request):
    return HttpResponse('Hello , it\'s me!')

@api_view(['GET'])
def products_list(request):
    products = Product.objects.all()
#     [product1, product2, product3]
    serializer = ProductsSerializer(products, many=True)
#     [{'id': 1}, 'title': 'Some', 'descripption': '...' , 'price': .. ]
    return Response(serializer.data)

class ProductsListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)


# class ProductsListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductsSerializer
#
#
# class ProductDetailsView(RetrieveAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductDetailsSerializer
#
#
# class CreateProductView(CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class UpdateProductView(UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#
# class DestroyProductView(DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = CreateProductSerializer
#
#


class ProductFilter(filters.FilterSet):
    price_from = filters.NumberFilter('price', 'gte')
    price_to = filters.NumberFilter('price', 'lte')
    class Meta:
        model = Product
        fields = ('price_from', 'price_to')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter, rest_filters.OrderingFilter]
    # filterset_fields = ('price')
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price']


    # api/v1/products/
    # api/v1/products/?price_from=10000&price_to=15000


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     price_from = self.request.query_params.get('price_from')
    #     price_to = self.request.query_params.get('price_to')
    #     queryset = queryset.filter(price__gte=price_from, price__lte=price_to)
    #     return queryset



    def get_serializer_class(self):
        if self.action == 'list':
            return ProductsSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        return CreateProductSerializer


    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


# CRUD(Create, Retrieve, Update, Delete)
#         POST    GET     PUT/PATCH  DELETE


# создает отзыв только залогиненый пользаватель
# редактировать может только админ или автор
class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ReviewSerializer


    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []

    # api/v1/products/id
    # api/v1/products/id/reviews/
    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        # reviews = ProductReview.objects.filter(product=product)
        reviews = product.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=200)



# TODO: Ограничение кол-во запросов
# TODO: Документация
# TODO: README


# REST - архитектурный подход
# 1. модель клиент -сервер
# 2. Отсутствие состояние
# 3. Кеширование
# 4. Единообразин интерфейса
#     1. Определение ресурсов
#       URI('api/v1/products/1') - это путь
#     2. Управление ресурсами через представление
#     3. Самодостаточнные сообщение
#     4. Гипермедиа


# 5. Слои
# 6. код по требованию

# 'GET', 'POST', 'PUT', 'PATCH',        'DELETE'
#  list   crete  update  partial_update   destroy
#  retrieve



# API(Application Programming Interface)
# Паттерн MVC


# Product.objects.all() - выдает весь список объектов класса
# SELECT * FROM product

# Product.objects.create() - создает новый объект
# INSERT INTO product ...

# Product.objects.update() - обновляет объекты
# UPDATE product ...

# Product.objects.delete() - удаляет объкты
# DELETE FROM products;

# Product.objects.filter(условие)
# SELECT * FROM product WHERE условие;

# Операции сравниенние
# "="
# Product.objects.filter(price=10000)
# SELECT * FROM product WHERE price = 100000;

# ">"
# Product.objects.filter(price__gt=10000)
# SELECT * FROM product WHERE price > 10000;

# "<"
# Product.objects.filter(price__lt=10000)
# SELECT * FROM product WHERE price < 10000;

# ">="
# Product.objects.filter(price__gte=10000)
# SELECT * FROM product WHERE price >= 10000;

# "<="
# Product.objects.filter(price__lte=10000)
# SELECT * FROM product WHERE price <= 10000;

# BETWEEN
# Product.objects.filter(price__range=[50000, 80000])
# SELECT * FROM product WHERE  price BETWEEN 50000 AND 80000;

# IN
# Product.objects.filter(price__in=[50000,80000])
# SELECT * FROM product WHERE  price IN 50000 AND 80000;

# LIKE
# ILIKE

# 'work%'
# Product.objects.filter(title__startswitch='Apple')
# SELECT * FROM product WHERE title LIKE 'Apple%'
# Product.objects.filter(title__istartswitch='Apple')
# SELECT * FROM product WHERE title ILIKE 'Apple%'

# '%work'
# Product.objects.filter(title__endswitch='GB')
# SELECT * FROM product WHERE title LIKE '%GB';

# Product.objects.filter(title__iendswitch='GB')
# SELECT * FROM product WHERE title ILIKE '%GB';

# '%work%'
# Product.objects.filter(title__contains='Samsung')
# SELECT * FROM product WHERE title LIKE '%Samsung%';

# Product.objects.filter(title__icontains='Samsung')
# SELECT * FROM product WHERE title ILIKE '%Samsung%';

# 'work'
# Product.objects.filter(title__exact='Apple Iphone 12')
# SELECT * FROM product  WHERE title LIKE 'Apple Iphone 12';

# Product.objects.filter(title__iexact='Apple Iphone 12')
# SELECT * FROM product  WHERE title ILIKE 'Apple Iphone 12';

# Сортировка
# ORDER BY
# Product.objects.order_by('price')
# SELECT * FROM product ORDER BY price ASC;

# # Product.objects.order_by('-price')
# SELECT * FROM product ORDER BY price DESC;

# Product.objects.order_by('-price', 'title')
# SELECT * FROM product ORDER BY price DESC , title ASC;

# LIMIT
# Product.objects.all()[:2]
# SELECT * FROM product LIMIT 2;

# Product.objects.all()[3:6]
# SELECT * FROM product LIMIT 3 OFFSET 3;

# Product.objects.first()
# SELECT * FROM product LIMIT 1;


# get() - возвращает один объект

# Product.objects.get(id=1)
# SELECT * FROM product WHERE id=1;

# DoesNotExist - возникает , если не найден ни один объект
# MultipleObjectsReturned - возникает , когда найдено больше одного

# count() - возвращает кол-во результатов

# Product.objects.count()
# SELECT COUNT(*) FROM product;

# Product.objects.filter(...).count()
# SELECT COUNT(*) FROM product WHERE ...;

# exclude()
# Product.objects.filter(price__gt=10000)
# SELECT COUNT(*) FROM product WHERE price > 10000;

# Product.objects.exlude(price__gt=10000)
# SELECT COUNT(*) FROM product WHERE NOT price > 10000;

# QuerySet - список объектов модели