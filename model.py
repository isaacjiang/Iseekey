__author__ = 'isaacjiang'
# import MySQLdb

import sqlalchemy

# db = MySQLdb.connect(host='127.0.0.1', db='ik', user='ikadmin', passwd='ikadmin', port=3306)

class data():
    engine = sqlalchemy.create_engine('mysql+mysqldb://ikadmin:ikadmin@localhost/ik')

    def Coursework(self):

        connection = self.engine.connect()

        result = connection.execute(
            "select coursework_name, substring(coursework_file from 3) as coursework_file  from coursework_name")

        course = {}
        for row in result:
            course[row['coursework_name']] = {'text': row['coursework_name'], 'is_selected': False}

        connection.close()
        return course

    def CwPlaying_desc(self):

        connection = self.engine.connect()
        result = connection.execute(
            "select coursework_name,coursework_desc from coursework_name")
        course_desc = {}
        for row in result:
            course_desc[row['coursework_name']] = row['coursework_desc']
        connection.close()
        return course_desc

    def CwPlaying_file(self):

        connection = self.engine.connect()
        result = connection.execute(
            "select coursework_name,substring(coursework_file from 3) as coursework_file  from coursework_name")
        course_file = {}
        for row in result:
            course_file[row['coursework_name']] = row['coursework_file']
        connection.close()
        return course_file