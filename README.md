# 🎓 SmartLearn AI

> An intelligent, AI-powered study assistant that helps students learn smarter — upload documents, generate summaries, take quizzes, chat with an AI tutor, and manage notes, all in one place.

---

## ✨ Key Features

- 🤖 **AI Chat Assistant** — Conversational study help powered by DeepSeek via OpenRouter
- 📄 **Document Upload & Extraction** — Upload PDFs and extract their text content automatically
- 📝 **AI Summaries** — Instantly generate concise summaries from uploaded content
- 🧠 **AI Quiz Generator** — Auto-generate quizzes based on your study material
- 🗒️ **Notes Manager** — Create and manage personal study notes
- 📜 **Chat History** — Review your previous AI conversations from your dashboard
- 🔐 **User Authentication** — Secure login and registration system
- 🗄️ **PostgreSQL Database** — Persistent storage for users, notes, chat history, and uploads

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **Database** | PostgreSQL (`psycopg2`) |
| **AI Provider** | OpenRouter API (DeepSeek model) |
| **PDF Processing** | PyPDF2 / pdfminer |
| **Templating** | Jinja2 (Flask templates) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Auth** | Flask Sessions |
| **Config** | python-dotenv |

---

## ✅ Prerequisites

Make sure you have the following installed:

- **Python** 3.9+
- **PostgreSQL** 13+ (running locally or remotely)
- **pip** (Python package manager)
- An **OpenRouter API Key** — get one free at [openrouter.ai](https://openrouter.ai)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/smartlearn-ai.git
cd smartlearn-ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Then open `.env` and update each value (see Environment Variables section below).

### 5. Create the PostgreSQL Database

Open psql or pgAdmin and run:

```sql
CREATE DATABASE "SmartLearn-AI";
```

The app will automatically initialize the required tables on first run.

### 6. Run the Application

```bash
python app.py
```

Open your browser and visit: **http://localhost:5000**

---

## 🔐 Environment Variables

Create a `.env` file in the project root based on `.env.example`:

| Variable | Description | Example |
|---|---|---|
| `OPENROUTER_API_KEY` | Your OpenRouter API key | `sk-or-v1-...` |
| `OPENROUTER_MODEL` | AI model to use | `deepseek/deepseek-chat` |
| `SECRET_KEY` | Flask session secret key | `any-random-secret-string` |
| `UPLOAD_FOLDER` | Folder for uploaded files | `static/uploads` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_NAME` | PostgreSQL database name | `SmartLearn-AI` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `your_password` |
| `DB_PORT` | PostgreSQL port | `5432` |

---

## 📁 Project Structure

```
SmartLearn AI Project/
│
├── app.py                  # Application entry point & Flask config
├── config.py               # Base configuration class
├── requirements.txt        # Python dependencies
├── .env                    # Local environment variables (not committed)
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
│
├── routes/                 # Flask Blueprints (one per feature)
│   ├── auth_routes.py      # Login, Register, Logout
│   ├── main_routes.py      # Home, About, Features, Contact
│   ├── chat_routes.py      # AI Chat interface
│   ├── upload_routes.py    # File upload & text extraction
│   ├── summary_routes.py   # AI summary generation
│   ├── quiz_routes.py      # AI quiz generation
│   └── notes_routes.py     # Notes CRUD
│
├── utils/                  # Helper utilities
│   ├── ai_handler.py       # OpenRouter API integration
│   ├── db.py               # Database connection & initialization
│   ├── helpers.py          # Shared helper functions
│   └── pdf_extractor.py    # PDF text extraction
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base layout template
│   ├── index.html          # Landing page
│   ├── auth/               # Login & Register pages
│   └── dashboard/          # Protected dashboard pages
│       ├── dashboard.html
│       ├── chat.html
│       ├── upload.html
│       ├── summary.html
│       ├── quiz.html
│       ├── notes.html
│       └── history.html
│
└── static/                 # Static assets (CSS, JS, images, uploads)
    └── uploads/            # User-uploaded files (auto-created)
```

---

## 🌐 Application Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Landing page |
| `GET` | `/auth/login` | Login page |
| `POST` | `/auth/login` | Handle login |
| `GET` | `/auth/register` | Register page |
| `POST` | `/auth/register` | Handle registration |
| `GET` | `/auth/logout` | Log out |
| `GET/POST` | `/chat/` | AI Chat interface |
| `GET/POST` | `/upload/` | Upload documents |
| `GET/POST` | `/summary/` | Generate AI summary |
| `GET/POST` | `/quiz/` | Generate AI quiz |
| `GET/POST` | `/notes/` | Manage notes |

---

## 🤖 AI Integration

SmartLearn AI uses **OpenRouter** as the AI gateway, which lets you swap models easily. The default model is `deepseek/deepseek-chat`.

To change the AI model, update `OPENROUTER_MODEL` in your `.env` file. Supported models include:

- `deepseek/deepseek-chat` (default)
- `openai/gpt-4o`
- `anthropic/claude-3.5-sonnet`
- `meta-llama/llama-3.1-70b-instruct`

Browse all available models at [openrouter.ai/models](https://openrouter.ai/models).

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| `OPENROUTER_API_KEY is not set` | Make sure `.env` exists and the key is set |
| Database connection error | Ensure PostgreSQL is running and credentials in `.env` are correct |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your virtual environment |
| Upload not working | Ensure `static/uploads/` exists (auto-created on startup) |
| Port 5000 in use | Kill the process or change port in `app.py` |

---

