# Kumify

Kumify is a personal management tool designed to track and manage various aspects of your life, including habits, moods, dreams, activities, and more. Built with Django, it offers a modular design, allowing users to manage different modules according to their needs.

## Features

- **Mood Tracking**: Log your mood entries, visualize mood patterns with statistics, and manage activities associated with moods.
- **Dream Journal**: Record your dreams, categorize them with themes, and track lucid or special dreams.
- **Habits Tracking**: Set up habits and monitor them through customizable schedules.
- **Health Tracking**: Manage medications, schedules, and track health parameters.
- **Friends Management**: Basic personal relationship manager to keep track of connections.
- **Environment Tracking**: Analyze CO2 emissions and offset efforts.
- **OpenID Connect Authentication**: Supports authentication with an external OpenID Connect provider.
- **Notification System**: Receive notifications via Telegram or Matrix for different events or reminders.
- **API**: Simple API to extend the application's capabilities.

## Installation

### Prerequisites

- Python 3.11 or higher
- A database server (SQLite is configured by default, can be switched to MariaDB/MySQL)

### Steps

1. **Clone the repository**:

   ```bash
   git clone https://git.private.coffee/kumi/kumify.git
   cd kumify
   ```

2. **Create a virtual environment and activate it**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the settings**:

   - Copy `settings.dist.ini` to `settings.ini` and edit as necessary with your configurations (e.g., database settings).

5. **Prepare the database**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser for administrative access**:

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

   Access the application at `http://localhost:8000`.

## Configuration

The application uses `settings.ini` to manage configuration parameters like database, debugging, timezone, and other module-specific settings. Ensure to configure storage settings if you're using S3 for file storage or MySQL for the database.

## Modules

Enable or disable different modules in `kumify/settings.py` by modifying the `ENABLED_MODULES` list.

### Available Modules

- `cbt`: Cognitive Behavioral Therapy tools
- `mood`: Mood tracking and statistics
- `habits`: Habits management (WIP)
- `dreams`: Dream journal and analysis
- `health`: Health and medication tracking (WIP)
- `friends`: Relationship management (WIP)
- `environment`: CO2 management and offsetting (WIP)

## Notifications

Kumify supports sending notifications via Telegram and Matrix. Setup requires API keys and configuration details for each platform in the database settings.

## Development

This project includes additional tools and dependencies specified in `requirements-dev.txt` for development purposes, such as code formatters and linters.

### Development Commands

- **Format code with Black**:

  ```bash
  black .
  ```

- **Lint code with Ruff**:
  ```bash
  ruff check .
  ```

## Contributing

Contributions are welcome. Feel free to open issues or submit pull requests for bug fixes, feature requests, and enhancements.

## License

Kumify is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

Thanks to various open source projects that have contributed to this application, including Django and its ecosystem.
