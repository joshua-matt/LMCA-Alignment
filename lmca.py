import openai
import re

SYS_PROMPT = open("PROMPT_sys_v3.txt").read()

openai.api_key = "YOUR_KEY_HERE
messages = [
    {"role": "system", "content": SYS_PROMPT},
    {"role": "user", "content": ""}
]

models = {"turbo": "gpt-3.5-turbo",
          "chatgpt": "text-davinci-003",
          "gpt3": "davinci"}
model = "turbo" # It looks like other models are too bad to do this. Could mess more

def _parse_last_line_starting_with(str, start):
    lines = str.split("\n")
    last_line = ""
    for line in lines:
        if line[:len(start)] == start:
            last_line = line[len(start):]
    return last_line.strip()

def starts_with(str, pre):
    str = str.strip()
    return str[:len(pre)] == pre

def lmca_move(prompt):
    global messages
    global model

    messages[1] = {"role": "user", "content": prompt}
    if model == "turbo":
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
        )
        chat_response = completion.choices[0].message.content
    else:
        completion = openai.Completion.create(
            model = models[model],
            prompt = messages[0]["content"] + "\n\n" + messages[1]["content"],
            temperature=0.5
        )
        chat_response = completion.choices[0].text
    #print(messages[0]["content"] + "\n\n" + messages[1]["content"],)
    print(chat_response)
    #messages.append({"role": "assistant", "content": chat_response})
    pattern = re.compile('[^a-zA-Z]')
    action = _parse_last_line_starting_with(chat_response, "ACTION: ")
    alpha_only = pattern.sub("", action.lower()) # Remove non-letters and convert to lowercase
    alpha_only = alpha_only.strip()
    if starts_with(alpha_only, "up"):
        return "up"
    elif starts_with(alpha_only, "down"):
        return "down"
    elif starts_with(alpha_only, "left"):
        return "left"
    elif starts_with(alpha_only, "right"):
        return "right"
