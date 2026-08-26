import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import matplotlib.patches as mpatches
from geopy.geocoders import Nominatim
import time
import pycountry_convert as pc
import json
import pycountry
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from googletrans import Translator
here = os.path.abspath(os.path.dirname(__file__))

# Contador para registros processados com sucesso
records_processed = 0
# Contador para registros que falharam ao serem processados
records_failed = 0
data = []

# Adicione esta linha no início do seu código
print("Iniciando o processamento dos arquivos...")

download_path = os.path.join(here, 'C:/Iniciacao_Cientifica/Preprocess/NA')
comcodons = True

# Imprime o caminho que está sendo verificado
print(f"Verificando a pasta: {download_path}")

identifier_pattern = re.compile(
    r"(?P<ID>[^\s]+)\s(?P<Type>[A-Z])\/(?P<Species>[^/]+(?:\s[^/]+)*)\/(?P<Location>[^\/]+)\/(?P<Data>[^/]+)\/(?P<Sequence_type>[^\s]+)\s"
)

# Verifica se a pasta existe antes de tentar ler os arquivos
if not os.path.exists(download_path):
    print(f"ERRO: O caminho '{download_path}' não foi encontrado.")
else:
    for file_name in os.listdir(download_path):
        if file_name.endswith(".fa"):
            file_path = os.path.join(download_path, file_name)

            class_match = re.search(r"\((.*?)\)", file_name)
            class_name = class_match.group(1) if class_match else "Unknown"

            segment_match = re.search(r"_(.*?)_", file_name)
            segment = segment_match.group(1) if segment_match else "Unknown"

            Subtype_match = re.search(r"^(H\d+N\d+)", file_name)
            Subtype = Subtype_match.group(1) if Subtype_match else "Unknown"

            with open(file_path, "r") as fasta_file:
                identifier = ""
                sequence = ""

                for line in fasta_file:
                    line = line.strip()
                    if line.startswith(">"):
                        if identifier and sequence:
                            data.append([identifier, sequence, class_name, segment, Subtype])
                        identifier = line[1:]
                        sequence = ""
                    else:
                        sequence += line

                if identifier and sequence:
                    data.append([identifier, sequence, class_name, segment, Subtype])


data_cleaned = []
for entry in data:
    match = identifier_pattern.match(entry[0])
    if match:
        ID = match.group("ID")
        Type = match.group("Type")
        Species = match.group("Species")
        Location = match.group("Location")
        Data = match.group("Data")
        Sequence_type = match.group("Sequence_type")

        data_cleaned.append([
            ID, Type, Species, Location, Data, Sequence_type,
            entry[1], entry[2], entry[3], entry[4]
        ])
        records_processed += 1
    else:
        # Se o padrão não for encontrado, imprima a linha que falhou
        print(f"AVISO: Registro ignorado por formato inválido: {entry[0]}")
        records_failed += 1


df = pd.DataFrame(data_cleaned, columns=[
    "ID", "Type", "Species", "Location", "Sequence_type", "Data",
    "Sequence", "Class", "Segment", "Subtype"
])

# Adicione estas linhas no final para um resumo
print("\n--- Resumo do Processamento ---")
print(f"Registros lidos dos arquivos: {len(data)}")
print(f"Registros processados e adicionados ao DataFrame: {records_processed}")
print(f"Registros ignorados devido a formato inválido: {records_failed}")
print("\nProcessamento concluído com sucesso!")



# ... (todo o seu código de processamento)

# Salva os dados processados em um novo arquivo FASTA
output_fasta_file = 'dados_processados.fa'
print(f"\nSalvando dados em {output_fasta_file}...")

with open(output_fasta_file, 'w') as fasta_file:
    # Itera sobre cada linha (cada registro) do DataFrame
    for _, row in df.iterrows():
        # Constrói a linha do cabeçalho FASTA
        header = f">{row['ID']} {row['Type']}/{row['Species']}/{row['Location']}/{row['Data']}/{row['Sequence_type']}"
        sequence = row['Sequence']
        
        # Escreve o cabeçalho no novo arquivo
        fasta_file.write(header + '\n')
        
        # --- A NOVA PARTE DO CÓDIGO ---
        # Divide a sequência em pedaços de 60 caracteres
        for i in range(0, len(sequence), 60):
            fasta_file.write(sequence[i:i+60] + '\n')
        # -----------------------------
        
print(f"Dados salvos com sucesso em {output_fasta_file}")