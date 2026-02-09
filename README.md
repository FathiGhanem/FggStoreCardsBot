# 🎮 FGGSTORE Card Generator Bot

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-20.6-blue)](https://python-telegram-bot.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen)](https://www.docker.com/)

A professional, open-source Telegram bot for automatically generating customized PlayStation Store card images with proper Arabic text support.

**⭐ Star this repo if you find it helpful! Contributions are welcome!**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Deployment](#-deployment) • [Architecture](#-architecture)

</div>

---

## ✨ Features

- 🎯 **Interactive Workflow** - Guided conversation flow for card creation
- 💳 **Multiple Card Values** - Support for $10, $20, $25, $50, and $100 cards
- 🌍 **Multi-Region** - USA, KSA (Saudi Arabia), and UAE region support
- 🔐 **Auto-Format Codes** - Automatic formatting of activation codes (XXXX-XXXX-XXXX)
- 📝 **Arabic Support** - Proper Arabic text rendering with BiDi support
- 👤 **Customer Personalization** - Add custom customer names
- ⏰ **Auto Timestamps** - Automatic issue date and time with timezone support
- 🎨 **Professional Design** - High-quality card image generation
- 🔒 **Authorized Access** - Secure access control for authorized users only
- 📊 **Clean Architecture** - Modern layered architecture with separation of concerns
- 🐳 **Docker Ready** - Containerized deployment with Docker Compose
- 📦 **Poetry Support** - Modern Python dependency management

---

## 🚀 Why This Bot?

### Modern Development Stack
- **Docker** - Consistent environments, easy deployment, no dependency conflicts
- **Poetry** - Better dependency management than pip, reproducible builds
- **Layered Architecture** - Maintainable, testable, and extensible code
- **Type Hints & Docstrings** - Self-documenting, IDE-friendly code
- **Makefile** - Simple commands for all common tasks

### Production Ready
- ✅ Environment-based configuration
- ✅ Structured logging with levels
- ✅ Error handling and validation
- ✅ Non-root Docker user for security
- ✅ Health checks in Docker
- ✅ Resource limits configured

---

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Your Telegram User ID (get from [@userinfobot](https://t.me/userinfobot))

---

## 🚀 Installation

### Quick Start with Docker 🐳 (Recommended)

```bash
git clone https://github.com/yourusername/FggStoreCardsBot.git
cd FggStoreCardsBot
cp .env.example .env
# Edit .env with your BOT_TOKEN and AUTHORIZED_USER_ID
docker-compose up -d
```

### With Poetry 📦

```bash
poetry install
cp .env.example .env
# Edit .env with your credentials
poetry run python main.py
```

### With pip

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python main.py
```

### Setup Configuration

**Configure .env file:**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Add your credentials to `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
AUTHORIZED_USER_ID=your_telegram_user_id
LOG_LEVEL=INFO
```

### Required Assets

Ensure these files are in place:

- **Card Template**: `templates/card.png` - Your PlayStation card template image
- **Font File**: `assets/fonts/tahoma.ttf` - Arabic-compatible font (Tahoma or similar)

---

## 🎯 Usage

### Running the Bot

**With Docker:**
```bash
docker-compose up -d        # Start in background
docker-compose logs -f      # View logs
docker-compose down         # Stop
```

**With Poetry:**
```bash
poetry run python main.py
# Or use the Makefile:
make run
```

**With pip:**
```bash
python main.py
```

**Using Makefile (recommended):**
```bash
make help           # Show all available commands
make install        # Install dependencies
make run            # Run the bot
make docker-up      # Run with Docker
make docker-logs    # View Docker logs
make test           # Run tests
make format         # Format code
```

You should see:

```
2026-02-09 12:00:00 - __main__ - INFO - Starting FGGSTORE Card Generator Bot v2.0.0
2026-02-09 12:00:00 - __main__ - INFO - Authorized User ID: 123456789
2026-02-09 12:00:00 - __main__ - INFO - Bot is running and polling for updates...
```

### Bot Commands

- `/start` - Begin card generation process
- `/cancel` - Cancel current operation

### Card Generation Flow

1. **Start**: Send `/start` to the bot
2. **Select Price**: Choose card value (10$, 20$, 25$, 50$, 100$)
3. **Select Country**: Choose region (USA, KSA, UAE)
4. **Enter Code**: Provide activation code (auto-formatted)
5. **Enter Name**: Add customer name
6. **Receive Card**: Bot generates and sends the customized card image

---

## 📁 Project Structure

```
FggStoreCardsBot/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── config/                   # Configuration layer
│   │   ├── __init__.py
│   │   └── settings.py          # Application settings
│   ├── models/                   # Data models layer
│   │   ├── __init__.py
│   │   └── card_data.py         # Card data structures
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   └── card_generator.py   # Image generation service
│   ├── handlers/                 # Telegram handlers layer
│   │   ├── __init__.py
│   │   └── card_handler.py     # Conversation handlers
│   └── utils/                    # Utilities layer
│       ├── __init__.py
│       ├── constants.py         # Constants and enums
│       └── text_processor.py   # Arabic text processing
├── assets/                       # Static assets
│   └── fonts/                   # Font files
│       └── tahoma.ttf
├── templates/                    # Image templates
│   └── card.png                 # Card template
├── temp/                         # Temporary files (auto-created)
├── main.py                       # Application entry point
├── pyproject.toml               # Poetry dependencies & config
├── requirements.txt              # Pip dependencies (alternative)
├── Dockerfile                    # Docker container definition
├── docker-compose.yml           # Docker orchestration
├── .dockerignore                # Docker build exclusions
├── Makefile                     # Development commands
├── .env.example                  # Environment variables template
├── .gitignore                   # Git ignore rules
├── LICENSE                       # MIT License
├── Procfile                      # Deployment configuration
├── QUICK_START.md               # Quick setup guide
├── REFACTORING_SUMMARY.md       # Migration documentation
└── README.md                     # This file
```

---

## 🏗️ Architecture

The bot follows a **layered architecture** pattern:

### Layers

1. **Configuration Layer** (`app/config/`)
   - Manages environment variables and settings
   - Validates configuration on startup
   - Provides centralized access to paths and constants

2. **Models Layer** (`app/models/`)
   - Defines data structures (CardData, enums)
   - Handles data validation and formatting
   - Provides data transformation methods

3. **Services Layer** (`app/services/`)
   - Business logic implementation
   - Image generation with PIL
   - Text processing and rendering

4. **Handlers Layer** (`app/handlers/`)
   - Telegram conversation flow
   - User interaction logic
   - Command and message handling

5. **Utils Layer** (`app/utils/`)
   - Helper functions
   - Constants and enums
   - Arabic text processing utilities

### Design Patterns

- **Singleton Pattern**: Configuration settings
- **Service Pattern**: Card generation logic
- **Conversation Pattern**: Multi-step user interactions
- **Separation of Concerns**: Clear layer boundaries

---

## ☁️ Deployment

### Deploy with Docker (Production)

**Using Docker on any VPS (DigitalOcean, AWS, etc.):**

```bash
# On your server
git clone your-repository
cd FggStoreCardsBot

# Configure environment
cp .env.example .env
vim .env  # Add your credentials

# Deploy
docker-compose up -d

# Verify
docker-compose logs -f
```

**Update deployment:**
```bash
git pull
docker-compose down
docker-compose up -d --build
```

### Deploy on Render

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin your-repo-url
   git push -u origin main
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Background Worker"
   - Connect your GitHub repository
   - Configure:
     - **Name**: fggstore-bot
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`

3. **Add Environment Variables**
   - `BOT_TOKEN`: Your bot token
   - `AUTHORIZED_USER_ID`: Your Telegram user ID
   - `LOG_LEVEL`: INFO

4. **Deploy** - Click "Create Background Worker"

### Deploy on Railway

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login and Initialize**
   ```bash
   railway login
   railway init
   ```

3. **Add Environment Variables**
   ```bash
   railway variables set BOT_TOKEN=your_token
   railway variables set AUTHORIZED_USER_ID=your_id
   ```

4. **Deploy**
   ```bash
   railway up
   ```

### Deploy on Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create fggstore-bot

# Set environment variables
heroku config:set BOT_TOKEN=your_token
heroku config:set AUTHORIZED_USER_ID=your_id

# Deploy
git push heroku main
```

---

## 🛠️ Development

```bash
# Format code
make format

# Run tests
make test

# Type checking
make lint

# Docker commands
make docker-up      # Start
make docker-down    # Stop
make docker-logs    # View logs
```

### Adding New Features

1. **New Card Values**: Update `CardPrice` enum in `app/models/card_data.py`
2. **New Countries**: Update `Country` enum in `app/models/card_data.py`
3. **New Text Fields**: Update `POSITIONS` in `app/utils/constants.py`

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BOT_TOKEN` | Telegram Bot API token | ✅ Yes | - |
| `AUTHORIZED_USER_ID` | Telegram user ID with access | ✅ Yes | - |
| `LOG_LEVEL` | Logging verbosity | ❌ No | `INFO` |

### Customization

- **Font**: Replace `assets/fonts/tahoma.ttf` with your preferred Arabic-compatible font
- **Template**: Replace `templates/card.png` with your custom card design
- **Positions**: Adjust text positions in `app/utils/constants.py`
- **Timezone**: Modify `TIMEZONE_OFFSET_HOURS` in `app/config/settings.py`

---

## 🐛 Troubleshooting

### Common Issues

**Bot doesn't respond**
- Verify `BOT_TOKEN` is correct
- Check bot is running: `ps aux | grep main.py`
- Review logs for errors

**"Unauthorized" message**
- Ensure `AUTHORIZED_USER_ID` matches your Telegram user ID
- Get your ID from [@userinfobot](https://t.me/userinfobot)

**Font rendering issues**
- Ensure `tahoma.ttf` exists in `assets/fonts/`
- Verify font supports Arabic characters
- Check file permissions

**Template not found**
- Place `card.png` in `templates/` directory
- Verify file name matches exactly
- Check file permissions

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**FGGSTORE**

---

## 📞 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/yourusername/FggStoreCardsBot/issues)
- 💬 [Discussions](https://github.com/yourusername/FggStoreCardsBot/discussions)

---

<div align="center">

**Made with ❤️ by FGGSTORE**

⭐ Star this repo if you find it helpful!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/FggStoreCardsBot?style=social)](https://github.com/yourusername/FggStoreCardsBot/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/FggStoreCardsBot?style=social)](https://github.com/yourusername/FggStoreCardsBot/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/FggStoreCardsBot?style=social)](https://github.com/yourusername/FggStoreCardsBot/watchers)

**Open Source | MIT Licensed | Contributions Welcome**

</div>
