from pathlib import Path

import altair as alt
import pandas as pd
from shiny import module, render, ui
from shinywidgets import output_widget, render_altair

from .utils import filter_and_rank

dados_vestibular = pd.read_parquet(
    Path(__file__).parent.parent / "data/densidades_vestibular_ufrgs.parquet"
)
dados_vestibular["ano"] = dados_vestibular["ano"].astype(str)
dados_vestibular["ano_datetime"] = pd.to_datetime(dados_vestibular["ano"] + "-01-01")
dados_vestibular = dados_vestibular[dados_vestibular["n_vagas"] > 0]
dados_vestibular["curso"] = dados_vestibular["curso"].str.replace(
    " - Bacharelado", "", regex=False
)

anos_base = dados_vestibular["ano"].drop_duplicates().to_list()
anos_base.sort()

modalidades_ingresso = dados_vestibular["categoria"].drop_duplicates().to_list()
modalidades_ingresso.sort()


@module.ui
def comparacao_ui():
    comparacao_ui = ui.page_fluid(
        ui.row(
            ui.h1(
                "Comparação densidades para ingresso pelo Vestibular UFRGS",
                style="text-align:center",
            )
        ),
        ui.hr(),
        ui.row(
            ui.column(
                3,
                ui.input_checkbox_group(
                    "anos_comparacao",
                    "Anos para comparação:",
                    [{year: ui.span(year) for year in anos_base}][0],
                    selected=anos_base,
                ),
                ui.input_radio_buttons(
                    "ano_base",
                    "Ano base de comparação:",
                    [{year: ui.span(year) for year in anos_base}][0],
                    selected=anos_base[-1],
                ),
                ui.input_select(
                    "modalidade_ingresso",
                    "Modalidade de ingresso",
                    [{mod: ui.span(mod) for mod in modalidades_ingresso}][0],
                    selected="Total",
                ),
                ui.h6("Download Button pending", style="color: #e6e6e6e"),
            ),
            ui.column(
                9,
                # ui.output_table("comp_bump_chart")
                output_widget("comp_bump_chart"),
            ),
        ),
    )
    return comparacao_ui


@module.server
def comparacao_server(input, output, session):
    @output
    @render_altair
    def comp_bump_chart():

        if input.anos_comparacao().__len__() > 0:
            vest_filtro = dados_vestibular[
                dados_vestibular["categoria"] == input.modalidade_ingresso()
            ]

            cursos_base = filter_and_rank(vest_filtro, input.ano_base())["curso"]

            vest_filtro = vest_filtro[vest_filtro["curso"].isin(cursos_base)]

            df = pd.concat(
                [
                    filter_and_rank(vest_filtro, selected_year)
                    for selected_year in input.anos_comparacao()
                ],
                axis=0,
            )

            return (
                alt.Chart(df)
                .mark_line(point=True)
                .encode(
                    x=alt.X("ano_datetime").timeUnit("year").title("Ano"),
                    y="rank:O",
                    color=alt.Color("curso"),
                    tooltip=["curso", "densidade", "rank", "ano"],
                )
                .transform_window(
                    rank="rank()",
                    sort=[alt.SortField("densidade", order="descending")],
                    groupby=["ano"],
                )
                .properties(
                    title={
                        "text": "Comparação das densidades para ingresso pelo Vestibular UFRGS",
                        "subtitle": [
                            f"Utilizando {input.ano_base()} como ano-base",
                            f"Modalidade de ingresso: {input.modalidade_ingresso()}",
                        ],
                    }
                )
                .interactive()
            )
