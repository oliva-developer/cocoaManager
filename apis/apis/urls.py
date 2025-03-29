from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from apis_.views import (
    CollaboratorViewSet, TaskViewSet, ArticleViewSet, PurchaseViewSet,
    PurchaseDetailViewSet, ToolMaintenanceViewSet, WorkingDayViewSet,
    SaleProductViewSet
)
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'collaborators', CollaboratorViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'purchase-details', PurchaseDetailViewSet)
router.register(r'tool-maintenances', ToolMaintenanceViewSet)
router.register(r'working-days', WorkingDayViewSet)
router.register(r'sale-products', SaleProductViewSet)

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include(router.urls)),
    path('dash/', include('django_plotly_dash.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)