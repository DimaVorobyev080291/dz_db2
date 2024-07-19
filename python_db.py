import psycopg2
import db_client

names = ['Анна','Екатерина','Оля','Света','Таня','Иван','Петр','Семен','Артур','Евгений','Оля']
last_names = ['Ефремова','Великая','Светова','Васечкина','Горбышова','Иванов','Петров','Семенов','Пирожков','Иванов','Москалюк']
emails = ['11111111@mail.ru','ouwhvuih@mail.ru','ytytytytyt@mail.ru','trtryry@mail.r','777777@mail.r','777777@mail.r','5555555@mail.r','766767676@mail.r','twehicgew@mail.r','fguywgy@mail.r','yuwgyufg@mail.r']
phones = ['11111111','ouwhvuih','ytytytytyt','trtryry','777777','777777554','5555555','766767676','twehicgew','fguywgy454','yuwgyufg676',]

with psycopg2.connect(database="test", user="postgres", password="gearsofwar2") as conn:
    client = db_client.PYTHONDBClient(conn)
    create_db = client.create_db()
    for n,ln,em,ph in zip(names, last_names,emails,phones):
        client.create_client(n,ln,em,ph)
    client.create_client('Чижик','Чижиков','2mail@mail')
    client.create_client('Амур','Лимуров','123457@mail.ty')
    client.add_phone(1 , '00000000')
    client.add_phone(1 , '22222222')
    client.add_phone(1 , '4444444')
    client.add_phone(5 , 'gf3883646737')
    client.add_phone(10 , '7777731212')
    client.add_phone(9 , '64356345647')
    client.change_client(4,first_name='anna', phone='+01+03+03+04+0+40')
    client.delete_phone('4444444', 1)
    client.delete_client(13)
    client.show_client(first_name='Оля', last_name='Москалюк')
conn.close()