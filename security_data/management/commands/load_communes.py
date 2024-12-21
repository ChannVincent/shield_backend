import csv
import os
from django.core.management.base import BaseCommand
from ...models import Commune

class Command(BaseCommand):
    help = 'Parse CSV data from file in the assets folder and load into the Commune model'

    def handle(self, *args, **kwargs):
        # Define the path to the CSV file in the assets folder
        file_path = os.path.join(os.path.dirname(__file__),  '..', '..', 'assets', 'code_commune_2024.csv')

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
            reader = csv.DictReader(csv_file)
            # Loop through each row in the CSV
            for row in reader:
                if row["TYPECOM"] != "COM":
                    continue  # Skip rows where TYPECOM is not "COM"

                # Create a new Commune instance with data from the row
                Commune.objects.create(
                    code_commune=row["COM"], 
                    region=row["REG"],  
                    department=row["DEP"],  
                    arrondissement=row["ARR"],
                    name_capital=row["NCC"],
                    name_order=row["NCCENR"],
                    name_full=row["LIBELLE"]
                )
                progress += 1
                if progress % 1000 == 0:
                    self.stdout.write(self.style.NOTICE(f'progress: {progress} / {total_rows} : {progress / total_rows * 100}%'))

            # Output success message after loading the data
            self.stdout.write(self.style.SUCCESS('CSV data successfully loaded into Commune model'))
