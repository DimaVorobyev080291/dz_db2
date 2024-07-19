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

    def change_client(self, client, first_name='', last_name='', email='', phone=''):
 
        with self.conn.cursor() as cur:
            if first_name != '':
                cur.execute("""
                            UPDATE clients SET first_name=%s WHERE id=%s;
                            """, (first_name,client ))
                self.conn.commit()
                print('Имя изменено.')
            else:
                print('Имя без изменений.')

            if last_name != '':
                cur.execute("""
                            UPDATE clients SET last_name=%s WHERE id=%s;
                            """, (last_name,client ))
                self.conn.commit()
                print('Фамилия изменена.')
            else:
                print('Фамилия без изменений.')

            if email != '':
                cur.execute("""
                            UPDATE clients SET email=%s WHERE id=%s;
                            """, (email,client ))
                self.conn.commit()
                print('Email изменен.')
            else:
                print('Email без изменений.')

            if phone != '':
                cur.execute("""
                        SELECT phone, client, id FROM phones
                        WHERE client=%s ;
                         """, (client,))
                info_phones = (cur.fetchall())

                if len(info_phones) != 1:
                    print('Выберите id телефона который хотите изменить :')
                    for p in info_phones:
                        print (f'{p[0]} {p[2]}')

                    couse_id_phone = int(input())
                    print(couse_id_phone)

                    cur.execute("""
                            UPDATE phones SET phone=%s WHERE id=%s;
                            """, (phone, couse_id_phone))
                    self.conn.commit()
                    print('Телефон изменен.')
                else:
                    cur.execute("""
                            UPDATE phones SET phone=%s WHERE id=%s;
                            """, (phone,client))
                    self.conn.commit()
                    print('Телефон изменен.')
            else:
                print('Телефон без изменений.')

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
                DELETE FROM phones WHERE client=%s ;
                """, ( id,))
        self.conn.commit()

        with self.conn.cursor() as cur:
            cur.execute("""
                DELETE FROM clients WHERE id=%s ;
                """, (id,))
        self.conn.commit()

        print('Клиент удален !')

    def show_client(self, first_name='', last_name='', email='', phone=''):
       with self.conn.cursor() as cur:
            cur.execute("""
                SELECT first_name, last_name, email, client, phone FROM clients
                JOIN phones ON clients.id = phones.client
                WHERE first_name LIKE %s or last_name LIKE %s or email LIKE %s or phone LIKE %s;
                """, (first_name,last_name,email,phone,))
            info = cur.fetchall()

            if last_name != '':
               for i in info :
                    for item in i:
                        if item == last_name:
                            print(i)
                        elif item == email:
                            print(i)
            elif  email != '':
                for i in info :
                    for item in i:
                        if item == last_name:
                            print(i)
                        elif item == email:
                            print(i)
            else:
                print(info)