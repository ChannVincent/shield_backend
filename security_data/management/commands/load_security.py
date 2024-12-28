import csv
import os
from django.core.management.base import BaseCommand
from ...models import Commune, Securite
from security_data.communes_filter import data_commune_filter

class Command(BaseCommand):
    help = 'Parse CSV data from file in the assets folder and load into the Commune and Securite models'

    def handle(self, *args, **kwargs):
        # Define the path to the CSV file in the assets folder
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'delinquance_par_commune.csv')

        # Ensure the file exists before attempting to read it
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} does not exist'))
            return
        
        # Open and parse the CSV file
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            progress = 0
            total_rows = sum(1 for _ in csv_file) - 1
            # Reset the file pointer to the start
            csv_file.seek(0) 
            reader = csv.DictReader(csv_file, delimiter=';')
            # Loop through each row in the CSV
            for row in reader:
                # Extract Commune based on CODGEO_2024
                code_commune = row["CODGEO_2024"]
                # don't do each rows (many hours to parse)
                if code_commune not in data_commune_filter:
                    continue

                try:
                    # Fetch the Commune (do not create if not found)
                    commune = Commune.objects.get(code_commune=code_commune)
                except Commune.DoesNotExist:
                    # Skip row if the commune does not exist
                    self.stdout.write(self.style.WARNING(f"Commune with code {code_commune} not found. Skipping row."))
                    continue

                # Now create the Securite instance for this row
                Securite.objects.create(
                    commune=commune,
                    year=f"20{row.get("annee", "")}",
                    agression_class=row.get("classe", ""),
                    aggression_unity=row.get("unité.de.compte", ""),
                    public_value=row.get("valeur.publiée", ""),
                    facts_value=row.get("faits", ""),
                    per_thousand=row.get("tauxpourmille", ""),
                    # complementinfoval=row.get("complementinfoval", ""),
                    # complementinfotaux=row.get("complementinfotaux", ""),
                    pop=row.get("POP", ""),
                    millpop=row.get("millPOP", ""),
                    # log=row.get("LOG", ""),
                    # milllog=row.get("millLOG", ""),
                )
                progress += 1

                # Print progress every 1000 records
                if progress % 1000 == 0:
                    self.stdout.write(self.style.NOTICE(f'Progress: {progress} / {total_rows} : {progress / total_rows * 100}%'))

            # Output success message after loading the data
            self.stdout.write(self.style.SUCCESS(f'CSV data successfully loaded into Securite model. {progress} rows processed.'))
