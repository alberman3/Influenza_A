import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def extrair_correlacoes(caminho_kernel, caminho_metadata=None):
    df_kernel = pd.read_csv(caminho_kernel)
    
    # 1. Cruzamento de Dados (Merge com Metadados Espaço-Temporais)
    if caminho_metadata and os.path.exists(caminho_metadata):
        df_meta = pd.read_csv(caminho_metadata)
        df = pd.merge(df_kernel, df_meta, on="ID_Sequencia", how="inner")
        print(f"[INFO] Metadados reais carregados. {len(df)} sequências cruzadas com sucesso.")
    else:
        print("[AVISO] Arquivo de metadados não fornecido.")
        print("[INFO] Gerando dados crono-geográficos simulados para testar o pipeline e a matemática...")
        # Simulando metadados caso o CSV real ainda não esteja finalizado
        np.random.seed(42)
        df_kernel['Ano_Coleta'] = np.random.randint(1990, 2026, size=len(df_kernel))
        df_kernel['Local'] = np.random.choice(['Brasil', 'EUA', 'China', 'Europa', 'África'], size=len(df_kernel))
        df = df_kernel

    # 2. Cálculo da Distância Molecular (1 - Similaridade)
    # Quanto maior a distância, mais o vírus evoluiu/mutou em relação à referência
    df['Distancia_Molecular'] = 1 - df['Similaridade_Cosseno']

    # 3. Análise Estatística (Extração de Correlações)
    r_pearson, p_pearson = stats.pearsonr(df['Ano_Coleta'], df['Distancia_Molecular'])
    rho_spearman, p_spearman = stats.spearmanr(df['Ano_Coleta'], df['Distancia_Molecular'])

    print("\n=== RESULTADOS DA CORRELAÇÃO CRONO-EVOLUTIVA ===")
    print(f"Correlação de Pearson (r): {r_pearson:.4f} (p-valor: {p_pearson:.4f})")
    print(f"Correlação de Spearman (rho): {rho_spearman:.4f} (p-valor: {p_spearman:.4f})")

    if p_pearson < 0.05:
        print("-> Conclusão: Existe uma correlação estatisticamente significativa entre o tempo e a evolução molecular!")
    else:
        print("-> Conclusão: A correlação temporal não foi estatisticamente significativa para este segmento.")

    # 4. Geração de Gráficos e Componentes Visuais
    nome_base = os.path.splitext(os.path.basename(caminho_kernel))[0]
    pasta_saida = os.path.dirname(caminho_kernel)

    # Plot 1: Regressão Linear (Tempo vs Distância Genética)
    plt.figure(figsize=(10, 6))
    sns.regplot(x='Ano_Coleta', y='Distancia_Molecular', data=df, 
                scatter_kws={'alpha':0.7, 'color':'#2980b9', 's': 50}, 
                line_kws={'color':'#e74c3c', 'linewidth': 2})
    plt.title('Rastreamento Temporal: Distância Molecular (Uso de Códons) ao Longo dos Anos')
    plt.xlabel('Ano de Coleta')
    plt.ylabel('Distância Molecular (1 - Similaridade CBUC)')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    caminho_plot_tempo = os.path.join(pasta_saida, f"{nome_base}_grafico_tempo.png")
    plt.savefig(caminho_plot_tempo, dpi=300, bbox_inches='tight')
    plt.close()

    # Plot 2: Boxplot por Geografia (Assinaturas Regionais)
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Local', y='Distancia_Molecular', data=df, palette='Set2')
    plt.title('Distribuição da Evolução Molecular por Região Geográfica')
    plt.xlabel('Região de Coleta')
    plt.ylabel('Distância Molecular')
    
    caminho_plot_geo = os.path.join(pasta_saida, f"{nome_base}_grafico_geo.png")
    plt.savefig(caminho_plot_geo, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"\n[SUCESSO] Componentes visuais para rastreamento exportados na pasta do segmento!")
    print(f"-> {caminho_plot_tempo}")
    print(f"-> {caminho_plot_geo}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python rastreamento_crono_geo.py <arquivo_kernel.csv> [arquivo_metadata.csv opcional]")
        sys.exit(1)
        
    arq_kernel = sys.argv[1]
    arq_meta = sys.argv[2] if len(sys.argv) > 2 else None
    
    extrair_correlacoes(arq_kernel, arq_meta)