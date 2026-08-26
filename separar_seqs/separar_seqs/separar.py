from Bio import SeqIO
import re
from collections import defaultdict

entrada = "Refseqs.fasta"
segmentos = defaultdict(list)
nao_identificados = []

def identificar_segmento(header):
    header = header.lower()
    
    # 1️⃣ tenta pegar "segment X"
    match = re.search(r"segment (\d+)", header)
    if match:
        return match.group(1)
    
    # 2️⃣ fallback por nome do gene
    if "pb2" in header:
        return "1"
    elif "pb1" in header:
        return "2"
    elif re.search(r"\bpa\b", header):
        return "3"
    elif "hemagglutinin" in header or "ha" in header:
        return "4"
    elif "nucleoprotein" in header or "np" in header:
        return "5"
    elif "neuraminidase" in header or "na" in header:
        return "6"
    elif "matrix" in header or "m1" in header or "m2" in header:
        return "7"
    elif "nonstructural" in header or "ns1" in header or "ns2" in header:
        return "8"
    
    return None  # não identificado

# leitura
for record in SeqIO.parse(entrada, "fasta"):
    header = record.description
    seg = identificar_segmento(header)
    
    if seg:
        segmentos[seg].append(record)
    else:
        print(f"⚠️ Não identificado: {header}")
        nao_identificados.append(record)

# salvar
for seg, seqs in segmentos.items():
    nome_arquivo = f"segmento_{seg}.fasta"
    SeqIO.write(seqs, nome_arquivo, "fasta")
    print(f"✔ {nome_arquivo} -> {len(seqs)} sequências")