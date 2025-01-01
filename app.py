from llama_cpp import Llama
from chromaconsole import Color, Style
import os, json

if not os.path.exists("./ana-v1-m7.Q4_K_M.gguf"):
    print(f"{Color.text("#F00")}Model file not found. Please download the model file and place it in the root directory.\n{Color.text("#0F0")}https://huggingface.co/TheBloke/Ana-v1-m7-GGUF/resolve/main/ana-v1-m7.Q4_K_M.gguf {Style.reset()}")
    exit()

#TODO: Load the Llama model
llm = Llama(
    model_path="./ana-v1-m7.Q4_K_M.gguf",  # Update with your model's path
    n_gpu_layers=-1,  # Use all available GPU layers, or adjust if needed
    n_ctx=10000,  # Set the context length (adjust based on the model's limits)
    verbose=False  # Set to True for verbose output
)

#! Godness
#! Gracious
#! U This Model Runs
#! Fast
#? - Just Rayen
#TODO: Define a function to get the response from the GGUF model
def get_llm_response(prompt):
    output = llm(
        prompt,
        max_tokens=64,
        stop=["User:", "\n"],
        echo=False
    )
    return output["choices"][0]["text"]

#TODO: Define a function to save the conversation log to a file
def save_log(personality, prompt):
    """Save the conversation log to a file in JSON format."""
    log_data = {
        "personality": personality,
        "prompt": prompt
    }
    with open("conversation_log.json", "w", encoding="utf-8") as log_file:
        json.dump(log_data, log_file, ensure_ascii=False, indent=4)

#TODO: Define the personality and name of the chatbot
if os.path.exists("personality.json"):
    with open("personality.json", "r", encoding="utf-8") as personality_file:
        personality_data = json.load(personality_file)
        personality = personality_data.get("personality", "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.")
        name = personality_data.get("name", "tsundere-chan")
else:
    personality_data = {
        "personality": "You are a tsundere. You act cold and dismissive but secretly care about the user. Respond like a tsundere in all interactions.",
        "name": "tsundere-chan"
    }
    with open("personality.json", "w", encoding="utf-8") as personality_file:
        json.dump(personality_data, personality_file, ensure_ascii=False, indent=4)

# Ask user if they want to start a new conversation or load from the log
load_from_log = input(f"{Color.text("#07F")}Do you want to load from the previous log? {Color.text("#0AF")}{Style.italic()}(y/n): {Style.reset()}{Color.text("#0DF")}").lower()
print(f"{Style.reset()}", end="")

if load_from_log == "y" and os.path.exists("conversation_log.json"):
    with open("conversation_log.json", "r", encoding="utf-8") as log_file:
        log_data = json.load(log_file)
        personality = log_data.get("personality", personality)  # Retain previous personality if present
        prompt = log_data.get("prompt", "")
else:
    prompt = ""  # Start a new conversation

#TODO: Add a loop to keep the conversation going
if __name__ == "__main__":
    try:
        while True:
            user_input = input(f"{Style.bold()}{Color.text("#FF0")}You:{Style.reset()} {Color.text("#FF7")}")
            print(Style.reset())

            if user_input.lower() == "exit":
                break

            prompt += f"""\n\nUser: "{user_input}"\nYou: """
            response = get_llm_response(personality + prompt)
            prompt += response

            print(f"{Style.bold()}{Color.text("#F00")}{name}:{Style.reset()}{Color.text("#F77")}", response, Style.reset(),"\n")

    except KeyboardInterrupt:
        print(f"\n{Color.text("#F0F")}Ctrl+C detected. Saving log and exiting...{Style.reset()}")

    except SystemExit:
        print(f"\n{Color.text("#F0F")}Terminal close detected. Saving log and exiting...{Style.reset()}")

    finally:
        save_log(personality, prompt)