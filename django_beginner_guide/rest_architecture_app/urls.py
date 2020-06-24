from django.urls import include, path
from . import views

urlpatterns = [

  # ---------- Custom view logics for creating rest apis ------------
  
  # Seperate view method for each CRUD (Each logic same as below - "cus2/items" )
  # path('cus1/items/all', views.custom1_get_all_items),
  # path('cus1/items/create', views.custom1_create_new_item),
  # path('cus1/items/<int:item_id>/detail', views.custom1_get_item_detail),
  # path('cus1/items/<int:item_id>/update', views.custom1_update_item_detail),
  # path('cus1/items/<int:item_id>/delete', views.custom1_delete_item),

  # View method that controls the request type and perform their respective logic
  path('cus2/items/', views.custom2_items_view),
  path('cus2/items/<int:item_id>', views.custom2_item_detail_view),


  # ---------- Using View classes provided by rest framework ------------

  # APIView class that is the base of all views
  path('gn/items/', views.GenericView_ItemsView.as_view(), name='genric_items_view'),
  path('gn/items/<int:item_id>/', views.GenericView_ItemDetailView.as_view(), name='generic_item_detail_view'),

  # Concrete view classes composed by mixin classes with the base view
  path('items/', views.ItemsView.as_view(), name='mixin_items_view'),
  path('items/<int:item_id>/', views.ItemDetailView.as_view(), name='mixin_item_detail_view')

]