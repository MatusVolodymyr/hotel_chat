# Hotel Chat Application

A LangChain-based hotel room search and chat application with vector similarity search, logging, and a Streamlit web interface.

## Features

- 🏨 Semantic hotel room search using vector embeddings
- 🤖 LangChain-powered chat agent (Traditional & LCEL)
- 🔍 PostgreSQL with pgvector for similarity search
- 📊 Comprehensive logging system
- 🌐 **Streamlit web interface**
- 🔧 Configurable environment settings
- 💬 Interactive chat with conversation memory

### Configuration

Logging can be configured through environment variables:

```bash
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log file path (auto-rotated)
LOG_FILE=logs/hotel_chat.log

# Enable/disable console logging
LOG_CONSOLE=true

# Enable/disable file logging
LOG_FILE_ENABLE=true
```

### Usage

```python
from app.core.logger import get_logger

logger = get_logger(__name__)

logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")
logger.debug("This is debug info")
```

### Log Output Example

```
14:32:15 | INFO | hotel_agent.run:45 | Processing user input: looking for luxury hotel...
14:32:15 | DEBUG | vector_search.search_similar_rooms:23 | Generating query embedding
14:32:16 | DEBUG | embedding.embed_text:28 | Embedding generated with dimension: 384
14:32:16 | INFO | vector_search.search_similar_rooms:48 | Found 3 matching rooms
14:32:17 | INFO | hotel_agent.run:48 | Agent response generated successfully (length: 245)
```

## Quick Start

### Option 1: Streamlit Web Interface (Recommended)

1. **Setup environment:**
   ```bash
   cd /root/ai_projects/hotel_chat
   cp .env.example .env
   # Edit .env with your OpenAI API key and database settings
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database and load data:**
   ```bash
   # Set up PostgreSQL with pgvector extension
   python scripts/load_rooms.py
   ```

4. **Launch Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   # Or use the convenience script:
   ./run_streamlit.sh
   ```

5. **Open browser:** Navigate to `http://localhost:8501`

### Option 2: Command Line Interface

Run the terminal-based chat interface:
```bash
python main.py
```

## Web Interface Features

The Streamlit interface provides:

- **💬 Interactive Chat**: Сhat interface with message history
- **🔧 Live Configuration**: View current settings and model info
- **🔄 Memory Management**: Reset conversation or clear chat history
- **❓ Built-in Help**: Example queries and feature documentation

### Interface Controls

- **Reset Conversation**: Clear agent memory while keeping chat visible
- **Clear Chat**: Remove all messages from the interface
- **Help & Examples**: Expandable section with sample queries

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd /root/hotel_chat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Set up PostgreSQL with pgvector:**
   ```sql
   CREATE DATABASE hotel_db;
   \c hotel_db;
   CREATE EXTENSION vector;
   ```

5. **Load sample data:**
   ```bash
   python scripts/load_rooms.py
   ```

6. **Run the application:**
   ```bash
   python main.py
   ```

This will:
- Test all log levels
- Verify file and console output
- Test structured logging
- Check exception handling
- Validate module imports

## Project Structure

