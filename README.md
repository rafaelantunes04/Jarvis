# APP JARVIS
Personal Assistant Application that focuses on project building and evolving over time, totally local or hosted at home.

### Setup Repository
1. Install Python
2. Clone .env.example as only .env
3. Edit .env and add your username and password as plain text
4. Open terminal
5. `pip install uv`
6. `uv sync`

### Setup Memory
1. Install Docker
2. Open terminal and make sure you're on the base folder
3. `docker compose -f .\misc\docker-compose.yml up -d`

### Setup Local Chatbot
1. Install Ollama
2. Open terminal
3. `ollama pull qwen2.5:3b`

## Setup and Run Aplication
1. Install Rust Programming Language
2. Make sure its up to date
3. Open terminal
4. Run the backend (`uv run dev`)
5. Run the application (`cargo tauri dev`)
