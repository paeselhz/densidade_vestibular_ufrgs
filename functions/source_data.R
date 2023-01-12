source('functions/get_densities_ufrgs.R')

densidades_vestibular_ufrgs <-
  purrr::map_df(
    2017:2023,
    get_densities_ufrgs
  )

readr::write_rds(densidades_vestibular_ufrgs, 
                 'data/densidades_vestibular_ufrgs.rds')
