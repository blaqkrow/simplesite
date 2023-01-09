from proteinapp.models import Protein, Domain, ProteinDomain, Taxonomy
import csv


def run():
    Protein.objects.all().delete()
    Domain.objects.all().delete()
    ProteinDomain.objects.all().delete()
    Taxonomy.objects.all().delete()

    protein_domains = []
    protein_lengths = {}
    protein_taxonomy = {}

    # with open('scripts/3.csv') as file:
    with open('scripts/pfam_descriptions.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            domain_id = row[0]
            domain_description = row[1]
            domain = Domain(domain_id=row[0],
                        domain_description=row[1])
            domain.save()

    # with open('scripts/2.csv') as file:
    with open('scripts/assignment_data_set.csv') as file:
        reader = csv.reader(file)
        # next(reader)

        for row in reader:
            protein_id = row[0]
            taxa_id = row[1]
            clade = row[2]
            genus = row[3].split(' ')[0]
            species = row[3].split(' ')[1]
            description = row[4]
            domain_id = row[5]
            start = row[6]
            stop = row[7]
            length = row[8]
            print(row)

            taxonomy = Taxonomy.objects.filter(taxa_id=taxa_id).first()
            if not taxonomy:
                taxonomy = Taxonomy(taxa_id=taxa_id, clade=clade, 
                                genus=genus, species=species)
                taxonomy.save()
            
            # protein_lengths[protein_id] = length
            # protein_taxonomy[protein_id] = taxa_id
            protein_domains.append({
                "start": start,
                "stop": stop,
                "description": description,
                "domain_id": domain_id,
                "protein_id": protein_id
            })            
            protein = Protein.objects.filter(protein_id=protein_id).first()
            if not protein:
                protein = Protein(protein_id=protein_id, sequence='', taxonomy=taxonomy, length=length)
                protein.save()

    # with open('scripts/1.csv') as file:
    with open('scripts/assignment_data_sequences.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            protein_id = row[0]
            sequence = row[1]
            # taxa_id = protein_taxonomy[protein_id]
            # taxonomy = Taxonomy.objects.get(taxa_id=taxa_id)
            protein = Protein.objects.get(protein_id=protein_id)
            protein.sequence = sequence
            protein.save()
    
    for protein_domain in protein_domains:
        protein_id = protein_domain['protein_id']
        start = protein_domain['start']
        stop = protein_domain['stop']
        description = protein_domain['description']
        domain_id = protein_domain['domain_id']
        protein = Protein.objects.get(protein_id=protein_id)
        pfam = Domain.objects.get(domain_id=domain_id)
        protein_domain = ProteinDomain(pfam_id=pfam, protein=protein, start=start, stop=stop, description=description)
        protein_domain.save()
        protein.domains.add(protein_domain)
        protein.save()