```
hotel_chat/
├── app/
│   ├── __init__.py              # Package initialization with logging
│   ├── core/
│   │   ├── config.py            # Configuration management
│   │   └── logger.py            # Logging system 
│   ├── agent/
│   │   ├── lcel_agent.py        # LCEL agent with logging
│   │   └── tools/
│   │       └── search_for_rooms.py  # Search tool with logging
│   ├── services/
│   │   ├── embedding.py         # Embedding service with logging
│   │   ├── vector_search.py     # Vector search with logging
│   │   └── retrieval.py
│   ├── models/
│   │   ├── room.py              # Room model
│   │   └── base.py
│   ├── db/
│   │   └── session.py           # Database session with logging
│   └── schemas/
├── scripts/
│   └── load_rooms.py            # Data loading script with logging
├── logs/                        # Log files (auto-created)
├── main.py                      # CLI application 
├── streamlit_app.py             # Streamlit web interface 
├── run_streamlit.sh             # Streamlit launcher script 
├── test_logging.py              # Logging test script 
├── .env.example                 # Environment template 
├── .gitignore                   # Git ignore file 
├── requirements.txt             # Dependencies (with Streamlit) 
└── README.md                    # This file 
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+psycopg2://postgres:postgres@localhost/hotel_db` | PostgreSQL connection string |
| `OPENAI_API_KEY` | None | OpenAI API key (required) |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_FILE` | `logs/hotel_chat.log` | Log file path |
| `LOG_CONSOLE` | `true` | Enable console logging |
| `LOG_FILE_ENABLE` | `true` | Enable file logging |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Embedding model |
| `LLM_MODEL` | `gpt-4` | LLM model for chat |
| `LLM_TEMPERATURE` | `0` | LLM temperature |
| `VECTOR_SEARCH_K` | `5` | Number of search results |
| `AGENT_MODEL` | `gpt-4` | Agent model |
| `AGENT_VERBOSE` | `false` | Agent verbose mode |

## Running the Application

### 🌐 Streamlit Web Interface (Recommended)

The Streamlit interface provides the best user experience with:

```bash
# Quick start
streamlit run streamlit_app.py

# Or with custom configuration
./run_streamlit.sh
```

**Features:**
- Interactive chat interface
- Configuration dashboard
- Mobile-friendly design

### 💻 Command Line Interface

For terminal-based interaction:

```bash
python main.py
```

**Features:**
- Direct terminal chat
- Logging output visible
- Keyboard shortcuts (Ctrl+C to quit)
- Memory reset command

### 🧪 Testing

Test the logging system and imports:

```bash
python test_logging.py
```

## Example Queries

Try these sample queries in either interface:

- "I need a luxury hotel in Kyiv with spa access"
- "Show me budget accommodation under $50"
- "Find family apartments with kitchen in Dnipro"  
- "Beach hotels in Odesa with sea view and balcony"
- "Pet-friendly places with parking"
- "Eco-friendly cabins in the mountains"
- "Business hotels with conference facilities"

## Logging Modules

The following modules now include comprehensive logging:

- **`app.core.logger`** - Logging configuration and utilities
- **`app.agent.lcel_agent`** - agent building and execution
- **`app.agent.tools.search_for_rooms`** - Room search tool operations
- **`app.services.embedding`** - Text embedding generation
- **`app.services.vector_search`** - Vector similarity search
- **`app.db.session`** - Database session management
- **`scripts.load_rooms`** - Data loading operations

## Log Levels Used

- **DEBUG**: Detailed information for debugging (embeddings, SQL queries, etc.)
- **INFO**: General application flow and successful operations
- **WARNING**: Deprecation warnings and recoverable issues
- **ERROR**: Errors that don't stop the application
- **CRITICAL**: Severe errors that may cause application failure

## Log File Rotation

Log files are automatically rotated when they reach 10MB, with up to 5 backup files kept. Old log files are automatically cleaned up.

## Troubleshooting

### Streamlit Issues

**App won't start:**
- Check that Streamlit is installed: `pip install streamlit`
- Verify your Python environment
- Ensure port 8501 is available

**"OpenAI API key not configured" error:**
- Set your API key in `.env`: `OPENAI_API_KEY=your_key_here`
- Or export as environment variable: `export OPENAI_API_KEY=your_key`

**Database connection errors:**
- Verify PostgreSQL is running
- Check database URL in `.env`
- Ensure pgvector extension is installed

**Agent initialization fails:**
- Check internet connection for model downloads
- Verify OpenAI API key is valid
- Check logs for detailed error information

### General Issues

If you encounter logging issues:

1. Check file permissions for the `logs/` directory
2. Verify environment variables are set correctly
3. Run `python test_logging.py` to diagnose issues
4. Check console output for immediate feedback

## To do

- [ ] Add authentication for API endpoints
- [ ] Improve promts
- [ ] Rethink the structure of models to improve retrival
- [ ] Improve retrival functionality