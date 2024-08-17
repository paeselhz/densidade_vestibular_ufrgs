from shiny import App
from tabs.comparacao import comparacao_server, comparacao_ui

app_ui = comparacao_ui("comparacao")


def server(input, output, session):
    comparacao_server("comparacao")


app = App(app_ui, server)
