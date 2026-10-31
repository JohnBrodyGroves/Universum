## Universum

## Getting started (Windows)

You need Python 3.14, Node.js 22 or newer, and Git.

First time only:

```powershell
cd backend
py -V:3.14 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
cd ..\frontend
npm install
cd ..
```

Start Universum:

```powershell
.\run.ps1
```

Then open http://127.0.0.1:8000.

Run the backend tests: `cd backend` then `.venv\Scripts\python -m pytest`
