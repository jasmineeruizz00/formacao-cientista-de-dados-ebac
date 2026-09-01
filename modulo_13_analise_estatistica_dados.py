import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns

df= pd.read_csv('MODULO7_PROJETOFINAL_BASE_SUPERMERCADO - MODULO7_PROJETOFINAL_BASE_SUPERMERCADO (1).csv.csv')
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
print(df.head())

# 1 - Traga a média e a mediana dos preços - coluna Preco_Normal - por categoria de produto.
# Identifique as categorias que parecem ter um valor de média abaixo ou acima da mediana.
#media
print(df.groupby('Categoria')['Preco_Normal'].mean().reset_index().sort_values(by='Preco_Normal', ascending=False))
#mediana
print(df.groupby('Categoria')['Preco_Normal'].median().reset_index().sort_values(by='Preco_Normal', ascending=False))

# Tabela com média e mediana de preço normal por categoria
resumo = (df.groupby("Categoria", as_index=False)["Preco_Normal"].agg(media="mean", mediana="median"))

# Removi a parte do código que gerava um gráfico, pois o próximo gráfico já fazia a mesma coisa, só que melhor.
# Preferi manter apenas um para facilitar a manutenção.

# resumo["diferenca"] = resumo["media"] - resumo["mediana"]
# grafico_dados = resumo.melt( id_vars="Categoria", value_vars=["media", "mediana"], var_name="Medida",
#                              value_name="Preco" )
#
# fig = px.bar( grafico_dados, x="Categoria", y="Preco", color="Medida", barmode="group", title="Média e mediana do Preço"
#                                                                                               " Normal por categoria",
#     labels={ "Categoria": "Categoria",  "Preco": "Preço normal", "Medida": "Medida estatística" },
#     color_discrete_map={   "media": "#636EFA", "mediana": "#EF553B" } )
#
# fig.update_layout( xaxis_tickangle=-45, template="plotly_white" )
#
# fig.show()



#2 - Traga o desvio padrão por categoria de produto.
#Qual o comportamento da média e mediana nas categorias com maior desvio?

desvio_padrao_por_categoria = df.groupby('Categoria')['Preco_Normal'].std().reset_index()
print(desvio_padrao_por_categoria)

resumo = ( df.groupby("Categoria", as_index=False)["Preco_Normal"] .agg( media="mean", mediana="median",
                                                                         desvio="std" ) )

# Ordena pelo maior desvio padrão
resumo = resumo.sort_values("desvio", ascending=False)

print(resumo)
#Nas categorias com maior desvio padrão de Preco_Normal, nota-se que a diferença entre média e mediana é mais
# pronunciada, o que sugere maior assimetria na distribuição dos preços.

# Cria a tabela com as três medidas por categoria
resumo = (
    df.groupby("Categoria", as_index=False)["Preco_Normal"].agg(media="mean",mediana="median",desvio="std")
    .sort_values("desvio", ascending=False))

fig = go.Figure()
# Barra 1: média
fig.add_trace(go.Bar(x=resumo["Categoria"],y=resumo["media"],name="Média",marker_color="#636EFA" ))

# Barra 2: mediana
fig.add_trace( go.Bar(x=resumo["Categoria"],y=resumo["mediana"],name="Mediana", marker_color="#EF553B" ))

# Linha: desvio padrão
fig.add_trace(go.Scatter( x=resumo["Categoria"],y=resumo["desvio"],name="Desvio padrão",mode="lines+markers",
        line=dict(color="#00CC96", width=3),marker=dict(size=8), yaxis="y2"))

fig.update_layout(title="Média, mediana e desvio padrão do preço normal por categoria",xaxis=dict(
    title="Categoria",tickangle=-45),yaxis=dict( title="Preço normal" ),
    yaxis2=dict( title="Desvio padrão",overlaying="y",side="right" ),
    barmode="group",
    template="plotly_white",
    legend_title_text="Medidas")

fig.show()
#resposta pergunta 1
#O gráfico evidencia diferenças entre média e mediana do preço normal nas diferentes categorias, sugerindo distribuições
# assimétricas em alguns grupos.
#resposta pergunta 2
#As categorias com maior desvio padrão de Preco_Normal apresentam diferença mais acentuada entre média e mediana.
# Em geral, nessas categorias a média é maior que a mediana, o que indica que alguns produtos com preços bem acima da
# maioria elevam a média, enquanto a mediana permanece mais próxima dos valores típicos de preço. Isso sugere
# distribuições assimétricas à direita nos grupos com maior variabilidade de preços.

## 3 - Plot um boxplot da distribuição do Preco_Normal para a categoria que você identificou que tem o maior desvio
# padrão. Como é a distribuição desses dados segundo o boxplot? Você identifica muitos outliers?

categoria_maior_desvio = "lacteos"

df_cat = df.loc[df["Categoria"] == categoria_maior_desvio, "Preco_Normal"]

plt.figure(figsize=(8, 6))
sns.boxplot(y=df_cat)

plt.title(f"Distribuição de Preco_Normal na categoria '{categoria_maior_desvio}'")
plt.ylabel("Preço normal")
plt.tight_layout()
plt.show()
#A categoria lacteos apresenta uma distribuição assimétrica à direita. A maior parte dos preços está concentrada em
# valores baixos, mas há muitos outliers acima do bigode superior, alguns próximos de 20.000. Esses valores extremos
# aumentam significativamente a dispersão e ajudam a explicar o alto desvio padrão da categoria.

# 4 - Plote um gráfico de barras onde temos a média de descontos por categoria.
# Média de desconto por categoria
media_desconto = (df.groupby("Categoria", as_index=False)["Desconto"].mean()
                  .sort_values("Desconto", ascending=False))

print(media_desconto)

fig = px.bar(media_desconto,x="Categoria",y="Desconto",title="Média de descontos por categoria",
             labels={"Categoria": "Categoria","Desconto": "Média do desconto"},
    color="Desconto",color_continuous_scale="Blues",text_auto=".2f")

fig.update_layout(xaxis_tickangle=-45,template="plotly_white",coloraxis_showscale=False)

fig.show()

# 5 - Plote um gráfico de mapa interativo agrupando os dados por categoria, marca e trazendo a média de desconto.

# Média de desconto por categoria e marca
media_desconto_marca = (df.groupby(["Categoria", "Marca"], as_index=False)["Desconto"]
                        .mean().sort_values("Desconto", ascending=False))


fig = px.treemap(media_desconto_marca,path=["Categoria", "Marca"],values="Desconto",color="Desconto",
                 color_continuous_scale="Blues",title="Média de desconto por categoria e marca",
                 labels={"Categoria": "Categoria","Marca": "Marca","Desconto": "Média de desconto"})

fig.update_traces( textinfo="label+value+percent parent")

fig.update_layout(template="plotly_white")

fig.show()
#Por fim, peço desculpas pelo tamanho do código e pela quantidade de comentários.
# Preferi deixar o projeto bem explicado e documentado,
# para facilitar meu entendimento no futuro e também tornar a correção mais clara.
