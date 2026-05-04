#!/usr/bin/env python3
"""
Local AI Toolset — leverage local Ollama models for Claude Code assistance.

Commands:
  local-ai search <query>    — Semantic code search using embeddings
  local-ai review [--diff <file>] [--staged]  — Code review using local model
  local-ai vision <image>    — Analyze image/screenshot
  local-ai chat <prompt>     — General chat with local model
  local-ai status             — Show available models and GPU status
  local-ai embed <text>       — Generate embedding vector (for RAG pipeline)
  local-ai index [--rebuild]  — Build/rebuild codebase embedding index
"""

import subprocess
import sys
import os
import json
import argparse
from pathlib import Path

# Config
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
EMBED_MODEL = "nomic-embed-text"
CODE_MODEL = "qwen2.5-coder:14b"
HEAVY_MODEL = "qwen2.5:32b"
VISION_MODEL = "minicpm-v:8b"
INDEX_DIR = Path.home() / ".local-ai" / "index"


def run_ollama(model, prompt, **kwargs):
    """Run an Ollama model and return the response."""
    import urllib.request

    body = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    body.update(kwargs)

    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/generate",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read())
            return data.get("response", "")
    except Exception as e:
        return f"[ERROR] {e}"


def run_ollama_embed(model, texts):
    """Generate embeddings for texts."""
    import urllib.request

    if isinstance(texts, str):
        texts = [texts]

    body = {
        "model": model,
        "input": texts,
    }

    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/embed",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
            return data.get("embeddings", [])
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return []


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)


def cmd_status():
    """Show available models and system status."""
    import urllib.request

    print("=" * 50)
    print("Local AI Status")
    print("=" * 50)

    # GPU status
    nvidia_smi = "/usr/lib/wsl/lib/nvidia-smi"
    if os.path.exists(nvidia_smi):
        result = subprocess.run([nvidia_smi, "--query-gpu=name,memory.used,memory.total", "--format=csv,noheader"],
                              capture_output=True, text=True)
        print(f"\nGPU: {result.stdout.strip()}")

    # Models
    print("\nInstalled Models:")
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    print(result.stdout)

    # Disk usage
    models_dir = Path("/root/models/gguf")
    if models_dir.exists():
        total = sum(f.stat().st_size for f in models_dir.glob("*.gguf"))
        print(f"GGUF models: {total / 1e9:.1f} GB on disk")

    # Endpoints
    print(f"\nAPI: {OLLAMA_HOST}")
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            tags = json.loads(resp.read())
            print(f"Connected: {len(tags.get('models', []))} models available")
    except Exception as e:
        print(f"Connection: FAILED — {e}")


def cmd_embed(text):
    """Generate embedding for text."""
    embeddings = run_ollama_embed(EMBED_MODEL, text)
    if embeddings:
        emb = embeddings[0]
        print(f"Dimension: {len(emb)}")
        print(f"First 10: {emb[:10]}")
        print(f"Norm: {sum(x*x for x in emb)**0.5:.4f}")
    else:
        print("Embedding failed. Is the model loaded?")


def cmd_search(query):
    """Semantic code search using embeddings."""
    import urllib.request

    # Generate query embedding
    print(f"Searching: '{query}'", file=sys.stderr)
    query_embs = run_ollama_embed(EMBED_MODEL, query)
    if not query_embs:
        print("Failed to embed query", file=sys.stderr)
        sys.exit(1)

    query_emb = query_embs[0]

    # Quick grep for candidate files (fallback hybrid search)
    words = [w for w in query.split() if len(w) > 2]
    candidates = set()
    search_dirs = [os.getcwd()]

    for word in words[:5]:
        try:
            result = subprocess.run(
                ["grep", "-rl", "--include=*.py", "--include=*.js", "--include=*.ts",
                 "--include=*.md", "--include=*.json", "--include=*.go",
                 "--include=*.rs", "--include=*.java", "--include=*.sh",
                 word, "."],
                capture_output=True, text=True, timeout=10, cwd=search_dirs[0]
            )
            for line in result.stdout.strip().split("\n"):
                if line:
                    candidates.add(line)
        except subprocess.TimeoutExpired:
            pass

    if not candidates:
        print("No candidate files found by keyword search.")
        return

    # Read candidate files and compute similarity
    results = []
    for filepath in list(candidates)[:50]:  # Limit candidates
        try:
            with open(filepath, "r", errors="ignore") as f:
                content = f.read(10000)  # First 10KB
        except Exception:
            continue

        # Simple chunking: split by function/class boundaries
        lines = content.split("\n")
        for i in range(0, len(lines), 30):
            chunk = "\n".join(lines[i:i + 30])
            if len(chunk.strip()) < 50:
                continue
            embs = run_ollama_embed(EMBED_MODEL, chunk)
            if embs:
                sim = cosine_similarity(query_emb, embs[0])
                results.append((sim, filepath, i + 1, chunk[:200]))

    # Sort by similarity and display top results
    results.sort(key=lambda x: x[0], reverse=True)

    print(f"\nTop {min(10, len(results))} results:\n")
    for i, (sim, filepath, line_num, snippet) in enumerate(results[:10]):
        print(f"{i+1}. [{sim:.3f}] {filepath}:{line_num}")
        preview = snippet.replace("\n", " ")[:120]
        print(f"   {preview}...")
        print()


