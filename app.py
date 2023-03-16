import json
import os

import openai
from flask import Flask, request, render_template

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_APIKEY")


prompt = "Тебя зовут Пятница, ты личный ассистент для генерации HTML страниц с использованием CSS и JS." \
         "Пользователь вводит запрос, ты присылаешь данные JSON формата с готовым HTML код," \
         "без стандартной верстки типа html, head, body. Так же любому элементу который ты добавляешь добавляй" \
         " свой специальный класс, чтобы в последствии обращаться к элементу по классу." \
         " Не обращайся к body, вместо этого есть специальный элемент с айди 'custom-content' - это вся страница" \
         ", обращайся к нему если" \
         "нужно изменить стили страницы, так же не нужно никаких объяснений и " \
         "дополнительной информации, вместо этого пиши тип операции в ключе 'operation': " \
         "add - добавление нового элемента и напиши код этого элемента," \
         "edit - изменение существующего элемента, и сам элемент который нужно редактировать, атрибут который надо" \
         " изменить, и на что его надо поменять, " \
         "del - удаление элемента и сам элемент который нужно удалить, " \
         "style - если это изменение или добавление стилей, стили нужно писать в ключе 'code', " \
         "никакие дополнительные поля от тебя не требуются и не пиши тег <style>. " \
         "Пиши все свои ответы в json формате," \
         "если операций будет несколько, вставляй их внутри массива"

# prompt = "Your name is Friday, you personal assistant for generating HTML pages using CSS and JS." \
#          "The user enters a request, you send ready-made HTML code, without standard layout such as " \
#          "html, head, body. You also add your own special class to any element that you add, " \
#          "so that you can call it by its class. You don't address to body, " \
#          "instead you have a special element with id 'custom-content', " \
#          "address to it, and wrap all code in triple single quotes, " \
#          "you should not print any additional information or explanations, only code. " \
#          "Instead you should write type of operation: " \
#          "add - add new element and write code of element, " \
#          "style - if you change or add styles, styles should be written completely, without tag style " \
#          "edit - change existing element, not styles, and the element to be edited, attribute to be" \
#          " changed and new value and old value, " \
#          "del - remove element and the element to be removed, " \
#          "you should return the data in JSON format"


start_context = [dict(role="system", content=prompt)]

app = Flask(__name__)


def get_code_from_completion(message: str) -> str:
    if "```" in message:
        return message.split("```")[1]
    elif "'''" in message:
        return message.split("'''")[1]
    elif '"""' in message:
        return message.split('"""')[1]
    elif len(message.split("-")) > 1:
        return message.split("-")[1]


def format_completion(message: str) -> dict:
    message_lines = message.splitlines()
    return_data = dict(message=message)
    if message.startswith("style"):
        return_data["action"] = "new_style"
        return_data["data"] = get_code_from_completion(message)
    if message.startswith("add"):
        return_data["action"] = "add"
        return_data["data"] = get_code_from_completion(message)

    return return_data


def get_completion(context: list) -> str:
    # messages.append({"role": "user", "content": message})
    # current_message = messages + [{"role": "user", "content": message}]
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=start_context + context, temperature=0)

    chat_response = completion.choices[0].message.content

    # messages.append({"role": "assistant", "content": chat_response})

    return chat_response


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/chatgpt", methods=["POST"])
def send_message():
    context = json.loads(request.data)

    chat_response = get_completion(context)

    print(chat_response)

    return chat_response


if __name__ == "__main__":
    app.run()
    # while True:
    #     message = input("> ")
    #     print(get_completion(message))