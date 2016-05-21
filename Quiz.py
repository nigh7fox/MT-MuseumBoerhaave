import pymysql.cursors
import Twitter
import base64
from ConnectToDB import ConnectDB as cdb


class QuizBH(object):

    def __init__(self, question_id, label_id):
        self.connect = cdb("localhost", "root", "t0ntibomama_", "MuseumBoerhaave")
        self.question_id = question_id
        self.label_id = label_id

    def remove_static(self):
        pass

    def split_row_questions(self):
        data_list = self.connect.get_db_field(str(self.question_id)).split(',')
        return data_list

    def split_row_labels(self):
        data_list = self.connect.get_labels(str(self.label_id)).split(',')
        return data_list

    def get_label_title(self):
        bh_label_header = self.split_row_labels()[1].replace("'", "").strip(" ")
        return bh_label_header

    def get_label_subtitle(self):
        bh_label_header = self.split_row_labels()[2].replace("'", "").strip(") ")
        return bh_label_header

    def get_question_id(self):
        bh_question_id = self.split_row_questions()[0].strip("(")
        return bh_question_id

    def get_question(self, question_id):
        data_list = self.connect.get_db_field(str(question_id)).split(',')
        bh_question = str(data_list[1]).replace("'", "").strip(" ")
        return bh_question

    def get_answer(self):
        bh_answer = str(self.split_row_questions()[2]).replace("'", "").strip(" ")
        return bh_answer

    def get_question_video_link(self, question_id):
        data_list = self.connect.get_db_field(str(question_id)).split(',')
        bh_link = str(data_list[3]).replace("'", "").strip(") ")
        return bh_link

    def check_answer(self, answer):
        return answer is self.get_answer()

    def play(self):
        print("#########################################")
        print("## Welcome to the Museum Boerhave Quiz ##")
        print("#########################################")
        print("\n")

        row_count = (self.connect.get_questions_row_count()+1)
        i = 1
        correct = 0

        print("######################")
        name = input("## What is your name?: ")
        print("######################")
        print("\n")

        while i < row_count:
            question = self.get_question()
            user_input = input(question + ": ")
            if self.check_answer(user_input) is True:
                correct += 5
            i += 1
        self.connect.insert_highscore(name, str(correct))
        print("\n")
        print("########################################")
        print(" ###### " + name + ", FINAL SCORE IS: " + str(correct) + "  ######")
        print("########################################")

        total_score = (row_count*5)
