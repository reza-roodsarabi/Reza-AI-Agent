import json


def load_memory():
    with open("memory.json", "r") as f:
        return json.load(f)


def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)