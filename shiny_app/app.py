from tabs.comparacao import comparacao_ui, comparacao_server
from shiny import App

app_ui = comparacao_ui("comparacao")

def server(input, output, session):
    comparacao_server("comparacao")

app = App(app_ui, server)