from django.conf.urls import include, url
from django.contrib import admin

from core.models import archive
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, mixins

#  Serializers define the API representation.
class ArchiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = archive
        fields = ('matchid', 'date', 'hero', 'opponent_hero', 'hero_deck',
            'opponent_deck','cards', 'opponent_cards' ,'coin','result')

# ViewSets define the view behavior.

class ArchiveViewSet(viewsets.ReadOnlyModelViewSet): #viewsets.ModelViewSet):
    queryset = archive.objects.all()
    serializer_class = ArchiveSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'matchs', ArchiveViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('core.urls'), name='home'),
    #url(r'^$', include('core.urls'), name='home'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
]
