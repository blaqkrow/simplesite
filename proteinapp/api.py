from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError, transaction
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Domain, Protein, Taxonomy
from .serializers import (DomainSerializer, ProteinListSerializer, ProteinSerializer, 
                    CreateProteinSerializer, ProteinDomainListSerializer, TaxonomySerializer)

@api_view(['GET'])
def domain_detail(request, domain_id):
    try:
        # Get all domains
        domain = Domain.objects.get(domain_id=domain_id)
    except Domain.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = DomainSerializer(domain)
        return Response(serializer.data)

@api_view(['POST'])
def create_protein_detail(request):
    if request.method == "POST":
        serializer = CreateProteinSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create new protein
                with transaction.atomic():
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return HttpResponse(e, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def protein_detail(request, protein_id):
    try:
        # Get protein with protein id
        protein = Protein.objects.get(protein_id=protein_id)
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ProteinSerializer(protein, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def protein_list(request, taxa_id):
    try:
        # Get taxonomy with taxa id
        taxonomy = Taxonomy.objects.get(taxa_id=taxa_id)
        # Get proteins with taxonomy
        proteins = Protein.objects.filter(taxonomy=taxonomy)
    except Taxonomy.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ProteinListSerializer(proteins, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def domain_list(request, taxa_id):
    try:
        # Get taxonomy with taxa id
        taxonomy = Taxonomy.objects.get(taxa_id=taxa_id)
        # Get proteins with taxonomy
        proteins = Protein.objects.filter(taxonomy=taxonomy)
        combined = None
        # For each protein, get domains of protein
        for i, protein in enumerate(proteins):
            if i == 0:
                combined = protein.domains.all()
            combined = combined | protein.domains.all()
    except Taxonomy.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ProteinDomainListSerializer(combined, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def domain_coverage(request, protein_id):
    try:
        # Get protein with protein id
        protein = Protein.objects.get(protein_id=protein_id)
        total = 0
        # Calculate total coverage
        for protein_domain in protein.domains.all():
            total += protein_domain.stop - protein_domain.start
        coverage = total / protein.length
    except Protein.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        return Response(f"coverage: {coverage}")