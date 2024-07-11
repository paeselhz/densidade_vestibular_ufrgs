import os
import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd

class DensitiesUFRGS:

    def __init__(self):
        self.base_url = "https://www.ufrgs.br/vestibular/cv"

    def clear(self):
        self.year = None
        self.request_ufrgs = None
        self.table_courses = None
        self.df_list = None

    def build_url(self):
        return self.base_url + self.year + "/densidade/"

    def request_url(self):
        self.request_ufrgs = requests.get(self.build_url())
        return 0

    def run_bs4(self):
        soup = bs4(self.request_ufrgs.content, "html.parser")

        tabelas_cursos_div = soup.find('div', id = 'tabelasCursos')

        self.table_courses = tabelas_cursos_div.find_all('table', class_='col s12 curso')

        return 0
    
    def parse_table(self, bs4_table):
        print(bs4_table.find('th').text)
        table_data = []

        for row in bs4_table.find_all('tr'):
            cols = row.find_all('td')
            if cols:
                table_data.append([col.text for col in cols])
        table_data = [row if len(row) == 4 else row[:4] for row in table_data]
        df = pd.DataFrame(table_data, columns=['categoria', 'n_inscritos', 'n_vagas', 'drop'])
        df.drop('drop', axis = 1)
        df['n_inscritos'] = pd.to_numeric(df['n_inscritos'], errors='coerce')
        df['n_vagas'] = pd.to_numeric(df['n_vagas'], errors='coerce')
        df.fillna(0, inplace=True)

        df = pd.concat([df, pd.DataFrame([['Total', df['n_inscritos'].sum(), df['n_vagas'].sum()]], columns = ['categoria', 'n_inscritos', 'n_vagas'])])
        df['densidade'] = df['n_inscritos']/df['n_vagas']

        df['curso'] = bs4_table.find('th').text

        return df
        


    def run_extraction(self, years):

        self.year_df = []

        for year in years:
            print(year)
            self.year = year.__str__()
            self.request_url()

            self.run_bs4()

            self.df_list = []

            for table in self.table_courses:
                self.df_list.append(self.parse_table(table))

            final_df = pd.concat(self.df_list)
            final_df['ano'] = year

            self.year_df.append(final_df.copy())

        self.all_years = pd.concat(self.year_df)
            
        self.clear()
        return 1

    def export_parquet(self, folder = 'data'):
        os.makedirs(folder, exist_ok=True)
        self.all_years.drop('drop', axis = 1, inplace=True)
        self.all_years = self.all_years[['ano', 'curso', 'categoria', 'n_inscritos', 'n_vagas', 'densidade']]
        self.all_years.to_parquet(f"{folder}/densidades_vestibular_ufrgs.parquet")

        return 1

            
                


