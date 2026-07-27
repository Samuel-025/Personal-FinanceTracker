# Contributing to Personal Finance Tracker V2

Thank you for your interest in contributing to Personal Finance Tracker!

## 🚀 Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork locally**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Personal-FinanceTracker.git
   cd Personal-FinanceTracker
   ```
3. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # or .\.venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

## 🧪 Running Tests & Verification

Before opening a pull request, please verify that core imports and REST API endpoints execute cleanly:

```bash
python -c "
from fastapi.testclient import TestClient
from database import init_db
from server import app
import main, models, database, data_entry

init_db()
with TestClient(app) as client:
    assert client.get('/api/categories').status_code == 200
    assert client.get('/api/transactions').status_code == 200
    assert client.get('/api/export/csv').status_code == 200
    assert client.get('/api/export/excel').status_code == 200
    assert client.get('/api/export/pdf').status_code == 200
    print('All automated API tests passed!')
"
```

## 📝 Pull Request Guidelines

- Ensure your code follows PEP 8 standards.
- Keep commits concise and descriptive.
- Make sure existing web dashboard and CLI functionalities remain intact.
