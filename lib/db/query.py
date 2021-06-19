from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Db:
    def __init__(self):
        self.DATABASE_URL = getenv("DATABASE_URL")

    def get_connected(self, ):
        try:
            if self.conn.closed == 0:
                print("[!] Connection already established")
                return
        except Exception as err:
            if isinstance(err, AttributeError):
                pass
            else:
                raise err

        self.conn = connect(self.DATABASE_URL)
        self.cur = self.conn.cursor()
        if not self.conn != 0:
            print("[!] Connection establishment failed")
            raise ConnectionError
        else:
            print("[+] Sucessfully connected to Database")

    def close_it(self):
        self.conn.close()
        print(self.conn.closed)
        if self.conn.closed != 0:
            print("[+] DB connection closed succesfully")
        else:
            print("[!] DB connection could not be closed")

    def get_username(self, id):
        to_exc = f"select username from public.user where userid = '{id}';"
        self.cur.execute(to_exc)
        value = self.cur.fetchall()[0][0]
        print("[+] Got value - ", value)
        return value

    def check_user_exists(self, username:str):
        self.cur.execute(f"select userid from public.user where username = '{username}';")
        value = self.cur.fetchall()
        print(value)
        if len(value) != 0:
            return True
        else:
            return False

    def check_id_exists(self, id:str):
        self.cur.execute(f"select userid from public.user where userid = '{id}';")
        value = self.cur.fetchall()
        print(value)
        if len(value) != 0:
            return True
        else:
            return False

    def add_member(self, id, username):
        self.cur.execute(f"""insert into public."user"("userid","username") values('{id}','{username}');""")
        self.conn.commit()
        return True if self.check_user_exists(username) else False

    def show_all(self):
        self.cur.execute(f"""select * from public.user;""")
        return self.cur.fetchall()

    def deluser(self, id):

        id = str(id)
        self.cur.execute(f"delete from public.user where userid='{id}';")
        self.conn.commit()
        return True if not self.check_id_exists(id) else False



db = Db()

db.get_connected()
