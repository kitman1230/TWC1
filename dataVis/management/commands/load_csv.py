import pandas as pd
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand
from dataVis.models import ENERGY


class Command(BaseCommand):
    help = "Load data from file..."

    def handle(self, *args, **options):
        csv_fn = input("Please input the CSV file name: ")
        dataFile = settings.BASE_DIR / "data" / csv_fn
        sr = int(input("Please input rows need to be skipped: "))
        nr = int(input("Please input rows need to be collected: "))

        dt = pd.read_csv(dataFile, skiprows=sr, nrows=nr, index_col=0, sep=";")
        l_cols = list(dt.columns)
        l_rows = list(dt.index)

        for col in l_cols:
            for row in l_rows:
                ENERGY.objects.get_or_create(
                    energyYear=int(col),
                    energyType=row,
                    energyUsed=float(dt[col].loc[row]),
                )
