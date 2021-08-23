from django.db.models import query
from django.db.models.query import QuerySet
from .models import Tutorial
from .serializers import TutorialSerializer
from rest_framework import mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000

class TutorialHandler(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    pagination_class = StandardResultsSetPagination
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()

    def get(self, request, *args, **kwargs):
        tutorials = get_object_or_404(self.queryset, id=self.kwargs.get('pk'))
        serializers = self.serializer_class(tutorials)
        return Response(serializers.data)

    def delete(self, request, *args, **kwargs):
        if self.kwargs.get('pk'):                
            # tutorials = get_object_or_404(self.queryset, id=self.kwargs.get('pk'))
            # tutorials.delete()
            # return Response({"details": f"item with id : {self.kwargs.get('pk')} deleted"})
            return mixins.DestroyModelMixin.destroy(request, *args, **kwargs)
        else:
            count_deleted = self.queryset.delete()[0]
            return Response({'details': f'{count_deleted} rows deleted'})
            
    
class PublishedHandler(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    pagination_class = StandardResultsSetPagination
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.filter(published__in=[True])