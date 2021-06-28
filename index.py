#Blibioteca da API do Lichess
import berserk 
#Blibioteca pymsql
import pymysql
#Conectando a base de dados.
link = pymysql.connect(db="lichesss",user="root",passwd="")
#Executando o cursor do mysql
cursor = link.cursor()
#Depositando o token.
token='WONnyuEKIcIQDSAD'
#Autenticação do token de segurança.
session = berserk.TokenSession(token)
client = berserk.Client(session=session)
#Pegando detalhes da conta
client.account.get()
#TOP 10 JOGADORES BULLET
top_bullet=client.users.get_leaderboard('bullet', count=11)
#TOP 10 JOGADORES BLITZ
top_blitz=client.users.get_leaderboard('blitz', count=11)
#TOP 10 JOGADORES RAPID
top_rapid=client.users.get_leaderboard('rapid', count=11)
#Inserindo os dados na base dados 
for r in top_bullet:
    #Este try não vai inserir o title caso ele não exista
    try:
       a="INSERT INTO top_bullet (id, username, title) VALUES (' " + r['id'] + " ', ' " + r['username'] + " ', ' " + r['title'] + " ') "
       cursor.execute(a)
       link.commit()
    except KeyError:
       a="INSERT INTO top_bullet (id, username) VALUES (' " + r['id'] + " ', ' " + r['username'] + " ') "
       cursor.execute(a)
       link.commit()
for m in top_rapid:
    try:
        c="INSERT INTO top_rapid (id, username, title) VALUES (' " + m['id'] + " ', ' " + m['username'] + " ', ' " + m['title'] + " ') "
        cursor.execute(c)
        link.commit()
    except KeyError:
        c="INSERT INTO top_rapid (id, username) VALUES (' " + m['id'] + " ', ' " + m['username'] + " ') "
        cursor.execute(c)
        link.commit() 
for l in top_blitz:
    try:
        b="INSERT INTO top_blitz (id, username, title) VALUES (' " + l['id'] + " ', ' " + l['username'] + " ', ' " + l['title'] + " ') "
        cursor.execute(b)
        link.commit()
    except KeyError:
        b="INSERT INTO top_blitz (id, username) VALUES (' " + l['id'] + " ', ' " + l['username'] + " ') "
        cursor.execute(b)
        link.commit()
#Começando a coletar os usernames para o trabalho de comparação
for l in top_blitz:
    cursor.execute("SELECT username FROM top_blitz")
    resultado_b=cursor.fetchall()
    link.commit()
for m in top_rapid:
    cursor.execute("SELECT username FROM top_rapid")
    resultado_r=cursor.fetchall()
    link.commit()
for r in top_bullet:
    cursor.execute("SELECT username FROM top_bullet")
    resultado_bli=cursor.fetchall()
    link.commit()
#LISTANDO OS MELHORES JOGADORES
print("+----------------------BULLET---------------------------+")
print("|",resultado_b,"|") 
print("+----------------------RAPID----------------------------+")
print("|",resultado_r,"|")
print("+----------------------BLITZ----------------------------+")
print("|",resultado_bli,"|")
print("+-------------------------------------------------------+")
#Achando os melhores entre as 3
cursor.execute("SELECT * FROM top_blitz INNER JOIN top_bullet on top_bullet.username = top_blitz.username INNER JOIN top_rapid on top_rapid.username = top_blitz.username")
melhores_3=cursor.fetchall()
link.commit()
#Achando os melhores entre rapid e bullet 
cursor.execute("SELECT top_rapid.username , top_bullet.username FROM top_rapid INNER JOIN top_bullet ON top_bullet.username =top_rapid.username")
melhores_rapid_bullet=cursor.fetchall()
link.commit()
#Achando os melhores entre rapid e blitz 
cursor.execute("SELECT top_rapid.username , top_blitz.username FROM top_rapid INNER JOIN top_blitz ON top_blitz.username =top_rapid.username")
melhores_rapid_blitz=cursor.fetchall()
link.commit()
#Achando os melhores entre blitz e bullet 
cursor.execute("SELECT top_blitz.username , top_bullet.username FROM top_blitz INNER JOIN top_bullet ON top_blitz.username =top_bullet.username")
melhores_bullet_blitz=cursor.fetchall()
link.commit()
print("+-------------------Imprimindo Jogadores Comuns-------------------+")
print("Os melhores 3 jogadores:",melhores_3)
print("Os melhores rapid e bullet:",melhores_rapid_bullet)
print("Os melhores rapid e blitz:",melhores_rapid_blitz)
print("Os melhores bullet e blitz:",melhores_bullet_blitz)
