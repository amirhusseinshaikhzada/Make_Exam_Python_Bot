from schema import db_url
import psycopg2




db_path = "quiz.db"



conn = psycopg2.connect(db_path)
cursor = conn.cursor()


cursor.execute(
    '''
    INSERT INTO questions (question , option1 , option2 , option3 , option4 , correct_option) VALUES
('4' , 'پایتون چیست؟' , 'یک سیستم عامل' , 'نام یک حیوان' , 'یک مرورگر' , 'یک زبان برنامه نویسی'),
('2' , 'Table' , 'House' , 'int' , 'Car' , 'کدام گزینه نوع داده در پایتون است؟'),
('3' , 'out()' , 'print()' , 'echo()' , 'write()' , 'برای چاپ در پایتون از چه دستوری استفاده میشود؟'),
('3' , '10' , '6' , '9' , '5' , 'خروجی 2 ** 3 در پایتون چند میشود؟'),
('3' , '10' , '6' , '9' , '5' , 'lffjojcmfjffm'),
('1'  , '1' , 'afwetefw' ,'fsdarqaafa' , 'ddbdyztwth' ,'ertgdhtdejdj')''')


conn.commit()
conn.close()