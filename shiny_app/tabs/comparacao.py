import pandas as pd
from shiny import module, ui, render, reactive
from pathlib import Path
# from .utils import bumpchart

dados_vestibular = pd.read_parquet(Path(__file__).parent.parent / 'data/densidades_vestibular_ufrgs.parquet')
dados_vestibular['ano'] = dados_vestibular['ano'].astype(str)
dados_vestibular = dados_vestibular[dados_vestibular['n_vagas'] > 0]

anos_base = dados_vestibular['ano'].drop_duplicates().to_list()
anos_base.sort()

modalidades_ingresso = dados_vestibular['categoria'].drop_duplicates().to_list()
modalidades_ingresso.sort()

@module.ui
def comparacao_ui():
    comparacao_ui = ui.page_fluid(
        ui.row(
            ui.h1("Comparação densidades para ingresso pelo Vestibular UFRGS", style = "text-align:center")
        ),
        ui.hr(),
        ui.row(
            ui.column(
                3,
                ui.input_checkbox_group(
                    "anos_comparacao",
                    "Anos para comparação:",
                    [{year: ui.span(year) for year in anos_base}][0],
                    selected=anos_base
                ),
                ui.input_radio_buttons(
                    "ano_base",
                    "Ano base de comparação:",
                    [{year: ui.span(year) for year in anos_base}][0],
                    selected = anos_base[-1]
                ),
                ui.input_select(
                    "modalidade_ingresso",
                    "Modalidade de ingresso",
                    [{mod: ui.span(mod) for mod in modalidades_ingresso}][0],
                    selected = "Total"
                ),
                ui.h6("Download Button pending", style="color: #e6e6e6e"),
            ),
            ui.column(
                9,
                ui.output_table("comp_bump_chart")
            )
        )
    )
    return comparacao_ui

@module.server
def comparacao_server(input, output, session):
    @output
    @render.table
    def comp_bump_chart():

        if input.anos_comparacao().__len__() > 0:
            # vest_filtro = dados_vestibular[dados_vestibular['categoria'] == "Total"]
            vest_filtro = dados_vestibular[dados_vestibular['categoria'] == input.modalidade_ingresso()]
            # df = pd.concat([vest_filtro[vest_filtro['ano'] == selected_year].sort_values("densidade", ascending=False)[0:10] for selected_year in ["2022", "2023", "2024"]], axis=0)
            df = pd.concat([vest_filtro[vest_filtro['ano'] == selected_year].sort_values("densidade", ascending=False)[0:10] for selected_year in input.anos_comparacao()], axis=0)
        else:
            df = pd.DataFrame()

        return df
