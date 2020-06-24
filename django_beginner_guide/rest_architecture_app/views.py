from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ItemSerializer
from .models import Item

# Rest endpoints CRUD can be created in several ways
# Here 3 Options are mentioned

'''
Option-1) Seperate methods for each (GET, POST, PATCH and DELETE) 
    - Adjust urls.py accordingly
        - path('items/all', views.custom1_get_all_items),
        - path('items/create', views.custom1_create_new_item),
        - path('items/<int:item_id>/detail', views.custom1_get_item_detail),
        - path('items/<int:item_id>/update', views.custom1_update_item_detail),
        - path('items/<int:item_id>/delete', views.custom1_delete_item),
'''
@api_view(["GET"])
def custom1_get_all_items(request):
    # Refer to "custom2_items_view"
    pass

@api_view(["POST"])
def custom1_create_new_item(request):
    # Refer to "custom2_items_view"
    pass

@api_view(["GET"])
def custom1_get_item_detail(request, item_id):
    # Refer to "custom2_item_detail_view"
    pass

@api_view(["PATCH"])
def custom1_update_item_detail(request, item_id):
    # Refer to "custom2_item_detail_view"
    pass

@api_view(["DELETE"])
def custom1_delete_item(request, item_id):
    # Refer to "custom2_item_detail_view"
    pass

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

'''
Option-2) On the basis of REST Pattern, control from request Type
    - /items  -> wrap GET (all items), POST (create item)
    - /items/{id} -> GET by id, PATCH by id, DELETE by id  
'''
# /items 
@api_view(['GET', 'POST'])
def custom2_items_view(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# items/{id}
@api_view(['GET', 'PATCH', 'DELETE'])
def custom2_item_detail_view(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'GET':
        serializer = ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ItemSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        item.delete()
        return Response("Item deleted", status=status.HTTP_204_NO_CONTENT)


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

'''
Option-3) Using classes provided by rest_framework ( Follows REST Pattern)
    Advantage: No need to define mappings logics on methods
'''

'''
Way1:
- APIView -> 
        ItemsView - def get, def post
        path('items/', apiviews.ItemsView.as_view(), name='items_view')

        ItemsDetailView - def get, def patch, def delete (provide this methods)
        path('items/<int:item_id>/', apiviews.ItemDetailView.as_view(), name='item_detail_view')
'''
# /items
class GenericView_ItemsView(APIView):

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /items/{id}
class GenericView_ItemDetailView(APIView):

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ItemSerializer(item).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['question_id'])
        item.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

'''
Way2:
Provides default implementation 
- ListCreateAPIView -> default get(), default post()
        path('items/', apiviews.ItemsView.as_view(), name='items_view')
    
- RetrieveUpdateDestroyAPIView -> Default get(), patch() and delete()
        Mandatory attributes -> serializer_class , queryset , 
        Optional attributes -> lookup_url_kwarg (optional)
            path('items/<int:id>/', apiviews.ItemDetailView.as_view(), name='item_detail_view')
            [Note: "lookup_url_kwarg" is only needed for custom path variable 'items/<int:item_id>/' ]
'''
# /items
class ItemsView(ListCreateAPIView):

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# /items/{id}
class ItemDetailView(RetrieveUpdateDestroyAPIView):

    queryset = Item.objects.all()
    lookup_url_kwarg = 'item_id'
    serializer_class = ItemSerializer