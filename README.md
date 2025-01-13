# waifu bot
 
This project is a chatbot that uses the Llama model to simulate ai waifu based on the personality. I am also planning to add a Flask version later.

## Requirements

- Python 3.6+
- `llama_cpp` library
- `chromaconsole` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/umittadelen/waifu-bot.git
    cd waifu-bot
    ```

2. Install the required libraries:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the model file from [Hugging Face](https://huggingface.co/TheBloke/Ana-v1-m7-GGUF/resolve/main/ana-v1-m7.Q4_K_M.gguf) and place it in the root directory of the project.

## Usage

1. Run the chatbot:
    ```sh
    python app.py
    ```

2. open `0.0.0.0:8080`(default) on browser. (you can change it in `config.json`)

3. Type your messages and interact with the chatbot. Type **/exit** to save the conversation.

## Files

- `app.py`: Main script to run the chatbot.
- `config.json`: Configuration file for model path, ip:port, etc.
- `ana-v1-m7.Q4_K_M.gguf`: Model file (download separately).
- `chat_history.json`: Data when saving the conversation (contains the conversation, name and personality)

## Acknowledgements

- Inspired by [Just Rayen](https://www.youtube.com/@JustRayen)'s video on YouTube. (GGUF)
- Uses the Llama model from [llama_cpp](https://pypi.org/project/llama-cpp-python/).
- Console styling with [chromaconsole](https://pypi.org/project/chromaconsole/).