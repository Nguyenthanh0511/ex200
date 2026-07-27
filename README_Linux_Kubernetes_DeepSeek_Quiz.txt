RH124 / RH134 / KUBERNETES QUIZ + DEEPSEEK ASK AI
====================================================

PACKAGE CONTENTS
----------------
1. RH124_RH134_Kubernetes_297_Interactive_Quiz_With_DeepSeek_AI.html
2. serve_linux_kubernetes_quiz_with_deepseek.py
3. README_Linux_Kubernetes_DeepSeek_Quiz.txt

QUESTION SET
------------
- Existing RH124/RH134/Mixed Review questions: 267
- Kubernetes Workload questions: 10
- Kubernetes Network questions: 10
- Kubernetes Security questions: 10
- Total: 297

The Kubernetes questions are original practice questions based on official
Kubernetes documentation. They are not copied certification exam questions.

WINDOWS POWERSHELL
------------------
Place all files in the same folder, open PowerShell there, and run:

$env:DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY"
python .\serve_linux_kubernetes_quiz_with_deepseek.py

LINUX / MACOS
-------------
export DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY"
python3 ./serve_linux_kubernetes_quiz_with_deepseek.py

OPTIONAL MODEL
--------------
Windows:
$env:DEEPSEEK_MODEL="YOUR_SUPPORTED_MODEL_NAME"

Linux/macOS:
export DEEPSEEK_MODEL="YOUR_SUPPORTED_MODEL_NAME"

ASK AI BEHAVIOR
---------------
- Before checking an answer, AI is instructed to provide hints without revealing
  the correct option.
- After checking an answer, AI may explain the correct answer and your mistake.
- AI responses default to concise, focused explanations.
- RHEL answers prioritize Red Hat documentation and man pages.
- Kubernetes answers prioritize kubernetes.io official documentation.
- The current question's official reference and source URL are sent to AI.
- The API key is read from DEEPSEEK_API_KEY and is not stored in the HTML.

PROGRESS
--------
The updated website keeps the same browser storage key for questions 1-267,
so existing RH124/RH134 progress should remain available in the same browser.
The new Kubernetes questions use IDs 268-297.
