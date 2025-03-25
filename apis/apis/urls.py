from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apis_.views import (
    CollaboratorViewSet, TaskViewSet, ArticleViewSet, PurchaseViewSet,
    PurchaseDetailViewSet, ToolMaintenanceViewSet, WorkingDayViewSet,
    WorkingDayResourceViewSet, SaleProductViewSet
)

router = routers.DefaultRouter()
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'purchase-details', PurchaseDetailViewSet)
router.register(r'tool-maintenances', ToolMaintenanceViewSet)
router.register(r'working-days', WorkingDayViewSet)
router.register(r'working-day-resources', WorkingDayResourceViewSet)
router.register(r'sale-products', SaleProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]