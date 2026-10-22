import sys
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import os

def calcular_similaridade_cosseno(caminho_csv, id_referencia):
    # 1. Carregar os vetores gerados na Atividade anterior
    df = pd.read_csv(caminho_csv)
    
    # Isolar apenas as colunas numéricas do vetor (RSCU)
    colunas_rscu = [col for col in df.columns if col.startswith('RSCU_')]
    
    # 2. Verificar se a sequência de referência escolhida existe no ficheiro
    if id_referencia not in df['ID_Sequencia'].values:
        print(f"[ERRO] A sequência de referência '{id_referencia}' não foi encontrada no ficheiro.")
        print("Opções disponíveis:", df['ID_Sequencia'].tolist()[:5], "...")
        return
        
    # Extrair o vetor matemático da referência
    vetor_ref = df[df['ID_Sequencia'] == id_referencia][colunas_rscu].values[0]
    
    similaridades = []
    
    # 3. Aplicar o Algoritmo de Similaridade de Cosseno (Atividade 1)
    for index, row in df.iterrows():
        vetor_alvo = row[colunas_rscu].values
        
        # Scipy calcula a "distância", a "similaridade" é 1 - distância
        # Proteção matemática para vetores vazios
        if np.all(vetor_alvo == 0) or np.all(vetor_ref == 0):
            sim = 0.0
        else:
            sim = 1 - cosine(vetor_ref, vetor_alvo)
            
        similaridades.append(round(sim, 4))
        
    # Adicionar os resultados ao DataFrame
    df['Similaridade_Cosseno'] = similaridades
    
    # 4. Ordenar para que os vírus mais similares à referência fiquem no topo
    colunas_finais = ['ID_Sequencia', 'Similaridade_Cosseno'] + colunas_rscu
    df_ordenado = df[colunas_finais].sort_values(by='Similaridade_Cosseno', ascending=False)
    
    # Gerar nome do ficheiro de saída
    nome_base = os.path.splitext(os.path.basename(caminho_csv))[0]
    pasta_saida = os.path.dirname(caminho_csv) if os.path.dirname(caminho_csv) else "."
    
    # Substituir barras por underline para evitar erros no nome do ficheiro Linux
    ref_limpa = id_referencia.replace('/', '_')
    ficheiro_saida = os.path.join(pasta_saida, f"{nome_base}_kernel_{ref_limpa}.csv")
    
    df_ordenado.to_csv(ficheiro_saida, index=False)
    print(f"\n[SUCESSO] Kernel Matemático executado usando '{id_referencia}' como referência!")
    print(f"[INFO] Ficheiro gerado com o Ranking de Similaridade: {ficheiro_saida}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python kernel_cosseno.py <arquivo_vetores_RSCU.csv> <ID_da_Referencia>")
        sys.exit(1)
        
    caminho_vetores = sys.argv[1]
    referencia = sys.argv[2]
    
    calcular_similaridade_cosseno(caminho_vetores, referencia)