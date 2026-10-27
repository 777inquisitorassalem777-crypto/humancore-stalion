import json
from .kernel import CCOSKernel

def main():
    kernel = CCOSKernel()
    print("CCOS-Ω Research Core v0.1 — type 'exit' to quit, '/status' for status.")
    while True:
        try:
            text = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in {"exit", "quit"}:
            break
        if text == "/status":
            print(json.dumps(kernel.status(), ensure_ascii=False, indent=2))
            continue
        if not text:
            continue
        print(json.dumps(kernel.process(text), ensure_ascii=False, indent=2))
