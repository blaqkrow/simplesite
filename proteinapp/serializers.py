from rest_framework import serializers

from .models import Domain, Protein, ProteinDomain, Taxonomy

# Serialiser for domain
class DomainSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain_id', 'domain_description']

# Serialiser for protein domain list
class ProteinDomainListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    pfam_id = DomainSerializer(required=True)

# Serialiser for protein list
class ProteinListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Protein
        fields = ["id", "protein_id"]

# Serialiser for taxonomy
class TaxonomySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ['taxa_id', 'genus', 'clade', 'species']

# Serialiser for protein domain
class ProteinDomainSerializer(serializers.Serializer):
    pfam_id = DomainSerializer(required=True)
    start = serializers.IntegerField()
    stop = serializers.IntegerField()
    description = serializers.CharField(max_length=200)

# Serialiser for protein
class ProteinSerializer(serializers.Serializer):
    protein_id = serializers.CharField(max_length=60)
    sequence = serializers.CharField(max_length=200)
    taxonomy = TaxonomySerializer(required=True)
    length = serializers.IntegerField()
    domains = ProteinDomainSerializer(many=True) 

# Serialiser for create protein
class CreateProteinSerializer(serializers.Serializer):
# class ProteinSerializer(serializers.HyperlinkedModelSerializer):
    # domains = ProteinDomainSerializer(many=True)
    # taxonomy = serializers.HyperlinkedIdentityField(view_name="proteinapp:taxonomy-detail")
    # class Meta:
    #     model = Protein
    #     fields = ['protein_id', 'taxonomy', 'length', 'sequence', 'domains']

    taxonomy = TaxonomySerializer(required=True)
    # domains = ProteinDomainSerializer(many=True) 
    protein_id = serializers.CharField(max_length=60)
    length = serializers.IntegerField()
    sequence = serializers.CharField(max_length=200)

    # Create a new protein
    def create(self, validated_data):
        taxa_data = self.initial_data.get('taxonomy')
        domains_data = self.initial_data.get('domains')
        print('domains_data', domains_data)
        print('taxa_data', taxa_data)
        protein = Protein(**{**validated_data,
                        'taxonomy': Taxonomy.objects.get(taxa_id=taxa_data['taxa_id']),})
                        # 'domains': Domain.objects.filter(pk__in=domains_data_mapped)})
        print('protein', protein)
        protein.save()

        # Add domains for protein if any
        if domains_data and len(domains_data) > 0:
            domains_data_mapped = list(map(lambda x:x['pfam_id']['domain_id'], domains_data))
            for domain_data in domains_data:
                protein_domain = ProteinDomain(protein=protein, pfam_id=Domain.objects.get(domain_id=domain_data['pfam_id']['domain_id']), 
                            start=domain_data['start'], stop=domain_data['stop'], description=domain_data['description'])
                protein_domain.save()
                protein.domains.add(protein_domain)
            protein.save()

        return protein
