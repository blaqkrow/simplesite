from django.urls import include, path
from rest_framework import routers
from .views import (
    index, get_protein, get_domain, create_protein
)
from .api import (domain_detail, protein_list, protein_detail, 
                create_protein_detail, domain_list, domain_coverage)

# router = routers.DefaultRouter()
# router.register(r'protein', views.ProteinViewSet)
# router.register(r'pfam', views.DomainViewSet)
# router.register(r'proteins', views.ProteinViewSet)

urlpatterns = [
    # path('api', include(router.urls)),
    # path('api/protein/', ProteinListApiView.as_view()),
    # path('api/protein/<str:protein_id>/', ProteinDetailApiView.as_view()),
    # path('api/pfam/<str:domain_id>/', DomainDetailApiView.as_view()),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('', index, name='index'),
    path('create_protein/', create_protein, name='create_protein'),
    path('protein/<str:protein_id>', get_protein, name='get_protein'),
    path('domain/<str:domain_id>', get_domain, name='get_domain'),
    path('api/protein/', create_protein_detail, name='create_protein_detail_api'),
    path('api/protein/<str:protein_id>', protein_detail, name='protein_detail_api'),
    path('api/pfam/<str:domain_id>', domain_detail, name='domain_detail_api'),
    path('api/pfams/<str:taxa_id>', domain_list, name='domain_list_api'),
    path('api/proteins/<str:taxa_id>', protein_list, name='protein_list_api'),
    path('api/coverage/<str:protein_id>', domain_coverage, name='domain_coverage_api'),
]