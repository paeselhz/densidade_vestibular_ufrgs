
fluidPage(
  title = "Comparação Densidades UFRGS",
  fluidRow(
    column(
      width = 12,
      h1("Comparação densidades para ingresso pelo Vestibular UFRGS",
         align = "center"),
      hr()
    )
  ),
  column(
    width = 3,
    prettyCheckboxGroup(
      inputId = "anos_comparacao",
      label = "Anos para comparação",
      choices = densidades_vestibular_ufrgs %>% pull(ano) %>% unique(),
      selected = densidades_vestibular_ufrgs %>% pull(ano) %>% unique(),
      status = "primary",
      shape = "curve",
      outline = TRUE
    ),
    awesomeRadio(
      inputId = "ano_base",
      label = "Ano base de comparação", 
      choices = densidades_vestibular_ufrgs %>% pull(ano) %>% unique(),
      selected = densidades_vestibular_ufrgs %>% pull(ano) %>% unique() %>% max(),
      checkbox = TRUE
    ),
    pickerInput(
      inputId = "categoria_ingresso",
      label = "Modalidade de Ingresso", 
      choices = densidades_vestibular_ufrgs %>% pull(categoria) %>% unique(),
      options = list(
        `live-search` = TRUE
        )
    ),
    downloadButton('download_densidades', 'Baixar os dados')
  ),
  column(
    width = 9,
    highchartOutput('plot_cursos')
  )
)