library(shiny)
library(dplyr)
library(openxlsx)
library(highcharter)
library(shinyWidgets)

densidades_vestibular_ufrgs <-
  readr::read_rds('data/densidades_vestibular_ufrgs.rds')

js_tooltip <-
  paste0(
    "function(){return ('Curso: <strong>' +  this.point.curso + ",
    "'</strong> <br> Rank: ' + this.y + ",
    "' <br> Densidade: ' + this.point.densidade + ' alunos por vaga')}"
  )
