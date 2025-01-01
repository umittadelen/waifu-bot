# waifu bot
 
This project is a chatbot that uses the Llama model to simulate ai waifu based on the personality. I am also planning to add a Flask version later.

## Requirements

- Python 3.6+
- `llama_cpp` library
- `chromaconsole` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tsundere-chatbot.git
    cd tsundere-chatbot
    ```

2. Install the required libraries:
    ```sh
    pip install llama_cpp chromaconsole
    ```

3. Download the model file from [Hugging Face](https://huggingface.co/TheBloke/Ana-v1-m7-GGUF/resolve/main/ana-v1-m7.Q4_K_M.gguf) and place it in the root directory of the project.

## Usage

1. Run the chatbot:
    ```sh
    python app.py
    ```

2. Follow the prompts to start a new conversation or load from a previous log.

3. Type your messages and interact with the chatbot. Type **exit** to end the conversation.

## Files

- `app.py`: Main script to run the chatbot.
- `ana-v1-m7.Q4_K_M.gguf`: Model file (download separately).
- `readme.md`: Project documentation.
- `personality.json`: Stores the personality and name of the chatbot.
- `conversation_log.json`: Stores the conversation log.

## Acknowledgements

- Inspired by [Just Rayen](https://www.youtube.com/@JustRayen)'s video on YouTube. (GGUF)
- Uses the Llama model from [llama_cpp](https://pypi.org/project/llama-cpp-python/).
- Console styling with [chromaconsole](https://pypi.org/project/chromaconsole/).