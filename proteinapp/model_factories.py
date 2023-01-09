import factory
from random import randint

from .models import Domain, Protein, ProteinDomain, Taxonomy

# Factory to generate domains
class DomainFactory(factory.django.DjangoModelFactory):
    domain_id = factory.Sequence(lambda x: 'D%d' % x+str(1))
    domain_description = factory.Faker('sentence', nb_words=5)

    class Meta:
        model = Domain

# Factory to generate taxonomy
class TaxonomyFactory(factory.django.DjangoModelFactory):
    taxa_id = factory.Sequence(lambda x: 'T%d' % x+str(1))
    clade = factory.Faker('sentence', nb_words=1)
    genus = factory.Faker('sentence', nb_words=1)
    species = factory.Faker('sentence', nb_words=1)

    class Meta:
        model = Taxonomy

# Factory to generate protein domains
class ProteinDomainFactory(factory.django.DjangoModelFactory):
    protein = factory.SubFactory('proteinapp.model_factories.ProteinFactory')
    description = factory.Faker('sentence', nb_words=5)
    pfam_id = factory.SubFactory(DomainFactory)
    start = randint(1, 10000)
    stop = start + randint(1, 10000)

    class Meta:
        model = ProteinDomain

# Factory to generate proteins
class ProteinFactory(factory.django.DjangoModelFactory):
    protein_id = factory.Sequence(lambda x: 'D%d' % x+str(1))
    sequence = factory.Faker('pystr')
    taxonomy = factory.SubFactory(TaxonomyFactory)
    length = randint(1, 10000)

    class Meta:
        model = Protein
        
    @factory.post_generation
    def domains(self, create, extracted, **kwargs):
        if not create:
            # Simple build
            return

        if extracted:
            # A list of domains were passed in
            for domains in extracted:
                self.domains.add(domains)