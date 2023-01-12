library(rvest)

source('functions/standardize_table.R')

get_densities_ufrgs <-
  function(year) {
    
    if(year == 2021) {
      
      message("Nao ha dados para 2021")
      return(tibble(NULL))
      
    }
    
    tictoc::tic(
      paste0("Densidade dos cursos da UFRGS para ", year)
    )
    
    url_densidades <- paste0("https://www.ufrgs.br/vestibular/cv", year, "/densidade/")
    
    html_source_ufrgs <- rvest::read_html(url_densidades)
    
    densidades_ufrgs <- 
      purrr::map_df(
        1:100,
        function(idx, html_source = html_source_ufrgs) {
          
          xpath_curso <- paste0('//*[@id="tabelasCursos"]/table[', idx, ']')
          
          tryCatch({
            
            table_curso <-
              html_source %>% 
              rvest::html_element(xpath = xpath_curso) %>% 
              html_table() %>% 
              standardize_table()
            
            # message(table_curso %>% pull(curso) %>% unique())
            
            return(table_curso)
            
          },
          error = function(cond) {
            
            return(tibble(NULL))
            
          })
          
        }
      )
    
    densidades_ufrgs <-
      densidades_ufrgs %>% 
      mutate(
        ano = year
      ) %>% 
      relocate(
        ano, .before = curso
      )
    
    tictoc::toc()
    
    return(densidades_ufrgs)
    
  }
