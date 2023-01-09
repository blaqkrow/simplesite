from django.contrib import admin
from .models import Protein, Domain, ProteinDomain, Taxonomy

# Register all models
admin.site.register(Protein)
admin.site.register(Domain)
admin.site.register(ProteinDomain)
admin.site.register(Taxonomy)