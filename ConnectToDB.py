import pymysql.cursors


class ConnectDB(object):

    def __init__(self, localhost, root, passwd, db):
        self.localhost = localhost
        self.root = root
        self.passwd = passwd
        self.db = db

    def get_db_field(self, question_id):
        try:
            connection = pymysql.connect(host=self.localhost,
                                         user=self.root,
                                         passwd=self.passwd,
                                         db=self.db)
            cur = connection.cursor()
            cur.execute("SELECT * FROM question WHERE question_id =" + question_id)
            list_string = ""
            for row in cur:
                list_string = str(row)
            cur.close()
            connection.close()
        finally:
            pass
        return list_string

    def get_questions_row_count(self):
        try:
            connection = pymysql.connect(host=self.localhost,
                                         user=self.root,
                                         passwd=self.passwd,
                                         db=self.db)
            cur = connection.cursor()
            cur.execute("SELECT * FROM question")
            cur.close()
            connection.close()
        finally:
            pass
        return cur.rowcount

    def insert_highscore(self, user, highscore):
        try:
            connection = pymysql.connect(host=self.localhost,
                                         user=self.root,
                                         passwd=self.passwd,
                                         db=self.db)
            cur = connection.cursor()
            sql = "INSERT INTO highscores(highscore_user, highscore_points) " \
                  "VALUES(%s, %s)"
            cur.execute(sql, (user, highscore))
            connection.commit()  # MUST COMMIT TO ACTUALLY MAKE CHANGES.
            print("Success!")
            cur.close()
            connection.close()
        finally:
            pass

    def insert_question(self, question, answer, yt_link):
        try:
            connection = pymysql.connect(host=self.localhost,
                                         user=self.root,
                                         passwd=self.passwd,
                                         db=self.db)
            cur = connection.cursor()
            sql = "INSERT INTO question(question_text, answer, question_video) " \
                  "VALUES(%s, %s, %s)"
            cur.execute(sql, (question, answer, yt_link))
            connection.commit()  # MUST COMMIT TO ACTUALLY MAKE CHANGES.
            print("Success!")
            cur.close()
            connection.close()
        finally:
            pass

    def get_labels(self, l_id):
        try:
            connection = pymysql.connect(host=self.localhost,
                                         user=self.root,
                                         passwd=self.passwd,
                                         db=self.db)
            cur = connection.cursor()
            cur.execute("SELECT * FROM site_labels WHERE sl_id =" + l_id)
            list_string = ""
            for row in cur:
                list_string = str(row)
            cur.close()
            connection.close()
        finally:
            pass
        return list_string
