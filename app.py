from llama_cpp import Llama
from chromaconsole import Color, Style
import os, json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

config_path = "./config.json"
with open(config_path, "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

generating_response = False #! a global variable used to prevent spamming.

if not os.path.exists(str(config["model_path"])):
    print(f"{Color.text("#F00")}Model file not found. Please download the model file and place it in the root directory.\n{Color.text("#0F0")}https://huggingface.co/TheBloke/Ana-v1-m7-GGUF/resolve/main/ana-v1-m7.Q4_K_M.gguf {Style.reset()}")
    input("Press enter to exit...")
    exit()

llm = Llama(
    model_path=str(config["model_path"]),
    n_gpu_layers=int(config["n_gpu_layers"]),
    n_ctx=int(config["n_ctx"]),
    verbose=bool(config["verbose"])
)

def get_llm_response(prompt):
    global generating_response
    if not generating_response:
        generating_response = True
        output = llm(
            prompt,
            max_tokens=config["max_tokens"],
            stop=["User:", "\n"],
            echo=False
        )
        generating_response = False
        return output["choices"][0]["text"]
    else:
        return False

def save_log(name, personality, chat_history):
    """Save the conversation log to a file in JSON format."""
    log_data = {
        "name": name,
        "personality": personality,
        "chat_history": chat_history
    }
    with open(config["history_save_path"], "w", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)

def load_log():
    """Load the conversation log from a file in JSON format."""
    if os.path.exists(config["history_save_path"]):
        with open(config["history_save_path"], "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
    else:
        config_data = {
            "name": "tsundere-chan",
            "personality": "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.",
            "chat_history": []
        }
        with open(config["history_save_path"], "w", encoding="utf-8") as config_file:
            json.dump(config_data, config_file, ensure_ascii=False, indent=4)

    global name, personality, chat_history
    name = config_data.get("name", "tsundere-chan")
    personality = config_data.get("personality", "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.")
    chat_history = config_data.get("chat_history", [])

load_log()

@app.route("/")
def home():
    return render_template("index.html", name=name, personality=personality, chat_history=chat_history)

@app.route("/send_response", methods=["POST"])
def send_response():
    global chat_history
    user_input = request.form["user_input"]

    if chat_history != []:
        prompt = ""
        for chat in chat_history:
            prompt += f'\n\nUser: "{chat["user"]}"\nYou: {chat["bot"]}'
        prompt += f"""\n\nUser: "{user_input}"\nYou: """
    else:
        prompt = f"""\n\nUser: "{user_input}"\nYou: """

    response = get_llm_response("##ADMIN:"+personality + prompt)

    chat_history.append({"user": user_input, "bot": response})

    if response is False:
        return jsonify({"response": None})

    prompt += response
    return jsonify({"response": response, "name": name})

@app.route("/change_personality", methods=["POST"])
def change_personality():
    global name, personality, chat_history
    personality = request.form["user_input"]
    save_log(name, personality, chat_history)
    load_log()
    return jsonify({"status": "success"})

@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    return jsonify({"chat_history": chat_history, "name": name})

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    save_log(name, personality, chat_history)
    return jsonify({"status": "success"})

#save the data
@app.route("/save")
def save():
    save_log(name, personality, chat_history)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True, host=config["host"], port=config["port"])