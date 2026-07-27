FULL RH124 / RH134 / KUBERNETES QUIZ
======================================

QUESTION COUNTS
---------------
RH124: 117
RH134: 140
Mixed RH124/RH134: 10
Kubernetes Workload: 72
Kubernetes Network: 54
Kubernetes Security: 54
TOTAL: 447

KUBERNETES BANK
---------------
Total Kubernetes questions: 180
Single-choice: 145
Multiple-select: 35

Difficulty:
Easy: 36
Medium: 90
Hard: 54

Questions include concept recognition, YAML interpretation, and troubleshooting.
The technical basis is current official Kubernetes documentation at kubernetes.io.
These are original practice questions, not leaked or copied certification questions.

RUN
---
Windows:
python .\serve_quiz.py

Linux/macOS:
python3 ./serve_quiz.py

Open:
http://127.0.0.1:8765/

DEEPSEEK
--------
Enter the DeepSeek API key dynamically in Settings.
No static key is required.

PROGRESS
--------
Existing questions keep IDs 1-297.
New Kubernetes questions use IDs 298-447.
Existing browser progress remains compatible.


RUNTIME FIX
-----------
This edition fixes a page-load error where the inline JavaScript executed
before the dynamic Settings/API-key elements existed in the DOM.

Additional safeguards:
- Invalid or legacy browser progress is normalized instead of stopping render.
- Corrupt localStorage data is ignored and removed.
- Existing valid progress remains compatible.


E2E TEST HARDENING
------------------
- Prevented horizontal overflow caused by the closed Settings drawer on mobile.
- Added inline, accessible validation when the learner checks without selecting.
- Feedback and AI status use live regions for clearer user response.
- Tested desktop and 390px mobile layouts using Chromium browser automation.
