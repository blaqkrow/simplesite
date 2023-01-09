from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import DomainSerializer, ProteinSerializer, ProteinDomainSerializer, TaxonomySerializer
from .models import Domain, Protein, ProteinDomain, Taxonomy
from .forms import ProteinForm


# class DomainViewSet(viewsets.ModelViewSet):
#     queryset = Domain.objects.all()
#     serializer_class = DomainSerializer

# class ProteinDomainViewSet(viewsets.ModelViewSet):
#     queryset = ProteinDomain.objects.all()
#     serializer_class = ProteinDomainSerializer

# class ProteinViewSet(viewsets.ModelViewSet):
#     queryset = Protein.objects.all()
#     serializer_class = ProteinSerializer

# class TaxonomyViewSet(viewsets.ModelViewSet):
#     queryset = Taxonomy.objects.all()
#     serializer_class = TaxonomySerializer

# class DomainDetailApiView(APIView):
#     def get_object(self, domain_id):
#         try:
#             return Domain.objects.get(domain_id=domain_id)
#         except Domain.DoesNotExist:
#             return None

#     def get(self, request, domain_id, *args, **kwargs):
#         domain = self.get_object(domain_id)
#         if not domain:
#             return Response(
#                 {"res": "Domain with domain id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = DomainSerializer(domain, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
# class ProteinListApiView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = {
#             'sequence': request.data.get('sequence'), 
#             'protein_id': request.data.get('protein_id'), 
#             'length': request.data.get('length'), 
#         }
#         taxonomy = get_object_or_404(Taxonomy, taxa_id=request.data.get('taxa_id'))
#         data['taxonomy'] = taxonomy
#         data['domains'] = []
#         serializer = ProteinSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProteinDetailApiView(APIView):
#     def get_object(self, protein_id):
#         try:
#             return Protein.objects.get(protein_id=protein_id)
#         except Protein.DoesNotExist:
#             return None

#     def get(self, request, protein_id, *args, **kwargs):
#         protein = self.get_object(protein_id)
#         if not protein:
#             return Response(
#                 {"res": "Protein with protein id does not exists"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = ProteinSerializer(protein, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)


# Home page
def index(request):
    proteins = Protein.objects.all()
    domains = Domain.objects.all()
    return render(request, 'proteindata/index.html', {'proteins': proteins, 'domains': domains})

# Protein detail page
def get_protein(request, protein_id):
    protein = Protein.objects.get(protein_id=protein_id)
    return render(request, 'proteindata/protein.html', {'protein': protein, 'domains': protein.domains.all()})

# Domain detail page
def get_domain(request, domain_id):
    domain = Domain.objects.get(domain_id=domain_id)
    return render(request, 'proteindata/domain.html', {'domain': domain})

# Create protein page
def create_protein(request):
    proteins = Protein.objects.all()
    if request.method == 'POST':
        form = ProteinForm(request.POST)
        # Check form fields validity
        if form.is_valid():
            # Create protein
            protein = Protein()
            protein.protein_id = form.cleaned_data['protein_id']
            protein.length = form.cleaned_data['length']
            protein.sequence = form.cleaned_data['sequence']
            protein.taxonomy = form.cleaned_data['taxonomy']
            protein.save()
            return HttpResponseRedirect('/create_protein/')
        else:
            return render(request, 'proteindata/protein_create.html', {'proteins': proteins, 'form': form, 'error': 'failed'})
    else:
        form = ProteinForm()
        return render(request, 'proteindata/protein_create.html', {'proteins': proteins, 'form': form})