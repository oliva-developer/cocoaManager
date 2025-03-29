from rest_framework import viewsets
from .models import (
    Collaborator, Task, Article, Purchase, PurchaseDetail, 
    ToolMaintenance, WorkingDay, SaleProduct
)
from .serializers import (
    CollaboratorSerializer, TaskSerializer, ArticleSerializer, PurchaseSerializer, 
    PurchaseDetailSerializer, ToolMaintenanceSerializer, WorkingDaySerializer, SaleProductSerializer
)

class CollaboratorViewSet(viewsets.ModelViewSet):
    queryset = Collaborator.objects.all()
    serializer_class = CollaboratorSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class PurchaseDetailViewSet(viewsets.ModelViewSet):
    queryset = PurchaseDetail.objects.all()
    serializer_class = PurchaseDetailSerializer

class ToolMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = ToolMaintenance.objects.all()
    serializer_class = ToolMaintenanceSerializer

class WorkingDayViewSet(viewsets.ModelViewSet):
    queryset = WorkingDay.objects.all()
    serializer_class = WorkingDaySerializer

class SaleProductViewSet(viewsets.ModelViewSet):
    queryset = SaleProduct.objects.all()
    serializer_class = SaleProductSerializer