from django.db import models

# Model representing taxonomy
class Taxonomy(models.Model):
    taxa_id = models.CharField(max_length=60)
    clade = models.CharField(max_length=60)
    genus = models.CharField(max_length=60)
    species = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.taxa_id},{self.genus},{self.clade},{self.species}'

# Model representing domain
class Domain(models.Model):
    domain_id = models.CharField(max_length=60, primary_key=True)
    domain_description = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.domain_id},{self.domain_description}'

# Model representing protein
class Protein(models.Model):
    protein_id = models.CharField(max_length=60, unique=True)
    sequence = models.CharField(max_length=500)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.DO_NOTHING)
    length = models.IntegerField()
    domains = models.ManyToManyField('ProteinDomain', related_name='protein_domains', blank=True)

    def __str__(self):
        return f'{self.protein_id},{self.sequence},{self.length}'

# Model representing protein domain      
class ProteinDomain(models.Model):
    protein = models.ForeignKey(Protein, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    pfam_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    start = models.IntegerField()
    stop = models.IntegerField()

    def __str__(self):
        return f'{self.protein.protein_id},{self.description},{self.pfam_id.domain_id},{self.start},{self.stop}'
        

