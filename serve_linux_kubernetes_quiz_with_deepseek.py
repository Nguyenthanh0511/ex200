#!/usr/bin/env python3
"""
Local server for the RH124, RH134, and Kubernetes quiz with DeepSeek Ask AI.

Security:
- The DeepSeek API key is read from DEEPSEEK_API_KEY.
- The key is never embedded in the HTML file.
- The server binds to 127.0.0.1 by default.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser

HOST = os.environ.get("QUIZ_HOST", "127.0.0.1")
PORT = int(os.environ.get("QUIZ_PORT", "8765"))
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
API_URL = "https://api.deepseek.com/chat/completions"
QUIZ_FILE = "RH124_RH134_Kubernetes_297_Interactive_Quiz_With_DeepSeek_AI.html"

SYSTEM_PROMPT = """You are a precise technical tutor for:
- RH124 and RH134 on Red Hat Enterprise Linux 10.
- Kubernetes Workload, Network, and Security.

RESPONSE STYLE
- Answer briefly, clearly, and directly.
- Default to about 60-140 words unless the learner requests more detail.
- Do not repeat the question or add an introduction.
- Prefer: Answer, Why, and Source.
- Include a command, YAML fragment, or verification step only when it is useful.

SOURCE POLICY
- Every technical claim must be based on an authoritative source.
- For RHEL topics, prioritize Red Hat documentation and installed manual pages.
- For Kubernetes topics, prioritize kubernetes.io official documentation.
- Then use official upstream documentation such as GNU, systemd, OpenSSH, Podman, NetworkManager, CNCF, or Linux Foundation.
- Do not rely on random blogs, forums, Reddit, or unverified tutorials.
- The quiz CONTEXT provides a reference and source URL. Treat these as the primary reference for the current question.
- Do not claim that you opened or verified a URL unless its contents were actually supplied to you.
- Never invent commands, options, paths, configuration fields, citations, URLs, course wording, or exam questions.
- If you cannot verify a claim confidently from the supplied authoritative context or well-established official documentation, say: "I cannot verify this confidently from an authoritative source."

QUIZ BEHAVIOR
- Respect CONTEXT.checked.
- If CONTEXT.checked is false:
  - Do not reveal the correct option letter.
  - Do not quote the exact correct option as the answer.
  - Give a concise conceptual hint that helps the learner reason independently.
- If CONTEXT.checked is true:
  - You may explain the correct answer.
  - Explain briefly why the learner was correct or incorrect.
  - Explain distractors only when asked or when essential.

TECHNICAL APPROACH
- Distinguish runtime configuration from persistent configuration.
- For troubleshooting, use: observe, inspect state/logs, identify cause, apply the smallest correct fix, verify.
- Do not recommend disabling SELinux, firewalld, RBAC, or security controls as a normal first fix.
- For Kubernetes, distinguish desired state from observed state and use official resource semantics.

LANGUAGE
- Respond in the language selected by the learner.
- In Vietnamese responses, preserve commands, YAML fields, file paths, resource names, and official technical terms in English.

End technical answers with one concise source line using the CONTEXT reference or source URL.
"""

class QuizHandler(SimpleHTTPRequestHandler):
    server_version = "LinuxKubernetesQuizDeepSeek/2.0"

    def _json(self, status: int, payload: dict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self) -> None:
        if self.path != "/api/deepseek":
            self._json(404, {"error": "Not found"})
            return

        api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
        if not api_key:
            self._json(
                500,
                {"error": "DEEPSEEK_API_KEY is not set. Stop the server, set the environment variable, and start it again."},
            )
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 1_000_000:
                raise ValueError("Invalid request size")
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            self._json(400, {"error": f"Invalid request: {exc}"})
            return

        language = incoming.get("language", "English")
        context = incoming.get("context", {})
        history = incoming.get("history", [])
        if not isinstance(context, dict) or not isinstance(history, list):
            self._json(400, {"error": "Invalid context or history"})
            return

        clean_history = []
        for item in history[-10:]:
            if not isinstance(item, dict):
                continue
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
                clean_history.append({"role": role, "content": content[:12000]})

        context_message = (
            f"Answer language requested: {language}\n\n"
            "CURRENT QUIZ CONTEXT:\n"
            + json.dumps(context, ensure_ascii=False, indent=2)
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": context_message},
            *clean_history,
        ]

        body = json.dumps(
            {
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "temperature": 0.1,
                "max_tokens": 750,
            },
            ensure_ascii=False,
        ).encode("utf-8")

        req = urllib.request.Request(
            API_URL,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "RH124-RH134-Kubernetes-Quiz/2.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
            answer = result["choices"][0]["message"]["content"]
            self._json(200, {"answer": answer, "model": result.get("model", MODEL)})
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(detail)
                detail = parsed.get("error", {}).get("message") or detail
            except json.JSONDecodeError:
                pass
            self._json(exc.code, {"error": f"DeepSeek API: {detail[:1200]}"})
        except urllib.error.URLError as exc:
            self._json(502, {"error": f"Could not reach DeepSeek API: {exc.reason}"})
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            self._json(502, {"error": f"Unexpected DeepSeek response: {exc}"})
        except Exception as exc:
            self._json(500, {"error": f"Server error: {exc}"})

def main() -> None:
    root = Path(__file__).resolve().parent
    os.chdir(root)

    quiz = root / QUIZ_FILE
    if not quiz.exists():
        print(f"ERROR: Missing {QUIZ_FILE}", file=sys.stderr)
        sys.exit(1)

    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("WARNING: DEEPSEEK_API_KEY is not set. The quiz will open, but Ask AI will return an error.")

    url = f"http://{HOST}:{PORT}/{QUIZ_FILE}"
    httpd = ThreadingHTTPServer((HOST, PORT), QuizHandler)

    print("=" * 72)
    print("RH124 / RH134 / Kubernetes Quiz + DeepSeek Ask AI")
    print(f"Model : {MODEL}")
    print(f"Open  : {url}")
    print("Stop  : Ctrl+C")
    print("=" * 72)

    try:
        webbrowser.open(url)
    except Exception:
        pass

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        httpd.server_close()

if __name__ == "__main__":
    main()