def cmd_review(diff_file=None, staged=False):
    """Review code changes using local model."""
    if staged:
        result = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)
        diff = result.stdout
    elif diff_file:
        with open(diff_file) as f:
            diff = f.read()
    else:
        result = subprocess.run(["git", "diff"], capture_output=True, text=True)
        diff = result.stdout

    if not diff.strip():
        print("No changes to review.")
        return

    # Truncate if too large
    if len(diff) > 20000:
        diff = diff[:20000] + "\n... (truncated)"

    prompt = f"""You are a senior code reviewer. Analyze the following git diff and identify:

1. Bugs or logic errors
2. Security vulnerabilities
3. Performance issues
4. Code style or readability concerns

Be specific — reference exact lines. If there are no issues, say so clearly.

```diff
{diff}
```

Code Review:"""

    print("Reviewing changes...", file=sys.stderr)
    print(f"Model: {CODE_MODEL}", file=sys.stderr)
    response = run_ollama(CODE_MODEL, prompt)
    print(response)


def cmd_vision(image_path):
    """Analyze an image using vision model."""
    if not os.path.exists(image_path):
        print(f"File not found: {image_path}")
        sys.exit(1)

    print(f"Analyzing: {image_path}", file=sys.stderr)
    print(f"Model: {VISION_MODEL}", file=sys.stderr)

    # For Ollama vision, we need to use the chat API with images
    import urllib.request
    import base64

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    body = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": "Describe this image in detail. What do you see? If it's a screenshot of code, UI, or an error message, analyze it.",
                "images": [image_data],
            }
        ],
        "stream": False,
    }

    try:
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/chat",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            print(data.get("message", {}).get("content", "No response"))
    except Exception as e:
        print(f"[ERROR] {e}")


def cmd_chat(prompt):
    """General chat with heavy model."""
    print(f"Model: {HEAVY_MODEL}", file=sys.stderr)
    response = run_ollama(HEAVY_MODEL, prompt)
    print(response)


def cmd_index(rebuild=False):
    """Build a codebase embedding index for fast search."""
    import pickle

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_file = INDEX_DIR / "code_index.pkl"

    if index_file.exists() and not rebuild:
        print(f"Index exists at {index_file}. Use --rebuild to reindex.")
        return

    print(f"Building code index from {os.getcwd()}...", file=sys.stderr)

    # Find code files
    extensions = [".py", ".js", ".ts", ".go", ".rs", ".java", ".sh", ".md", ".json"]
    files = []
    for ext in extensions:
        result = subprocess.run(
            ["find", ".", "-name", f"*{ext}", "-not", "-path", "*/node_modules/*",
             "-not", "-path", "*/.git/*", "-not", "-path", "*/__pycache__/*",
             "-not", "-path", "*/vendor/*", "-not", "-path", "*/target/*"],
            capture_output=True, text=True,
        )
        files.extend([f.strip() for f in result.stdout.split("\n") if f.strip()])

    print(f"Found {len(files)} files to index.", file=sys.stderr)

    # Index files in chunks
    index = {}
    batch_size = 20

    for i in range(0, len(files), batch_size):
        batch = files[i : i + batch_size]
        batch_texts = []

        for fp in batch:
            try:
                with open(fp, "r", errors="ignore") as f:
                    content = f.read(8000)  # First 8KB
                # Chunk at function/class level
                lines = content.split("\n")
                for j in range(0, len(lines), 40):
                    chunk = "\n".join(lines[j : j + 40])
                    if len(chunk.strip()) > 100:
                        batch_texts.append((fp, j + 1, chunk))
            except Exception:
                pass

        if batch_texts:
            texts = [t[2] for t in batch_texts]
            embs = run_ollama_embed(EMBED_MODEL, texts)
            for (fp, line, text), emb in zip(batch_texts, embs):
                key = f"{fp}:{line}"
                index[key] = {
                    "file": fp,
                    "line": line,
                    "snippet": text[:200],
                    "embedding": emb,
                }

        print(f"\r  Indexed {min(i + batch_size, len(files))}/{len(files)} files", end="", flush=True, file=sys.stderr)

    print(f"\nSaving index ({len(index)} chunks)...", file=sys.stderr)
    with open(index_file, "wb") as f:
        pickle.dump(index, f)

    size_mb = os.path.getsize(index_file) / 1e6
    print(f"Index saved: {index_file} ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Local AI Toolset")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show model and system status")

    p = sub.add_parser("embed", help="Generate embedding for text")
    p.add_argument("text", help="Text to embed")

    p = sub.add_parser("search", help="Semantic code search")
    p.add_argument("query", help="Search query")

    p = sub.add_parser("review", help="Review code changes")
    p.add_argument("--diff", help="Diff file to review")
    p.add_argument("--staged", action="store_true", help="Review staged changes")

    p = sub.add_parser("vision", help="Analyze image/screenshot")
    p.add_argument("image", help="Path to image file")

    p = sub.add_parser("chat", help="General chat with local model")
    p.add_argument("prompt", help="Chat prompt")

    p = sub.add_parser("index", help="Build codebase embedding index")
    p.add_argument("--rebuild", action="store_true", help="Force rebuild")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "embed":
        cmd_embed(args.text)
    elif args.command == "search":
        cmd_search(args.query)
    elif args.command == "review":
        cmd_review(diff_file=args.diff, staged=args.staged)
    elif args.command == "vision":
        cmd_vision(args.image)
    elif args.command == "chat":
        cmd_chat(args.prompt)
    elif args.command == "index":
        cmd_index(rebuild=args.rebuild)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
