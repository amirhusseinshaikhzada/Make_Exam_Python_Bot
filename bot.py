from telebot import TeleBot , types
from flask import request
from dotenv import load_dotenv
from schema import create_tables
import query
import os
import flask


create_tables()
load_dotenv()
bot_token = os.getenv("BOT_TOKEN")


bot = TeleBot(bot_token , threaded=False)

app = flask.Flask(__name__)

user_answers = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Add Question" , "Take Quiz" , "My Results")
    bot.send_message(message.chat.id , "Wellcome To Quiz Bot" , reply_markup=markup)


@bot.message_handler(func=lambda msg: msg.text in ["Add Question" , "Take Quiz" , "My Results"])
def menu_handel(message):
    if message.text == "Add Question":
        bot.send_message(message.chat.id , "Send Me The Question In This Format:\n Question | Option1 | option2 | Option3 | option4 | Correct Option Number")
        bot.register_next_step_handler(message , add_question_handler)
    elif message.text == "Take Quiz":
        start_quiz(message)
    elif message.text == "My Results":
        scores = query.get_user_results(message.from_user.id)
        if scores:
            avg = sum(s[0] for s in scores) / len(scores)
            bot.send_message(message.chat.id , f"Your Past Scores: {[s[0] for s in scores]}\nAverage:{avg:.2f}")
        else:
            bot.send_message(message.chat.id , "No Results found.")




def add_question_handler(message):
    try:
        parts = message.text.split("|")
        if len(parts) != 6:
            raise ValueError
        question , o1 , o2 , o3 , o4 , correct = [p.strip() for p in parts]
        query.add_question(question , o1 , o2 , o3 , o4 , int(correct))
        bot.send_message(message.chat.id , "Question Added Successfully.")
    except Exception:
        bot.send_message(message.chat.id , "Invalid Format. Try Again.")





def start_quiz(message):
    questions = query.get_all_questions()
    if not questions:
        bot.send_message(message.chat.id , "No Questions Available.")
        return
    user_answers[message.from_user.id] = {"Questions" : questions , "current" : 0 , "score" : 0}
    send_question(message.chat.id , message.from_user.id)





def send_question(chat_id , user_id):
    state = user_answers[user_id]
    if state["current"] < len(state["Questions"]):
        q = state["Questions"][state["current"]]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("1" , "2" , "3" , "4")
        bot.send_message(chat_id , f"Q: {q[1]}\n1) {q[2]}\n2) {q[3]}\n3) {q[4]}\n4) {q[5]}" , reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id , check_answer)
    else:
        finish_quiz(chat_id , user_id)




def check_answer(message):
    user_id = message.from_user.id
    state = user_answers[user_id]
    q = state["Questions"][state["current"]]
    try:
        if int(message.text) == q[6]:
            state["score"] += 1
    except:
        pass
    state["current"] += 1
    send_question(message.chat.id , user_id)



def finish_quiz(chat_id , user_id):
    state = user_answers[user_id]
    score = state["score"]
    total = len(state["Questions"])
    query.save_result(user_id , score)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Add Question" , "Take Quiz" , "My Results")

    bot.send_message(chat_id , f"Quiz Finished. Your Score: {score}/{total}" , reply_markup=markup)
    del user_answers[user_id]







@app.route(f"/{bot_token}" , methods=["POST"])
def webhook():
    raw = request.get_data().decode("utf-8")
    print(f"Raw Update: {raw}")
    update = types.Update.de_json(raw)
    print(f"Parsed Update: {update}")
    bot.process_new_updates([update])
    return "0k" , 200


@app.route("/")
def index():
    return "Bot Is Runing!" , 200




if __name__ == "__main__":
    app.run(host="0.0.0.0" , port=8080)





bot.polling()