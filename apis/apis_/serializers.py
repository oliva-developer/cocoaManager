from rest_framework import serializers
from .models import (
    Collaborator, Task, Article, Purchase, PurchaseDetail, 
    ToolMaintenance, WorkingDay, WorkingDayResource, SaleProduct
)

class CollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaborator
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer):
    details = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Purchase
        fields = '__all__'

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = '__all__'

class ToolMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolMaintenance
        fields = '__all__'

class WorkingDaySerializer(serializers.ModelSerializer):
    resources = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = WorkingDay
        fields = '__all__'

class WorkingDayResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDayResource
        fields = '__all__'

class SaleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleProduct
        fields = '__all__'