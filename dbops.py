import sqlite3

#estabelecer conexão com o banco de dados
conn = sqlite3.connect('database.db', check_same_thread=False)
#criar cursor para executar comandos SQL
cursor = conn.cursor()

# comando sql para excluir a tabela se ela existir
sql = 'DROP TABLE IF EXISTS feed_item;'


# executar o comando sql
cursor.execute(sql)

# confirma a operação
conn.commit()

#fecha a conexão
cursor.close()
conn.close()


print ("Tabela excluída com sucesso.")