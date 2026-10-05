from itertools import combinations
import numpy as np
import pandas as pd
from scipy import stats

# 1. DADOS COM MAPEAMENTO DE GRUPOS
# Para mudar o número de grupos, basta mudar as strings na coluna "Grupo"!
dados = pd.DataFrame(
    {
        "Segmento": [
            "seg_1",
            "seg_2",
            "seg_3",
            "seg_4",
            "seg_5",
            "seg_6",
            "seg_7",
            "seg_8",
        ],
        "Variavel": [29.1, 28.5, 26.9, 70.2, 31.3, 68.6, 23.1, 42.6],
        "Missing": [0.000, 0.007, 0.000, 2.806, 0.000, 2.268, 0.000, 3.962],
        # Mude as rotulagens aqui livremente!
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

# ==============================================================================
# 2. CÁLCULO ESTATÍSTICO AUTOMÁTICO (Funciona para N grupos)
# ==============================================================================
stats_grupos = dados.groupby("Grupo")["Variavel"].agg(["mean", "std", "count"])

print("=== ESTATÍSTICA DESCRITIVA POR GRUPO ===")
for nome_grupo, linha in stats_grupos.iterrows():
    # Trata o desvio padrão caso o grupo só tenha 1 elemento (N=1)
    std_str = (
        f"±{linha['std']:.2f}%"
        if not np.isnan(linha["std"])
        else "N/A (n=1)"
    )
    print(
        f"• {nome_grupo} (n={int(linha['count'])}): Média = {linha['mean']:.2f}% | Desvio Padrão = {std_str}"
    )

# ==============================================================================
# 3. COMPARAÇÕES PAR A PAR AUTOMÁTICAS (itertools.combinations)
# ==============================================================================
print("\n=== COMPARAÇÕES RELATIVAS (%) ===")
nomes_grupos = stats_grupos.index.tolist()

# Faz a combinação de todos os grupos 2 a 2 automaticamente
for g1, g2 in combinations(nomes_grupos, 2):
    m1 = stats_grupos.loc[g1, "mean"]
    m2 = stats_grupos.loc[g2, "mean"]

    # Calcula a diferença do maior em relação ao menor
    if m1 >= m2:
        dif = ((m1 - m2) / m2) * 100
        print(f"• {g1} é +{dif:.2f}% mais variável que {g2}")
    else:
        dif = ((m2 - m1) / m1) * 100
        print(f"• {g2} é +{dif:.2f}% mais variável que {g1}")

# ==============================================================================
# 4. CORRELAÇÕES GLOBAIS (Não depende do número de grupos)
# ==============================================================================
r_pearson, p_pearson = stats.pearsonr(dados["Missing"], dados["Variavel"])
r_squared = r_pearson**2
rho_spearman, p_spearman = stats.spearmanr(dados["Missing"], dados["Variavel"])

print("\n=== CORRELAÇÕES GLOBAIS (Missing vs Sítios Variáveis) ===")
print(f"Pearson (r):     {r_pearson:.4f} (p-valor: {p_pearson:.4f})")
print(f"R-quadrado (R²):  {r_squared:.4f}")
print(f"Spearman (rho):  {rho_spearman:.4f} (p-valor: {p_spearman:.4f})")