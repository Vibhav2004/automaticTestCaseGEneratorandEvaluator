# AutoTestAI – Intelligent Dynamic Test Case Generator

AutoTestAI is an industry-level full-stack application designed to automatically generate, execute, and evaluate test cases for Java and Python code using advanced AST parsing and dynamic analysis.

## 🚀 Features
- **Intelligent Generation**: Uses AST analysis, Boundary Value Analysis (BVA), Equivalence Partitioning (EP), and Fuzzing.
- **Secure Execution**: Subprocess-based sandboxed execution with strict timeouts.
- **Professional Dashboard**: Real-time analytics using React and Recharts with persistent session history.
- **20+ Algorithm Samples**: Built-in Python and Java DSA snippets for benchmarking.
- **Academic Ready**: Full technical project report included for final year submissions.
- **Multi-language Support**: Python and Java parsing.

## 🏗️ Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TailwindCSS
- **Analysis**: `ast` (Python), `javalang` (Java)
- **Charts**: Recharts

---

## 🎓 Academic Justification

### 1. AST-Based Parsing
The system uses Abstract Syntax Trees (AST) to understand the semantic structure of the code. Unlike regex-based solutions, AST parsing allows us to:
- Identify function signatures and parameter types accurately.
- Detect control flow structures (if/else, loops) for path coverage.
- Extract constraints declared in docstrings or type hints.

### 2. Boundary Value Analysis (BVA) & Equivalence Partitioning (EP)
These are fundamental software testing techniques:
- **BVA**: Focuses on the "edges" of input domains (e.g., 0, -1, max_int) where bugs are most likely to occur.
- **EP**: Divides input data into partitions that are expected to be processed similarly, reducing redundant tests.

### 3. Fuzz Testing
Randomized input generation (fuzzing) helps discover unexpected edge cases and security vulnerabilities (like buffer overflows or unhandled exceptions) that manual testing might miss.

### 4. Path Coverage Strategy
By detecting conditionals (if/elif/else), the system attempts to generate inputs that trigger different execution branches, ensuring higher code coverage.

---

## 🛠️ Setup Instructions

### Backend
1. Navigate to `backend/`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
1. Navigate to `frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```

### Samples & Reports
- **Samples**: Located in `samples/python/` and `samples/java/`.
- **Report**: Detailed academic report in `PROJECT_REPORT.md`.

## 🔐 Security
- **Timeouts**: All tests are capped at 5 seconds to prevent infinite loops.
- **Subprocess Isolation**: Tests run in separate processes to avoid crashing the main server.
- **Memory Limits**: (In progress) Resource monitoring via `psutil`.

---

## 📦 Deployment (Docker)
Run the entire stack with:
```bash
docker-compose up --build
```
"# automaticTestCaseGEneratorandEvaluator" 
