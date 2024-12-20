from django.db import models

class Commune(models.Model):
    code_commune = models.CharField(max_length=20) # COM 77058
    region = models.CharField(max_length=20) # REG 11
    department = models.CharField(max_length=20) # DEP 77
    arrondissement = models.CharField(max_length=20) # ARR 775
    name_capital = models.CharField(max_length=200) # NCC BUSSY SAINT GEORGES
    name_order = models.CharField(max_length=200) # NCCENR Bussy-Saint-Georges
    name_full = models.CharField(max_length=200) # LIBELLE Bussy-Saint-Georges

    def __str__(self):
        return f"{self.name_full} ({self.code_commune})"
    

class Securite(models.Model):
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, null=True, default=None)
    year = models.CharField(max_length=20) # annee 16
    agression_class = models.CharField(max_length=200) # classe
    aggression_unity = models.CharField(max_length=200) # unité.de.compte
    public_value = models.CharField(max_length=20) # valeur.publiée
    facts_value = models.CharField(max_length=20) # faits
    per_thousand = models.CharField(max_length=20) # tauxpourmille
    complementinfoval = models.CharField(max_length=20) # complementinfoval
    complementinfotaux = models.CharField(max_length=20) # complementinfotaux
    pop = models.CharField(max_length=20) # POP
    millpop = models.CharField(max_length=20) # millPOP
    log = models.CharField(max_length=20) # LOG
    milllog = models.CharField(max_length=20) # millLOG

    def __str__(self):
        return f"{self.commune.name_full} (20{self.year}) : {self.agression_class}"