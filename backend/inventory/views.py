from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Vehicle, Purchase
from .serializers import RegisterSerializer, VehicleSerializer
from .permissions import IsAdminOrReadOnly
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[AllowAny]
class VehicleViewSet(viewsets.ModelViewSet):
    queryset=Vehicle.objects.all(); serializer_class=VehicleSerializer; permission_classes=[IsAuthenticated, IsAdminOrReadOnly]
    def get_queryset(self):
        qs=super().get_queryset()
        params=self.request.query_params
        for field in ('make','model','category'):
            value=params.get(field)
            if value: qs=qs.filter(**{field+'__icontains':value})
        try:
            if params.get('min_price'): qs=qs.filter(price__gte=params['min_price'])
            if params.get('max_price'): qs=qs.filter(price__lte=params['max_price'])
        except (ValueError, TypeError): pass
        return qs
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request, pk=None):
        qty=request.data.get('quantity',1)
        try: qty=int(qty)
        except (ValueError, TypeError): return Response({'detail':'Quantity must be a positive integer.'}, status=400)
        if qty < 1: return Response({'detail':'Quantity must be a positive integer.'}, status=400)
        with transaction.atomic():
            updated=Vehicle.objects.filter(pk=pk, quantity__gte=qty).update(quantity=F('quantity')-qty)
            if not updated:
                if not Vehicle.objects.filter(pk=pk).exists(): return Response({'detail':'Vehicle not found.'},status=404)
                return Response({'detail':'Insufficient stock.'},status=400)
            vehicle=Vehicle.objects.get(pk=pk)
            Purchase.objects.create(user=request.user,vehicle=vehicle,quantity=qty)
        return Response({'detail':'Purchase successful.','vehicle':VehicleSerializer(vehicle).data},status=200)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def restock(self, request, pk=None):
        if not request.user.is_staff: return Response({'detail':'Admin access required.'},status=403)
        try: qty=int(request.data.get('quantity',1))
        except (ValueError, TypeError): return Response({'detail':'Quantity must be a positive integer.'},status=400)
        if qty < 1: return Response({'detail':'Quantity must be a positive integer.'},status=400)
        vehicle=self.get_object(); Vehicle.objects.filter(pk=vehicle.pk).update(quantity=F('quantity')+qty); vehicle.refresh_from_db()
        return Response(VehicleSerializer(vehicle).data)
