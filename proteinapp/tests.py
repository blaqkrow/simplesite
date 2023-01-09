import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import (DomainSerializer, ProteinListSerializer, ProteinSerializer, 
                    CreateProteinSerializer, ProteinDomainListSerializer, TaxonomySerializer)

# Test DomainSerializer
class DomainSerializerTest(APITestCase):
    domain_1 = None
    domain_serializer = None
    
    # Set up data before each test case
    def setUp(self):
        self.domain_1 = DomainFactory.create(domain_id='D1')
        self.domain_serializer = DomainSerializer(instance=self.domain_1)
    
    # Clean up data after each test case
    def tearDown(self):
        Domain.objects.all().delete()
        DomainFactory.reset_sequence(0)

    def test_domainSerializer(self):
        data = self.domain_serializer.data
        self.assertEqual(set(data.keys()), set(['domain_id', 'domain_description']))
        
    def test_domainSerializerDomainHasCorrectData(self):
        data = self.domain_serializer.data
        self.assertEqual(data['domain_id'], self.domain_1.domain_id)
        self.assertEqual(data['domain_description'], self.domain_1.domain_description)

# Test ProteinDomainSerializer
class ProteinDomainSerializerTest(APITestCase):
    protein_domain_1 = None
    protein_domain_2 = None
    protein_domain_serializer = None
    
    # Set up data before each test case
    def setUp(self):
        self.protein_domain_1 = ProteinDomainFactory.create(pfam_id__domain_id='D1', pfam_id__domain_description='D1 description', start=50, stop=100, description='D1 protein domain description')
        self.protein_domain_2 = ProteinDomainFactory.create(pfam_id__domain_id='D2', pfam_id__domain_description='D2 description', start=50, stop=100, description='D2 protein domain description')
        self.protein_domain_serializer = ProteinDomainListSerializer(instance=[self.protein_domain_1, self.protein_domain_2], many=True)
    
    # Clean up data after each test case
    def tearDown(self):
        ProteinDomain.objects.all().delete()
        ProteinDomainFactory.reset_sequence(0)

    def test_proteinDomainSerializer(self):
        data = self.protein_domain_serializer.data
        self.assertEqual(len(data), 2)
        self.assertEqual(set(data[0].keys()), set(['pfam_id', 'id']))
        self.assertEqual(set(data[0]['pfam_id'].keys()), set(['domain_id', 'domain_description']))
        
    def test_proteinDomainSerializerDomainHasCorrectData(self):
        data = self.protein_domain_serializer.data
        self.assertEqual(data[0]['pfam_id']['domain_id'], self.protein_domain_1.pfam_id.domain_id)
        self.assertEqual(data[0]['pfam_id']['domain_description'], self.protein_domain_1.pfam_id.domain_description)
        self.assertEqual(data[1]['pfam_id']['domain_id'], self.protein_domain_2.pfam_id.domain_id)
        self.assertEqual(data[1]['pfam_id']['domain_description'], self.protein_domain_2.pfam_id.domain_description)

# Test ProteinSerializer
class ProteinSerializerTest(APITestCase):
    protein_1 = None
    taxa_1 = None
    domain_1 = None
    protein_serializer = None
    
    # Set up data before each test case
    def setUp(self):
        self.taxa_1 = TaxonomyFactory.create(taxa_id='T1', clade='E', species='Species', genus='Genus')
        self.domain_1 = ProteinDomainFactory.create(pfam_id__domain_id='D1', pfam_id__domain_description='D1 description', start=50, stop=100, description='D1 protein domain description')
        self.protein_1 = ProteinFactory.create(protein_id='A1', sequence='ABCD', length=100, 
                                        taxonomy=self.taxa_1, domains=(self.domain_1,))
        self.protein_serializer = ProteinSerializer(instance=self.protein_1)
    
    # Clean up data after each test case
    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        TaxonomyFactory.reset_sequence(0)
        DomainFactory.reset_sequence(0)
        ProteinDomainFactory.reset_sequence(0)

    def test_proteinSerializer(self):
        data = self.protein_serializer.data
        print(data.keys())
        self.assertEqual(set(data.keys()), set(['protein_id', 'length', 'sequence', 'taxonomy', 'domains']))
        self.assertEqual(set(data['taxonomy'].keys()), set(['taxa_id', 'clade', 'genus', 'species']))
        self.assertEqual(len(data['domains']), 1)
        self.assertEqual(data['domains'][0].keys(), set(['pfam_id', 'description', 'start', 'stop']))
        
    def test_proteinSerializerProteinHasCorrectData(self):
        data = self.protein_serializer.data
        self.assertEqual(data['protein_id'], 'A1')
        self.assertEqual(data['taxonomy']['clade'], 'E')
        self.assertEqual(data['taxonomy']['species'], 'Species')
        self.assertEqual(data['taxonomy']['genus'], 'Genus')
        self.assertEqual(data['taxonomy']['taxa_id'], 'T1')
        self.assertEqual(len(data['domains']), 1)
        self.assertEqual(data['domains'][0]['pfam_id']['domain_id'], 'D1')
        self.assertEqual(data['domains'][0]['pfam_id']['domain_description'], 'D1 description')
        self.assertEqual(data['domains'][0]['start'], 50)
        self.assertEqual(data['domains'][0]['stop'], 100)
        self.assertEqual(data['domains'][0]['description'], 'D1 protein domain description')

