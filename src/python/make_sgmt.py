import os
from sqlite3 import connect
import sqlalchemy
import argparse
import pandas as pd
import datetime


user = 'root' #Login
psw = 'thg2g3gs' #Senha
host = 'localhost' #ip/host/dns
port = '3306/olist' # Port

# Os endereços de nosso projeto e sub pastas
BASE_DIR = os.path.dirname( os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) ) )
DATA_DIR = os.path.join( BASE_DIR, 'data')
SQL_DIR = os.path.join( BASE_DIR, 'src', 'sql' )

parser = argparse.ArgumentParser()
parser.add_argument('--date_end', '-e', help='Data de fim da extração', default='2018-06-01')
args = parser.parse_args()

date_end = args.date_end

ano = int(date_end.split("-")[0]) - 1
mes = int(date_end.split("-")[1])
date_init = f"{ano}-{mes}-01"

# Verificando o diretorio sql
# print(SQL_DIR)

# Importando a query sql
with open( os.path.join(SQL_DIR, 'segmentos.sql' ) ) as query_file:
    query = query_file.read()

query = query.format( date_init = date_init, 
                      date_end = date_end  )

# Abrindo conexão com o banco...
str_connection = 'mysql+pymysql://{user}:{psw}@{host}:{port}'
str_connection = str_connection.format( user=user, psw=psw, host=host, port=port )
connection = sqlalchemy.create_engine( str_connection )

# Teste query
# df = pd.read_sql_query( query, connection )
# print(df)

create_query = f'''
CREATE TABLE tb_seller_sgmt AS
{query}
;'''

insert_query = f'''
DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
INSERT INTO tb_seller_sgmt
{query}
;'''

try:
    connection.execute( create_query )
except:
    for q in insert_query.split(";")[:-1]:
        connection.execute( q )
