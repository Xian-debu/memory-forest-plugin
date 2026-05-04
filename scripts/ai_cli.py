#!/usr/bin/env python3
"""AI CLI - Interactive AI tools using DeepSeek API (Anthropic-compatible endpoint)."""
import os, sys, json, argparse, subprocess
from urllib.request import Request, urlopen
from urllib.error import URLError

API_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic") + "/v1/messages"
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")

def extract_text(result):
    """Extract text from API response, handling thinking blocks."""
    for block in result.get("content", []):
        if block.get("type") == "text":
            return block.get("text", "")
    return "(no text response)"

def chat(prompt, model="deepseek-v4-flash", max_tokens=1024):
    """Send a chat prompt to the DeepSeek API."""
    body = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = Request(API_URL, data=body, headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    })
    try:
        with urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except URLError as e:
        return {"error": str(e)}

def cmd_chat(args):
    """Interactive chat session."""
    print(f"AI Chat (model: {args.model}, /quit to exit)")
    history = []
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in ("/quit", "/exit", "/q"):
            break
        if not user_input:
            continue
        history.append({"role": "user", "content": user_input})
        result = chat(user_input, model=args.model, max_tokens=args.max_tokens)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            text = extract_text(result)
            print(f"\nAI: {text}")
            history.append({"role": "assistant", "content": text})

def cmd_review(args):
    """Review a code file or snippet."""
    if args.file:
        with open(args.file) as f:
            code = f.read()
    elif args.paste:
        code = args.paste
    else:
        code = sys.stdin.read()

    focus = f" Focus on: {args.focus}." if args.focus else ""
    prompt = f"""Review the following code.{focus}

Code:
```{args.language or ''}
{code}
```

Provide a concise code review covering:
1. Bugs or logic errors
2. Security vulnerabilities
3. Performance issues
4. Readability/maintainability suggestions
5. Best practices violations

Be specific - reference line numbers if possible. If the code looks good, say so."""

    print("Reviewing...\n")
    result = chat(prompt, model=args.model, max_tokens=args.max_tokens)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(extract_text(result))

def cmd_summarize(args):
    """Summarize text content."""
    if args.file:
        with open(args.file) as f:
            text = f.read()
    elif args.paste:
        text = args.paste
    else:
        text = sys.stdin.read()

    style = args.style or "concise"
    word_limit = args.words or 200
    prompt = f"Summarize the following text in a {style} style (max {word_limit} words):\n\n{text}"
    result = chat(prompt, model=args.model, max_tokens=args.max_tokens)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(extract_text(result))

def cmd_translate(args):
    """Translate text to a target language."""
    if args.file:
        with open(args.file) as f:
            text = f.read()
    elif args.paste:
        text = args.paste
    else:
        text = sys.stdin.read()

    prompt = f"Translate the following text to {args.target}. Only output the translation, nothing else:\n\n{text}"
    result = chat(prompt, model=args.model, max_tokens=args.max_tokens)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(extract_text(result))

def main():
    parser = argparse.ArgumentParser(description="AI CLI Tools (DeepSeek API)")
    parser.add_argument("--model", default="deepseek-v4-flash", help="Model to use")
    parser.add_argument("--max-tokens", type=int, default=2048, help="Max output tokens")

    sub = parser.add_subparsers(dest="command", help="Commands")

    # Chat
    chat_p = sub.add_parser("chat", help="Interactive chat")
    chat_p.set_defaults(func=cmd_chat)

    # Review
    review_p = sub.add_parser("review", help="Code review")
    review_p.add_argument("--file", help="Code file to review")
    review_p.add_argument("--paste", help="Code snippet to review")
    review_p.add_argument("--focus", help="Specific focus area (security, performance, style)")
    review_p.add_argument("--language", help="Programming language")
    review_p.set_defaults(func=cmd_review)

    # Summarize
    sum_p = sub.add_parser("summarize", help="Summarize text")
    sum_p.add_argument("--file", help="Text file to summarize")
    sum_p.add_argument("--paste", help="Text to summarize")
    sum_p.add_argument("--style", help="Summary style (concise, detailed, bullets)")
    sum_p.add_argument("--words", type=int, help="Max word count")
    sum_p.set_defaults(func=cmd_summarize)

    # Translate
    trans_p = sub.add_parser("translate", help="Translate text")
    trans_p.add_argument("target", help="Target language (e.g. Chinese, French, Japanese)")
    trans_p.add_argument("--file", help="Text file to translate")
    trans_p.add_argument("--paste", help="Text to translate")
    trans_p.set_defaults(func=cmd_translate)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
