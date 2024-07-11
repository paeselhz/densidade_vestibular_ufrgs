from utils import DensitiesUFRGS

ufrgs = DensitiesUFRGS()

ufrgs.run_extraction([2017, 2018, 2019, 2020, 2022, 2023, 2024])

ufrgs.export_parquet()
