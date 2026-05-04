#!/usr/bin/env python3
"""Lightweight AI webhook server using stdlib only. Provides webhook endpoints for AI Chat, Code Review, and Summarization."""
import os, sys, json, time, logging, hashlib, hmac
from urllib.request import Request, urlopen
from urllib.error import URLError
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

API_URL = os.environ.get("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic") + "/v1/messages"
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
HOST = os.environ.get("AI_SERVER_HOST", "0.0.0.0")
PORT = int(os.environ.get("AI_SERVER_PORT", "8899"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ai-webhook")

def call_deepseek(prompt, model="deepseek-v4-flash", max_tokens=2048):
    """Call the DeepSeek API."""
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
        with urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except URLError as e:
        return {"error": str(e)}

def extract_text(result):
    """Extract text content from API response."""
    for block in result.get("content", []):
        if block.get("type") == "text":
            return block.get("text", "")
    return ""

class AIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info("%s %s", self.address_string(), format % args)

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_POST(self):
        path = self.path.rstrip("/")
        try:
            body = self._read_body()
        except json.JSONDecodeError:
            return self._send_json({"error": "Invalid JSON"}, 400)

        if path == "/chat":
            self._handle_chat(body)
        elif path == "/review":
            self._handle_review(body)
        elif path == "/summarize":
            self._handle_summarize(body)
        elif path == "/translate":
            self._handle_translate(body)
        elif path == "/health":
            self._send_json({"status": "ok", "timestamp": datetime.now().isoformat()})
        elif path == "/help":
            self._send_json({
                "endpoints": {
                    "/chat": "POST {\"prompt\": \"...\"} - AI chat completion",
                    "/review": "POST {\"code\": \"...\", \"language\": \"py\", \"focus\": \"security\"} - Code review",
                    "/summarize": "POST {\"text\": \"...\", \"style\": \"concise\", \"words\": 100} - Text summarization",
                    "/translate": "POST {\"text\": \"...\", \"target\": \"Chinese\"} - Translation",
                    "/health": "GET/POST - Health check"
                }
            })
        else:
            self._send_json({"error": f"Unknown endpoint: {path}", "hint": "See /help for available endpoints"}, 404)

    def do_GET(self):
        if self.path.rstrip("/") in ("/health", "/"):
            self._send_json({"status": "ok", "timestamp": datetime.now().isoformat()})
        else:
            self._send_json({"error": "Use POST method. See /help for endpoints."}, 405)

    def _handle_chat(self, body):
        prompt = body.get("prompt", "")
        if not prompt:
            return self._send_json({"error": "Missing 'prompt' field"}, 400)
        model = body.get("model", "deepseek-v4-flash")
        max_tokens = body.get("max_tokens", 2048)
        logger.info("CHAT [%s] %s", model, prompt[:80])
        result = call_deepseek(prompt, model=model, max_tokens=max_tokens)
        if "error" in result:
            return self._send_json({"error": result["error"]}, 500)
        self._send_json({
            "reply": extract_text(result),
            "model": result.get("model"),
            "usage": result.get("usage", {})
        })

    def _handle_review(self, body):
        code = body.get("code", "")
        if not code:
            return self._send_json({"error": "Missing 'code' field"}, 400)
        language = body.get("language", "")
        focus = body.get("focus", "")
        focus_line = f" Focus on: {focus}." if focus else ""
        prompt = f"""Review the following code.{focus_line}

Code:
```{language}
{code}
```

Provide a concise code review covering bugs, security, performance, and best practices. Be specific."""
        logger.info("REVIEW [%s] %d chars", language or "?", len(code))
        result = call_deepseek(prompt, max_tokens=2048)
        if "error" in result:
            return self._send_json({"error": result["error"]}, 500)
        self._send_json({
            "review": extract_text(result),
            "language": language,
            "model": result.get("model"),
            "usage": result.get("usage", {})
        })

    def _handle_summarize(self, body):
        text = body.get("text", "")
        if not text:
            return self._send_json({"error": "Missing 'text' field"}, 400)
        style = body.get("style", "concise")
        words = body.get("words", 200)
        prompt = f"Summarize the following text in a {style} style (max {words} words):\n\n{text}"
        logger.info("SUMMARIZE %d chars, style=%s", len(text), style)
        result = call_deepseek(prompt, max_tokens=1024)
        if "error" in result:
            return self._send_json({"error": result["error"]}, 500)
        self._send_json({
            "summary": extract_text(result),
            "style": style,
            "model": result.get("model"),
            "usage": result.get("usage", {})
        })

    def _handle_translate(self, body):
        text = body.get("text", "")
        target = body.get("target", "Chinese")
        if not text:
            return self._send_json({"error": "Missing 'text' field"}, 400)
        prompt = f"Translate the following text to {target}. Only output the translation, nothing else:\n\n{text}"
        logger.info("TRANSLATE to %s, %d chars", target, len(text))
        result = call_deepseek(prompt, max_tokens=2048)
        if "error" in result:
            return self._send_json({"error": result["error"]}, 500)
        self._send_json({
            "translation": extract_text(result),
            "target": target,
            "model": result.get("model"),
            "usage": result.get("usage", {})
        })

def main():
    if not API_KEY:
        logger.error("ANTHROPIC_AUTH_TOKEN not set. Source ~/.bashrc first.")
        sys.exit(1)
    server = HTTPServer((HOST, PORT), AIHandler)
    logger.info("AI Webhook Server starting on %s:%d", HOST, PORT)
    logger.info("Endpoints: /chat /review /summarize /translate /health /help")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        server.shutdown()

if __name__ == "__main__":
    main()
