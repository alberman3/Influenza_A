import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

# Configuração de estilo para publicações científicas
sns.set_theme(style="ticks")
plt.rcParams.update({"font.family": "sans-serif", "font.size": 11})

# ==============================================================================
# 1. DADOS (Basta alterar a coluna "Grupo" para criar/remover grupos)
# ==============================================================================
dados = pd.DataFrame(
    {
        "Segmento": [
            "Seg 1",
            "Seg 2",
            "Seg 3",
            "Seg 4",
            "Seg 5",
            "Seg 6",
            "Seg 7",
            "Seg 8",
        ],
        "Variavel": [29.1, 28.5, 26.9, 70.2, 31.3, 68.6, 23.1, 42.6],
        "Missing": [0.000, 0.007, 0.000, 2.806, 0.000, 2.268, 0.000, 3.962],
        "Grupo": [
            "Core Interno",
            "Core Interno",
            "Core Interno",
            "Escape Imune",
            "Core Interno",
            "Escape Imune",
            "Core Interno",
            "Intermediario",  # Se quiser 2 grupos, mude para "Core Interno"
        ],
    }
)

# Descobre automaticamente a quantidade de grupos para nomear os arquivos salvos
n_grupos_qtd = dados["Grupo"].nunique()

# ==============================================================================
# GRÁFICO 1: Comparação dos Grupos (Média ± Desvio Padrão Visível)
# ==============================================================================
plt.figure(figsize=(7, 5))

# Agrupamento dinâmico ordenado da maior para a menor média
df_grupos = (
    dados.groupby("Grupo")["Variavel"]
    .agg(["mean", "std", "count"])
    .sort_values(by="mean", ascending=False)
)

# Preenche desvio padrão com 0 caso o grupo só tenha 1 elemento (ex: n=1)
yerr_values = df_grupos["std"].fillna(0)

# Paleta de cores gerada automaticamente de acordo com o número de grupos
n_grupos = len(df_grupos)
cores = sns.color_palette("Set2", n_colors=n_grupos)

bars = plt.bar(
    df_grupos.index,
    df_grupos["mean"],
    yerr=yerr_values,
    capsize=6,
    color=cores,
    edgecolor="black",
    alpha=0.85,
    width=0.5,
)

# Rótulo de médias + desvio padrão + amostragem (n) dentro de cada barra
for bar, count, std_val in zip(bars, df_grupos["count"], df_grupos["std"]):
    yval = bar.get_height()

    # Formata com o Desvio Padrão se houver mais de 1 elemento (n > 1)
    if count > 1 and pd.notna(std_val):
        texto = f"{yval:.1f}% ± {std_val:.2f}%\n(n={count})"
    else:
        texto = f"{yval:.1f}%\n(n={count})"

    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        yval / 2,
        texto,
        ha="center",
        va="center",
        color="white" if yval > 30 else "black",
        fontweight="bold",
        fontsize=10,
    )

plt.ylabel("Sítios Variáveis Médios (%)", fontsize=12)
plt.title("Variabilidade Nucleotídica por Grupo Funcional", fontsize=13, pad=15)
plt.ylim(0, max(dados["Variavel"]) * 1.25)  # Escala adaptável ao topo do gráfico
sns.despine()

plt.tight_layout()
# Salva dinamicamente indicando o nº de grupos no arquivo (ex: figura_1_3grupos.png)
plt.savefig(f"figura_1_{n_grupos_qtd}grupos_comparacao.png", dpi=300)
plt.close()


# ==============================================================================
# GRÁFICO 2: Regressão Linear + Pontos por Grupo (Dinâmico)
# ==============================================================================
plt.figure(figsize=(8, 5))

# 1. Linha de regressão linear global
sns.regplot(
    data=dados,
    x="Missing",
    y="Variavel",
    scatter=False,
    line_kws={"color": "#333333", "linestyle": "--", "linewidth": 1.5},
)

# 2. Pontos coloridos e estilizados dinamicamente por Grupo
ax = sns.scatterplot(
    data=dados,
    x="Missing",
    y="Variavel",
    hue="Grupo",
    palette="Set2",
    s=120,
    style="Grupo",
)

# 3. Anotação dos segmentos nos pontos
for _, row in dados.iterrows():
    ax.annotate(
        row["Segmento"],
        (row["Missing"], row["Variavel"]),
        xytext=(6, -2),
        textcoords="offset points",
        fontsize=9,
    )

# 4. Cálculo dinâmico das estatísticas globais para a caixa de texto
r_p, p_p = stats.pearsonr(dados["Missing"], dados["Variavel"])
r2 = r_p**2
r_s, p_s = stats.spearmanr(dados["Missing"], dados["Variavel"])

texto_stat = (
    f"$r = {r_p:.4f}$ (p = {p_p:.4f})\n"
    f"$R^2 = {r2:.4f}$\n"
    f"$\\rho = {r_s:.4f}$ (p = {p_s:.4f})"
)

plt.gca().text(
    0.05,
    0.95,
    texto_stat,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.85),
)

plt.xlabel("Missing (%)", fontsize=12)
plt.ylabel("Sítios Variáveis (%)", fontsize=12)
plt.title("Correlação entre Lacunas (Missing) e Variabilidade", fontsize=13, pad=15)
plt.legend(title="Grupo Funcional", loc="lower right")
sns.despine()

plt.tight_layout()
# Salva dinamicamente indicando o nº de grupos no arquivo (ex: figura_2_3grupos.png)
plt.savefig(f"figura_2_{n_grupos_qtd}grupos_regressao.png", dpi=300)
plt.close()

print(f"Gráficos gerados com sucesso para {n_grupos_qtd} grupo(s)!")