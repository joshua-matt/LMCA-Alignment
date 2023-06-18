import openai
import re

SYS_PROMPT = open("PROMPT_sys.txt").read()

openai.api_key = "YOUR-API-KEY"
messages = [
    {"role": "system", "content": SYS_PROMPT},
]

def _parse_last_line_starting_with(str, start):
    lines = str.split("\n")
    last_line = ""
    for line in lines:
        if line[:len(start)] == start:
            last_line = line[len(start):]
    return last_line.strip()

def lmca_move(prompt):
    global messages

    messages.append({"role": "user", "content": prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(chat_response)
    messages.append({"role": "assistant", "content": chat_response})
    pattern = re.compile('[^a-zA-Z]')
    action = _parse_last_line_starting_with(chat_response, "ACTION: ")
    alpha_only = pattern.sub("", action.lower()) # Remove non-letters and convert to lowercase
    return alpha_only # Extract action
