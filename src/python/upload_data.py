import os
import pandas as pd
import sqlalchemy

user = 'root' #Login
psw = 'thg2g3gs' #Senha
host = '127.0.0.1' #ip/host/dns
port = '3306' # Port

str_connection = 'mysql+pymysql://{user}:{psw}@{host}:{port}'
#str_connection = 'sqlite:///{path}'

# Criando os caminhos globais do projeto.
BASE_DIR = os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data')

#Testando se os caminhos estão corretos.
# print("Meu diretório do projeto é", BASE_DIR)
# print("Meu diretório dos dados é", DATA_DIR)

#Mostrando somente os arquivos com extensão .csv.
#Forma um -> List comprehension
# files_names = os.listdir( DATA_DIR )
# correct_files = []
# for i in files_names:
#     if i.endswith(".csv"):
#         correct_files.append(i)

# Forma dois -> List comprehension
files_names = [ i for i in os.listdir( DATA_DIR ) if i.endswith('.csv') ]

# Abrindo conexão com o banco...
str_connection = str_connection.format( user=user, psw=psw, host=host, port=port )
connection = sqlalchemy.create_engine( str_connection )

# Teste
# def data_quality(x):
#     if type(x) == str:
#         return x.replace("\n", "").replace("\r", '')
#     else:
#         return x

# Para cada arquivo é realizado uma inserção no banco
for i in files_names:
    df_tmp = pd.read_csv( os.path.join( DATA_DIR, i ) )
    table_name = "tb_" + i.strip('.csv').replace("olist_", "").replace("_dataset", "")
    df_tmp.to_sql( table_name, 
                    connection, 
                    schema='analytics',
                    if_exists='replace',
                    index=False )
    
    
