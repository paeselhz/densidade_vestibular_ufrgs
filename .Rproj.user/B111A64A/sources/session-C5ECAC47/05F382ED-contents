shinyServer(
  function(input, output, session) {
    
    observe({
      
      updateAwesomeRadio(
        session,
        inputId = "ano_base",
        choices = input$anos_comparacao,
        selected = max(input$anos_comparacao)
      )
      
    })
    
    output$plot_cursos <-
      renderHighchart({
        
        # browser()
        
        top_10_cursos_por_ano <-
          densidades_vestibular_ufrgs %>%
          filter(
            ano %in% input$anos_comparacao
          ) %>% 
          group_split(ano) %>% 
          purrr::map_df(
            function(x) {
              
              x %>% 
                filter(
                  categoria == input$categoria_ingresso
                ) %>% 
                arrange(desc(densidade)) %>% 
                head(10) %>% 
                mutate(
                  rank = 1,
                  rank = cumsum(rank)
                )
              
            }
          ) %>% 
          mutate(
            curso = stringr::str_replace(curso, " - Bacharelado", "")
          )
        
        text_modalidade_ingresso <-
          ifelse(input$categoria_ingresso == "Total",
                 "Utilizando todos os inscritos e vagas",
                 paste0("Modalidade de Ingresso: ", input$categoria_ingresso))
        
        top_10_cursos_por_ano %>% 
          filter(
            curso %in% c(top_10_cursos_por_ano %>% 
                           filter(ano == input$ano_base) %>% 
                           pull(curso))
          ) %>% 
          mutate(
            densidade = round(densidade, digits = 2)
          ) %>% 
          hchart(
            "spline",
            hcaes(x = ano, y = rank, group = curso)
          ) %>% 
          hc_yAxis(
            title = "",
            categories = paste0("Rank ", 0:10),
            reversed = TRUE,
            tickInterval = 1,
            min = 1,
            max = 10,
            gridLineWidth = 0
          ) %>% 
          hc_xAxis(
            title = "Ano",
            gridLineWidth = 0
          ) %>% 
          hc_tooltip(
            formatter = JS(js_tooltip)
          ) %>% 
          hc_legend(
            align = "left",
            verticalAlign = "bottom",
            layout = "vertical"
          ) %>% 
          hc_exporting(enabled = TRUE) %>% 
          hc_title(
            text = "Comparação das Densidades para Ingresso pelo Vestibular UFRGS",
            margin = 20,
            align = "center"
          ) %>% 
          hc_subtitle(
            text = paste0(
              "Utilizando ", input$ano_base, " como ano-base <br>",
              text_modalidade_ingresso
            ),
            align = "center"
          )
        
        
      })
    
    output$download_densidades <-
      downloadHandler(
        filename = function() { 
          paste("densidades_vestibular_ufrgs.xlsx", sep="")
        },
        content = function(file) {
          # writexl::write_xlsx(densidades_vestibular_ufrgs, file)
          openxlsx::write.xlsx(densidades_vestibular_ufrgs, file)
        })
    
  }
)