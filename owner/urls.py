from django.urls import path
from .views import (
    OwnerDashboardView,
    OwnerProductListView,
    OwnerProductCreateView,
    OwnerProductUpdateView,
    OwnerProductDeleteView,
    OwnerMessageCenterView, ExportOrdersCSVView, StatisticsView, OwnerReplyMessageView,
)
from .views import PromotionToggleView, HomepageEditView
from .views import OwnerUserListView, OwnerBlockUserView, OwnerDeleteUserView
from .views import (
    OwnerOrderListView, OwnerUpdateOrderStatusView,
    TransportSettingsView,
)





urlpatterns = [
    path('', OwnerDashboardView.as_view(), name='owner-dashboard'),
    path('products/', OwnerProductListView.as_view(), name='owner-product-list'),
    path('products/add/', OwnerProductCreateView.as_view(), name='owner-product-add'),
    path('products/<int:pk>/edit/', OwnerProductUpdateView.as_view(), name='owner-product-edit'),
    path('products/<int:pk>/delete/', OwnerProductDeleteView.as_view(), name='owner-product-delete'),
    path('messages/', OwnerMessageCenterView.as_view(), name='owner-messages'),
    path('messages/<int:message_id>/reply/', OwnerReplyMessageView.as_view(), name='owner-reply-message'),
    path('products/<int:pk>/toggle-promotion/', PromotionToggleView.as_view(), name='owner-toggle-promotion'),
    path('homepage/edit/', HomepageEditView.as_view(), name='owner-homepage-edit'),
    path('users/', OwnerUserListView.as_view(), name='owner-user-list'),
    path('users/<int:user_id>/block/', OwnerBlockUserView.as_view(), name='owner-block-user'),
    path('users/<int:user_id>/delete/', OwnerDeleteUserView.as_view(), name='owner-delete-user'),
    path('orders/', OwnerOrderListView.as_view(), name='owner-order-list'),
    path('orders/<int:order_id>/update-status/', OwnerUpdateOrderStatusView.as_view(),
         name='owner-update-order-status'),
    path('transport-settings/', TransportSettingsView.as_view(), name='owner-transport-settings'),
    path('orders/export-csv/', ExportOrdersCSVView.as_view(), name='owner-export-orders-csv'),
    path('statistics/', StatisticsView.as_view(), name='owner-statistics'),

]
