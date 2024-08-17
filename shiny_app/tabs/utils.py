def filter_and_rank(df, ano):
    df_return = df[df["ano"] == ano].sort_values("densidade", ascending=False)[0:10]
    df_return["rank"] = df_return["densidade"].rank(ascending=False)
    df_return["densidade"] = df_return["densidade"].round(2)
    return df_return
