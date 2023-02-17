# Importa as bibliotecas
import os
import sqlite3
import shutil
import pandas as pd
import xml.etree.ElementTree as et

# Cria um dataframe vazio
df = pd.DataFrame(
    columns=["natOp", "dhEmi"])

# Cria um dicionário vazio
dic = {}

# Cria um contador
cont = -1

# Localiza a pasta que contém os arquivos
diretorio = "./arquivos"

# Itera a pasta
for arquivo in os.listdir(diretorio):

    # Verifica se a extensão do arquivo é .xml
    if arquivo.endswith(".xml"):
        cont += 1

        # Determina o caminho de cada arquivo
        caminho_arquivo = os.path.join(diretorio, arquivo)
       
        arvore = et.parse(caminho_arquivo)

        raiz = arvore.getroot()

        for filhas in raiz:
            for netas in filhas:
                for bisnetas in netas:
                    
                    for trinetas in bisnetas:
                        if 'natOp' in trinetas.tag:
                            dic['natOp'] = trinetas.text
                        
                        if 'dhEmi' in trinetas.tag:
                            dic['dhEmi'] = trinetas.text
                        

                    if dic != {}:
                        df.loc[len(df)] = dic
                    dic = {}

print(df)
print()
print(f'O número de arquivos xml são: {cont}!')
print()


# cria a conexão com o banco de dados
conn = sqlite3.connect('banco.db')

try:
    # salva o dataframe na tabela
    df.to_sql('registros', conn, index=False)

except:
    # Define o caminho para o arquivo de origem e de destino
    origem = 'banco.db'
    destino = 'backup-banco.db'

    # Faz a cópia do arquivo de origem para o destino
    shutil.copy(origem, destino)

    # carrega os dados da tabela existente em um dataframe
    banco = pd.read_sql_query("SELECT * FROM registros", conn)

    # concatena os dataframes
    df_concatenado = pd.concat([df, banco], ignore_index=True)

    # salva o dataframe concatenado na tabela, substituindo a tabela existente
    df_concatenado.to_sql('registros', conn, if_exists='replace', index=False)

# fecha a conexão com o banco de dados
conn.close()
