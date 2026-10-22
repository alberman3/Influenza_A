import sys
import os
import pandas as pd
from Bio import SeqIO
from collections import Counter

# Tabela do Código Genético Padrão: Mapeamento de Aminoácidos para os seus respetivos códons
codigo_genetico = {
    'F': ['TTT', 'TTC'], 'L': ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'],
    'I': ['ATT', 'ATC', 'ATA'], 'M': ['ATG'], 'V': ['GTT', 'GTC', 'GTA', 'GTG'],
    'S': ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'], 'P': ['CCT', 'CCC', 'CCA', 'CCG'],
    'T': ['ACT', 'ACC', 'ACA', 'ACG'], 'A': ['GCT', 'GCC', 'GCA', 'GCG'],
    'Y': ['TAT', 'TAC'], 'H': ['CAT', 'CAC'], 'Q': ['CAA', 'CAG'],
    'N': ['AAT', 'AAC'], 'K': ['AAA', 'AAG'], 'D': ['GAT', 'GAC'],
    'E': ['GAA', 'GAG'], 'C': ['TGT', 'TGC'], 'W': ['TGG'],
    'R': ['CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'], 'G': ['GGT', 'GGC', 'GGA', 'GGG'],
    '*': ['TAA', 'TAG', 'TGA'] # Stop codons (geralmente ignorados no cálculo final do RSCU)
}

# Dicionário inverso (Códon -> Aminoácido) para facilitar a tradução
codon_para_aa = {codon: aa for aa, codons in codigo_genetico.items() for codon in codons}

def extrair_vetor_codoes(seq_cds):
    """
    Recebe uma sequência de nucleotídeos (CDS validada) e devolve um dicionário
    com a contagem absoluta de cada códon e o valor RSCU (Uso Relativo de Códons Sinônimos).
    """
    seq_str = str(seq_cds).upper()
    
    # 1. Separar a sequência em trincas (códons)
    codoes_seq = [seq_str[i:i+3] for i in range(0, len(seq_str), 3) if len(seq_str[i:i+3]) == 3]
    
    # 2. Contagem absoluta de cada códon na sequência
    contagem_codoes = Counter(codoes_seq)
    
    # 3. Contagem absoluta de cada aminoácido (Tradução in silico)
    contagem_aa = Counter([codon_para_aa.get(c, 'X') for c in codoes_seq])
    
    vetor_features = {}
    
    # 4. Cálculo do RSCU (Frequência observada / Frequência esperada se o uso fosse uniforme)
    for aa, codons in codigo_genetico.items():
        if aa == '*': 
            continue # Omitimos os stop codons do vetor de features evolutivas
            
        n_sinonimos = len(codons)
        total_deste_aa = contagem_aa.get(aa, 0)
        
        for codon in codons:
            contagem_abs = contagem_codoes.get(codon, 0)
            
            if total_deste_aa > 0:
                rscu = contagem_abs / (total_deste_aa / n_sinonimos)
            else:
                rscu = 0.0
                
            vetor_features[f"Count_{codon}"] = contagem_abs
            vetor_features[f"RSCU_{codon}"] = round(rscu, 4)
            
    return vetor_features

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python vetorizacao_codoes.py <arquivo_curado.fasta>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    
    if not os.path.exists(arquivo_entrada):
        print(f"[ERRO] O ficheiro {arquivo_entrada} não foi encontrado.")
        sys.exit(1)

    resultados_lista = []
    
    # Carrega as sequências que já passaram pelo filtro do alinhamento.py
    for record in SeqIO.parse(arquivo_entrada, "fasta"):
        vetor_amostra = {"ID_Sequencia": record.id}
        
        # Calcula as métricas e adiciona ao vetor da amostra
        metricas_codoes = extrair_vetor_codoes(record.seq)
        vetor_amostra.update(metricas_codoes)
        
        resultados_lista.append(vetor_amostra)
        
    # Converte tudo num DataFrame do Pandas para visualização e exportação
    df_vetores = pd.DataFrame(resultados_lista)
    
    # Gera o nome de saída dinamicamente
    nome_base = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    pasta_saida = os.path.dirname(arquivo_entrada) if os.path.dirname(arquivo_entrada) else "."
    caminho_csv = os.path.join(pasta_saida, f"{nome_base}_vetores_RSCU.csv")
    
    df_vetores.to_csv(caminho_csv, index=False)
    
    print(f"[SUCESSO] Tradução e vetorização concluídas! Foram analisadas {len(resultados_lista)} sequências.")
    print(f"[INFO] Tabela de métricas RSCU e contagens absolutas guardada em: {caminho_csv}")