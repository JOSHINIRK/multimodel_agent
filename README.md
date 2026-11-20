# Multimodal AI Agent

A Streamlit app that answers questions about an image. Upload a picture, type a question, and a vision-capable model served by [Groq](https://groq.com/) analyzes the image and replies. Every question and answer is logged to a CSV file.

## Features

- Upload PNG, JPG, JPEG or WEBP images and preview them in the browser
- Ask any free-text question about the image (e.g. "Explain this dashboard", "What document is this?")
- Answers come from a multimodal model via the Groq chat completions API
- Each run is appended to `logs/output_logs.csv` with a timestamp, image name, prompt and response

## Project structure

```
multimodal-agent/
├── agent.py           # Groq client and analyze_image(image, prompt)
├── app.py             # Streamlit UI and CSV logging
├── requirements.txt   # Python dependencies
├── .env.example       # Template for environment variables
└── logs/              # Created at runtime; output_logs.csv (gitignored)
```

## How it works

1. `app.py` takes the uploaded image and the user's question.
2. `agent.py` converts the image to RGB, encodes it as a base64 JPEG data URL, and sends it with the question to the model (`MODEL_NAME` in `agent.py`), together with a system prompt that tells the model not to invent information.
3. The model's answer is shown in the app and appended to `logs/output_logs.csv`.

## Setup

Requires Python 3.9+ and a Groq API key.

```bash
git clone https://github.com/JOSHINIRK/multimodel_agent.git
cd multimodel_agent

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create your `.env` from the template and add your key:

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run

```bash
streamlit run app.py
```

Then open http://localhost:8501, upload an image, enter a question and click **Analyze Image**.

## Configuration

| Setting | Where | Description |
|---|---|---|
| `GROQ_API_KEY` | `.env` | Required. The app raises an error at startup if it is missing. |
| `MODEL_NAME` | `agent.py` | The Groq model used for image analysis. Change it to any vision-capable model available on your Groq account. |
| `max_completion_tokens` | `agent.py` | Maximum length of the answer (default 1024). |

## Logs

Each successful analysis adds a row to `logs/output_logs.csv`:

| Column | Description |
|---|---|
| `timestamp` | ISO time of the request |
| `image_name` | Uploaded file name |
| `prompt` | The question asked |
| `response` | The model's answer |

The `logs/` folder and `.env` are excluded from git.
