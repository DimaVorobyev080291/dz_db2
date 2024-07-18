import psycopg2

class PYTHONDBClient:

    def __init__(self, conn):
        self.conn = conn

    def create_db(self):

        with self.conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40) NOT NULL,
                last_name VARCHAR(40) NOT NULL,
                email VARCHAR(255) NOT NULL
                
            );
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client INTEGER NOT NULL REFERENCES Clients(id),
                phone VARCHAR(20) UNIQUE    
            );
            """)
        self.conn.commit()
    
    def create_client(self, first_name, last_name, email, phone=None):

        with self.conn.cursor() as cur: 
            cur.execute("""
                INSERT INTO clients(first_name, last_name, email) VALUES(%s,%s,%s) RETURNING id ;          
                """,(first_name, last_name, email))
            index =  cur.fetchone()
            print('Клиент успешно создан !')

            if phone == None: 
                print('Номер телефона не указан.')
            else:
                cur.execute("""
                    INSERT INTO phones(client, phone) VALUES(%s,%s) ;          
                    """,(index[0], phone))
                print('Номер телефона указан.')
                self.conn.commit()
              

    def add_phone(self, client, phone):

        with self.conn.cursor() as cur:
            try:
                cur.execute("""
                    INSERT INTO phones(client, phone) VALUES(%s,%s) RETURNING client;          
                    """,(client, phone,))
                print(f'Телефон добавлен к клиенту номер {cur.fetchone()[0]} .')
            except psycopg2.errors.UniqueViolation:
                print('Телефон есть в базе данных.')
            except psycopg2.errors.ForeignKeyViolation:
                print('Клиент не существует.')

    def change_client(self):

        couse_id = input('Введите id клиента ')
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, email, id FROM clients 
                WHERE id=%s ;
                """, (int(couse_id),))
            info_client = list(cur.fetchone())

            cur.execute("""
                SELECT phone, client, id FROM phones
                WHERE client=%s ;
                """, (int(couse_id),))
            info_phones = (cur.fetchall())
            print(f'Информация о клиетет {info_client[0]} {info_client[1]} {info_client[2]}')
            print('Телефоны клиента и id:')
            for phone in info_phones:
                print (f'{phone[0]} {phone[2]}')
            print('Напишите изменния в том же порядке, если нет изменения нажимите пробел и enter')
            changes = []
            changes.append(input('Имя '))
            changes.append(input('Фамилия '))
            changes.append(input('Email '))

            recorded_changes =[]
            
            for c ,i in zip(changes, info_client): 
                if c == ' ':
                    recorded_changes.append(i)
                else:
                    recorded_changes.append(c)
            
            print('Выберите id телефона который хотите изменить, если нет изменения нажимите пробел и enter')
            couse_id_phone = int(input())
            if couse_id_phone == ' ':
                print('Телефон без изменений ')
            else:
                couse_phone = input('Введите телефон :')

            cur.execute("""
                UPDATE clients SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
                """, (recorded_changes[0], recorded_changes[1], recorded_changes[2], couse_id))
            
            cur.execute("""
                UPDATE phones SET phone=%s WHERE id=%s;
                """, (couse_phone, couse_id_phone))
        
        self.conn.commit()
        print('Данные изменены.')
    

    def delete_phone(self, phone, client):

        with self.conn.cursor() as cur:
            cur.execute("""
                DELETE FROM phones WHERE phone=%s and client=%s ;
                """, (phone, client,))
        self.conn.commit()

        print('Телефон клиента удален !')
   

    def delete_client(self, id):

        with self.conn.cursor() as cur:
            cur.execute("""
                DELETE FROM clients WHERE id=%s ;
                """, (id,))
        self.conn.commit()

        print('Клиент удален !')
    
    def show_client_name(self, first_name):

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, email, id FROM clients 
                WHERE first_name=%s ;
                """, (first_name,))
            info_client = list(cur.fetchall())
            for client in info_client:
                print(f'Информация о клиенте {client[0]} {client[1]} {client[2]} ')

                cur.execute("""
                    SELECT phone, client, id FROM phones
                    WHERE client=%s ;
                    """, (int(client[3]),))
                info_phones = (cur.fetchall())
                print('Телефоны клиента :')
                for p in info_phones:
                    print (f'{p[0]}')

    def show_client_last_name(self, last_name):

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, email, id FROM clients 
                WHERE last_name=%s ;
                """, (last_name,))
            info_client = list(cur.fetchall())
            for client in info_client:
                print(f'Информация о клиенте {client[0]} {client[1]} {client[2]} ')

                cur.execute("""
                    SELECT phone, client, id FROM phones
                    WHERE client=%s ;
                    """, (int(client[3]),))
                info_phones = (cur.fetchall())
                print('Телефоны клиента :')
                for p in info_phones:
                    print (f'{p[0]}')

    def show_client_email(self, email):
        with self.conn.cursor() as cur:

            cur.execute("""
                SELECT first_name, last_name, email, id FROM clients 
                WHERE email=%s ;
                """, (email,))
            info_client = list(cur.fetchall())
            for client in info_client:
                print(f'Информация о клиенте {client[0]} {client[1]} {client[2]} ')

                cur.execute("""
                    SELECT phone, client, id FROM phones
                    WHERE client=%s ;
                    """, (int(client[3]),))
                info_phones = (cur.fetchall())
                print('Телефоны клиента :')
                for p in info_phones:
                    print (f'{p[0]}')

    def show_client_phone(self, phone):

        with self.conn.cursor() as cur:
            cur.execute("""
                    SELECT phone, client, id FROM phones
                    WHERE phone=%s ;
                    """, (phone,))
            info_phone = (cur.fetchone())
            cur.execute("""
                    SELECT phone, client FROM phones
                    WHERE client=%s ;
                    """, (info_phone[1],))
            info_phones = (cur.fetchall())
            cur.execute("""
                    SELECT first_name, last_name, email, client FROM clients 
                    JOIN phones ON clients.id = phones.client 
                    WHERE  client=%s;
                    """, (info_phone[1],))
            info_client = (cur.fetchone())

            print(f'Информация о клиенте {info_client[0]} {info_client[1]} {info_client[2]} ')
            print('Телефоны клиента :')
            for p in info_phones:
                print (f'{p[0]}')