library(dplyr)

standardize_table <-
  function(df) {
    
    nome_tabela <- colnames(df)[1]
    
    df <-
      df[,(ncol(df)-3):ncol(df)-1]
    
    colnames(df) <-
      c(
        'categoria',
        'n_inscritos',
        'n_vagas',
        'densidade'
      )
    
    df_clean <- 
      df %>% 
      select(-densidade) %>% 
      mutate(
        n_inscritos = ifelse(is.na(n_inscritos), 0, n_inscritos),
        n_vagas = ifelse(is.na(n_vagas), 0, n_vagas),
        curso = nome_tabela
      )
    
    df_totals <-
      tibble(
        curso = nome_tabela,
        categoria = 'Total',
        n_inscritos = df_clean %>% pull(n_inscritos) %>% sum(),
        n_vagas = df_clean %>% pull(n_vagas) %>% sum()
      ) %>% 
      bind_rows(df_clean) %>% 
      filter(
        n_vagas > 0
      ) %>% 
      mutate(
        densidade = n_inscritos/n_vagas
      ) 
    
    return(df_totals)
    
  }
