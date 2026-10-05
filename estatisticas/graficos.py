import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# ==========================================
# Dados do AMAS (Incluindo H7N9 no Segmento 8)
# ==========================================

dados = pd.DataFrame({

    "Segmento": [
        "segmento_1",
        "segmento_2",
        "segmento_3",
        "segmento_4",
        "segmento_5",
        "segmento_6",
        "segmento_7",
        "segmento_8"
    ],

    "Variavel": [
        29.1,  # 0.291 * 100
        28.5,  # 0.285 * 100
        26.9,  # 0.269 * 100
        70.2,  # 0.702 * 100
        31.3,  # 0.313 * 100
        68.6,  # 0.686 * 100
        23.1,  # 0.231 * 100
        42.6   # 0.426 * 100 (Com H7N9)
    ],

    "Informativo": [
        16.8,  # 0.168 * 100
        14.2,  # 0.142 * 100
        16.0,  # 0.160 * 100
        41.6,  # 0.416 * 100
        18.6,  # 0.186 * 100
        46.9,  # 0.469 * 100
        13.2,  # 0.132 * 100
        18.6   # 0.186 * 100 (Com H7N9)
    ],

    "Missing": [
        0.000,
        0.007,
        0.000,
        2.806,
        0.000,
        2.268,
        0.000,
        3.962  # 3.962% (Gap terminal do H7N9)
    ],

    "GC": [
        44.0,  # 0.440 * 100
        43.0,  # 0.430 * 100
        43.2,  # 0.432 * 100
        41.8,  # 0.418 * 100
        46.8,  # 0.468 * 100
        43.1,  # 0.431 * 100
        49.2,  # 0.492 * 100
        45.0   # 0.450 * 100
    ]
})


# =========================
# Gráfico 1: Ranking conservação
# =========================

df = dados.sort_values("Variavel")

plt.figure(figsize=(8, 5))

sns.barplot(
    data=df,
    x="Variavel",
    y="Segmento",
    hue="Segmento",
    palette="viridis",
    legend=False
)

plt.xlabel("Sítios variáveis (%)")
plt.ylabel("")
plt.title("Variabilidade nucleotídica dos segmentos")

plt.tight_layout()
plt.savefig("ranking_conservacao.png", dpi=300)
plt.close()


# =========================
# Gráfico 2: Conservação x Missing
# =========================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=dados,
    x="Missing",
    y="Variavel",
    s=150
)

# Rótulo com ajuste para não cortar no limite do gráfico
for i, row in dados.iterrows():
    plt.text(
        row["Missing"] + 0.08,
        row["Variavel"],
        row["Segmento"],
        va='center'
    )

plt.xlim(-0.2, 5.0)  # Margem expandida para caber o rótulo do segmento 8
plt.xlabel("Missing (%)")
plt.ylabel("Sítios variáveis (%)")
plt.title("Conservação versus qualidade do alinhamento")

plt.tight_layout()
plt.savefig("conservacao_missing.png", dpi=300)
plt.close()


# =========================
# Gráfico 3: Heatmap
# =========================

heat = dados.set_index("Segmento")[
    [
        "Variavel",
        "Informativo",
        "Missing",
        "GC"
    ]
]

plt.figure(figsize=(7, 5))

sns.heatmap(
    heat,
    annot=True,
    cmap="RdYlGn_r",
    fmt=".1f"
)

plt.title("Características dos segmentos")

plt.tight_layout()
plt.savefig("heatmap_segmentos.png", dpi=300)
plt.close()


print("Gráficos gerados com sucesso com a inclusão do H7N9!")