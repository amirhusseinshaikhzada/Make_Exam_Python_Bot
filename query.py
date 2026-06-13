from schema import db_url
import psycopg2


def connect_to_db():
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    return conn , cursor



def add_question(question , option1 , option2 , option3 , option4 , correct_option):
    conn , cursor = connect_to_db()
    cursor.execute('''
        INSERT INTO questions (question , option1 , option2 , option3 , option4 , correct_option) VALUES (%s , %s , %s , %s , %s , %s)''' , (question , option1 , option2 , option3 , option4 , correct_option))
    conn.commit()
    conn.close()



def get_all_questions():
    conn , cursor = connect_to_db()
    cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    conn.close()
    return questions



def save_result(user_id , score):
    conn , cursor = connect_to_db()
    cursor.execute("INSERT INTO results (user_id , score) VALUES (%s , %s)" , (user_id , score))
    conn.commit()
    conn.close()



def get_user_results(user_id):
    conn , cursor = connect_to_db()
    cursor.execute("SELECT score FROM results WHERE user_id = %s" , (user_id , ))
    scores = cursor.fetchall()
    conn.close()
    return scores