# Test TaxonomySerializer
class TaxonomySerializerTest(APITestCase):
    taxonomy_1 = None
    taxonomy_serializer = None
    
    # Set up data before each test case
    def setUp(self):
        self.taxonomy_1 = TaxonomyFactory.create(taxa_id='T1')
        self.taxonomy_serializer = TaxonomySerializer(instance=self.taxonomy_1)
    
    # Clean up data after each test case
    def tearDown(self):
        Taxonomy.objects.all().delete()
        TaxonomyFactory.reset_sequence(0)

    def test_taxonomySerializer(self):
        data = self.taxonomy_serializer.data
        self.assertEqual(set(data.keys()), set(['taxa_id', 'genus', 'clade', 'species']))
        
    def test_taxonomySerializerTaxonomyHasCorrectData(self):
        data = self.taxonomy_serializer.data
        self.assertEqual(data['taxa_id'], self.taxonomy_1.taxa_id)
        self.assertEqual(data['genus'], self.taxonomy_1.genus)
        self.assertEqual(data['clade'], self.taxonomy_1.clade)
        self.assertEqual(data['species'], self.taxonomy_1.species)

# Test Domain
class DomainTest(APITestCase):
    domain_1 = None
    good_url = ''
    bad_url = ''

    # Set up data before each test case
    def setUp(self):
        self.domain_1 = DomainFactory.create(domain_id='D1', domain_description='D1 description')
        self.good_url = reverse('domain_detail_api', kwargs={'domain_id': 'D1'})
        self.bad_url = '/api/pfam/H'

    # Clean up data after each test case
    def tearDown(self):
        Domain.objects.all().delete()
        DomainFactory.reset_sequence(0)

    def test_domainDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('domain_id' in data)
        self.assertEqual(data['domain_id'], 'D1')
        self.assertEqual(data['domain_description'], 'D1 description')

    def test_domainDetailReturnFailOnBadDomainId(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

# Test Protein
class ProteinTest(APITestCase):
    protein_1 = None
    protein_2 = None
    protein_3 = None
    good_url = ''
    bad_url = ''
    create_url = ''

    # Set up data before each test case
    def setUp(self):
        taxa_1 = TaxonomyFactory.create(taxa_id='T1', clade='E', species='Species', genus='Genus')
        taxa_2 = TaxonomyFactory.create(taxa_id='T2', clade='F', species='Species1', genus='Genus1')
        domain_1 = ProteinDomainFactory.create(pfam_id__domain_id='D1', pfam_id__domain_description='D1 description', start=50, stop=100, description='D1 protein domain description')
        domain_2 = ProteinDomainFactory.create(pfam_id__domain_id='D2', pfam_id__domain_description='D2 description', start=40, stop=90, description='D2 protein domain description')
        domain_3 = ProteinDomainFactory.create(pfam_id__domain_id='D3', pfam_id__domain_description='D3 description', start=30, stop=110, description='D3 protein domain description')
        self.protein_1 = ProteinFactory.create(protein_id='A1', sequence='ABCD', length=100, 
                                        taxonomy=taxa_1, domains=(domain_1,))
        self.protein_2 = ProteinFactory.create(protein_id='A2', sequence='EFGH', length=200,
                                        taxonomy=taxa_1, domains=(domain_2,))
        self.protein_2 = ProteinFactory.create(protein_id='A3', sequence='EFGH', length=200,
                                        taxonomy=taxa_2, domains=(domain_3,))
        self.good_url = reverse('protein_detail_api', kwargs={'protein_id': 'A1'})
        self.good_protein_list_url = reverse('protein_list_api', kwargs={'taxa_id': 'T1'})
        self.bad_protein_list_url = '/api/proteins/A'
        self.good_domain_list_url = reverse('domain_list_api', kwargs={'taxa_id': 'T1'})
        self.bad_domain_list_url = '/api/pfams/A'
        self.good_domain_coverage_url = reverse('domain_coverage_api', kwargs={'protein_id': 'A1'})
        self.bad_domain_coverage_url = '/api/coverage/A'
        self.bad_url = '/api/protein/H'
        self.create_protein_data = {
            "protein_id": "A4",
            "sequence": "MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA",
            "taxonomy": {
            "taxa_id": "T1",
            "clade": "E",
            "genus": "Ancylostoma",
            "species": "ceylanicum"
            },
            "length": 101,
            "domains": [
            {
            "pfam_id": {
            "domain_id": "D1",
            "domain_description": "PeptidaseC13family"
            },
            "description": "Peptidase C13 legumain",
            "start": 40,
            "stop": 94
            }]
        }

    # Clean up data after each test case
    def tearDown(self):
        Protein.objects.all().delete()
        ProteinFactory.reset_sequence(0)
        TaxonomyFactory.reset_sequence(0)
        DomainFactory.reset_sequence(0)
        ProteinDomainFactory.reset_sequence(0)

    def test_proteinDetailReturnSuccess(self):
        response = self.client.get(self.good_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue('protein_id' in data)
        self.assertEqual(data['protein_id'], 'A1')
        self.assertEqual(data['taxonomy']['clade'], 'E')
        self.assertEqual(data['taxonomy']['species'], 'Species')
        self.assertEqual(data['taxonomy']['genus'], 'Genus')
        self.assertEqual(data['taxonomy']['taxa_id'], 'T1')
        self.assertEqual(len(data['domains']), 1)
        self.assertEqual(data['domains'][0]['pfam_id']['domain_id'], 'D1')
        self.assertEqual(data['domains'][0]['pfam_id']['domain_description'], 'D1 description')
        self.assertEqual(data['domains'][0]['start'], 50)
        self.assertEqual(data['domains'][0]['stop'], 100)
        self.assertEqual(data['domains'][0]['description'], 'D1 protein domain description')

    def test_proteinDetailReturnFailOnBadProteinId(self):
        response = self.client.get(self.bad_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_proteinDetailCreateReturnSuccess(self):
        response = self.client.post('/api/protein/', self.create_protein_data, format="json")
        self.assertEqual(response.status_code, 201)

    def test_proteinDetailCreateReturnFailureOnExistingProteinId(self):
        bad_data = self.create_protein_data
        bad_data['protein_id'] = self.protein_1.protein_id
        response = self.client.post('/api/protein/', bad_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_proteinListReturnSuccess(self):
        response = self.client.get(self.good_protein_list_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['protein_id'], 'A1')
        self.assertEqual(data[1]['protein_id'], 'A2')

    def test_proteinListReturnFailureOnBadTaxaId(self):
        response = self.client.get(self.bad_protein_list_url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_domainListReturnSuccess(self):
        response = self.client.get(self.good_domain_list_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['pfam_id']['domain_id'], 'D1')
        self.assertEqual(data[0]['pfam_id']['domain_description'], 'D1 description')
        self.assertEqual(data[1]['pfam_id']['domain_id'], 'D2')
        self.assertEqual(data[1]['pfam_id']['domain_description'], 'D2 description')

    def test_domainCoverageReturnSuccess(self):
        response = self.client.get(self.good_domain_coverage_url, format='json')
        response.render()
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data, "coverage: 0.5")

    def test_domainCoverageReturnFailureOnBadProteinId(self):
        response = self.client.get(self.bad_domain_coverage_url, format='json')
        self.assertEqual(response.status_code, 400)
