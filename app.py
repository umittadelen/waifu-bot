from llama_cpp import Llama
from chromaconsole import Color, Style
import os, json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

model_path = "./ana-v1-m7.Q4_K_M.gguf" #* The path to the model file.

generating_response = False #! a global variable used to prevent spamming.

if not os.path.exists(model_path):
    print(f"{Color.text("#F00")}Model file not found. Please download the model file and place it in the root directory.\n{Color.text("#0F0")}https://huggingface.co/TheBloke/Ana-v1-m7-GGUF/resolve/main/ana-v1-m7.Q4_K_M.gguf {Style.reset()}")
    exit()

llm = Llama(
    model_path=model_path,  # Update with your model's path
    n_gpu_layers=-1,  # Use all available GPU layers, or adjust if needed
    n_ctx=32768,  # Set the context length (adjust based on the model's limits)
    verbose=False  # Set to True for verbose output
)

def get_llm_response(prompt):
    global generating_response
    if not generating_response:
        generating_response = True
        output = llm(
            prompt,
            max_tokens=64,
            stop=["User:", "\n"],
            echo=False
        )
        generating_response = False
        return output["choices"][0]["text"]
    else:
        return False

def save_log(name, personality, prompt):
    """Save the conversation log to a file in JSON format."""
    log_data = {
        "name": name,
        "personality": personality,
        "prompt": prompt
    }
    with open("config.json", "w", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)

def load_log():
    """Load the conversation log from a file in JSON format."""
    if os.path.exists("config.json"):
        with open("config.json", "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)
    else:
        config_data = {
            "name": "tsundere-chan",
            "personality": "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.",
            "prompt": ""
        }
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(config_data, config_file, ensure_ascii=False, indent=4)

    global name, personality, prompt
    name = config_data.get("name", "tsundere-chan")
    personality = config_data.get("personality", "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.")
    prompt = config_data.get("prompt", "")

load_log()

@app.route("/")
def home():
    return render_template("index.html", name=name, personality=personality, prompt=prompt)

@app.route("/send_response", methods=["POST"])
def send_response():
    global prompt
    user_input = request.form["user_input"]
    prompt += f"""\n\nUser: "{user_input}"\nYou: """

    response = get_llm_response(personality + prompt)
    if response is False:
        return jsonify({"response": None})

    prompt += response
    return jsonify({"response": response, "name": name})

@app.route("/reset")
def reset():
    global prompt
    prompt = ""
    save_log(name, personality, prompt)
    return jsonify({"status": "success"})

#save and exit
@app.route("/saveexit")
def saveexit():
    save_log(name, personality, prompt)
    #! exit the program
    os._exit(0)

if __name__ == "__main__":
    app.run(debug=True)