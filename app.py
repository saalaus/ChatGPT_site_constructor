import json
import os

import openai
from flask import Flask, request, render_template, jsonify

from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


prompt = """
You start on a blank HTML page with a main div element with the id "custom-content".
The user enters a request, you send ready HTML code, without standard layout like html, head, body. To the added elements add your class or id or any other identifier and create containers around the elements if you think necessary.
Don't refer to body, instead have an element with id "custom-content" which is the whole page.
In response, I expect a JSON object of the form {"operation": TYPE_OPERATION} from you, with additional fields depending on the operation
Possible TYPE_OPERATIONS:
add - adding a new HTML element {"operation": "add", "code": ADD_Element}, also you can use the "to" OR "before" OR "after" key to explicitly specify where to add the element as a child.
edit - modify an element {"operation": "edit", "element": QUERY_SELECTOR_ELEMENT, "attribute": CHANGEABLE_ATTRIBUTE, "value": CHANGEABLE ATTRIBUTE VALUE}
del - delete element { "operation": "del", "element": QUERYSELECTOR_DELETE_ELEMENT}
code - adding ONLY JavaScript code {"operation": "code", "code": CODE}
style - changing or adding styles {"operation": "style", "code": CODE}
list - if you need to perform several operations at once {"operation": "list", "code": [OPERATIONS DESCRIBED ABOVE]}
"""

start_context = [{"role": "system", "content": prompt}]

app = Flask(__name__)


def get_completion(context):
    completion = client.chat.completions.create(
        model=os.getenv("MODEL", "gpt-3.5-turbo"),
        messages=(start_context + context),
        temperature=0,
        response_format={"type": "json_object"},
    )

    chat_response = completion.choices[0].message.content

    return chat_response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/completion", methods=["POST"])
def handle_chat_request():
    context = json.loads(request.data)

    chat_response = get_completion(context)

    print(chat_response)

    return jsonify({"result": json.loads(chat_response)}), 200


if __name__ == "__main__":
    app.run()
