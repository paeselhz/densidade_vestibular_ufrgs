from functions.utils import DensitiesUFRGS

ufrgs = DensitiesUFRGS()


ufrgs.run_extraction([2023])

ufrgs.build_url()

ufrgs.request_ufrgs.content

# soup = BeautifulSoup(response.content, 'html.parser')
soup = bs4(ufrgs.request_ufrgs.content, "html.parser")

idx = 23

tabelas_cursos_div = soup.find('div', id = 'tabelasCursos')

specific_table = tabelas_cursos_div.find_all('table', class_='col s12 curso')
print(specific_table)

specific_table[0]

specific_table[0].find_all('th')