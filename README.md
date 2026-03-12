# Job Applications Tracker Bot  
[Open in Telegram](https://t.me/job_apps_tracker_bot)

A Telegram bot built with **Aiogram v3** that helps users track job applications, save jobs, manage statuses, and view statistics.

---

## Features

* Save jobs to your personal tracker.
* View all saved jobs with details.
* Change the status of a job (Applied, Accepted, Rejected).
* Delete jobs from your tracker.
* Interactive menu using **inline buttons**.
* Persistent state management using **FSMContext**.
* HTML-based message rendering for clean presentation.

---

## Screenshots / Preview

![Screenshot 1](https://github.com/lashchilin-andrii/job-tracker-bot/blob/demo/screenshot_1.jpg)  
![Screenshot 2](https://github.com/lashchilin-andrii/job-tracker-bot/blob/demo/screenshot_2.jpg)  
![Screenshot 3](https://github.com/lashchilin-andrii/job-tracker-bot/blob/demo/screenshot_3.jpg)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/job-applications-tracker-bot.git
cd job-applications-tracker-bot
```

2. Run with UV:

```bash
uv venv
source .venv/bin/activate
uv sync
```

3. Set your **Telegram Bot API token** in `.env`:

```python
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

---

## Usage

Run the bot:

```bash
python main.py
```

Interact with your bot in Telegram:

1. Start the bot with `/start`.
2. Use the menu buttons to:

   * Browase job offers by keywords and location
   * Save a job
   * View your jobs
   * Change job statuses
   * Delete jobs
   * View your profile stats

---

## Project Structure

```
.
├── alembic/                 # Alembic migrations
├── database.sqlite          # SQLite database
├── Dockerfile               # Docker configuration
├── main.py                  # Bot entry point
├── pyproject.toml
├── README.md
├── requirements.txt
├── src/
│   ├── api/jooble/          # Jooble API integration
│   ├── base/                # Core utilities
│   │   ├── button.py
│   │   ├── enum.py
│   │   ├── handler.py
│   │   ├── keyboard.py
│   │   ├── model.py
│   │   ├── repository.py
│   │   ├── service.py
│   │   └── state.py
│   ├── button.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── job/                 # Job-related models, services, handlers
│   │   └── base/ structure
│   ├── logging.py
│   ├── message.py
│   ├── state.py
│   ├── user/                # User-related models, services, handlers
│   │   └── base/ structure
│   └── user_job/            # User-job relations, handlers, services
│   │   └── base/ structure
├── test/                    # Unit tests
└── uv.lock                  # Dependency lock
```

---

Perfect! Here’s your **updated README** with a **Docker section** added and the installation/usage section removed:

---

# Job Applications Tracker Bot

A Telegram bot built with **Aiogram v3** that helps users track job applications, save jobs, manage statuses, and view statistics.

---

## Features

* Save jobs to your personal tracker.
* View all saved jobs with details.
* Change the status of a job (Applied, Accepted, Rejected).
* Delete jobs from your tracker.
* Interactive menu using **inline buttons**.
* Persistent state management using **FSMContext**.
* HTML-based message rendering for clean presentation.

---

## Docker

You can run the bot easily using Docker.

```bash
docker build -t job-tracker-bot .
```

### Run the container

```bash
docker run -d --name job-tracker-bot job-tracker-bot
```

---

## License

MIT License © [Andrii Lashchilin](https://github.com/lashchilin-andrii)

