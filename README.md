# Smart-Calendar-AI
An AI-powered smart calendar application built with Python, Streamlit, and Google Calendar API to analyze events, detect schedule conflicts, and identify available time slots.
# Smart Calendar AI

## Project Overview

Smart Calendar AI is an intelligent calendar management application built using Python, Streamlit, and Google Calendar API. The application analyzes calendar events, detects scheduling conflicts, and identifies available free time slots.

## Technologies Used

- Python
- Streamlit
- Google Calendar API
- Google OAuth 2.0

## Key Features

- Connects with Google Calendar
- Displays today's calendar events
- Detects scheduling conflicts
- Identifies available free time slots
- Analyzes schedules within working hours

## Project Workflow

1. Authenticate the user using Google OAuth 2.0.
2. Connect to Google Calendar using the Google Calendar API.
3. Retrieve calendar events.
4. Analyze today's schedule.
5. Detect overlapping or conflicting events.
6. Calculate available free time slots.
7. Display the results through a Streamlit interface.

## Project Structure

```text
Smart-Calendar-AI/
│
├── app.py
├── main.py
├── README.md
└── .gitignore
```

## Setup and Installation

1. Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

2. Navigate to the project folder:

```bash
cd Smart-Calendar-AI
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your own Google Calendar API credentials.

5. Run the Streamlit application:

```bash
streamlit run app.py
```

## Security Note

Google API credentials and authentication tokens are not included in this repository. Users must create their own Google Cloud project and configure their own credentials before running the application.

## Project Outcome

This project demonstrates API integration, OAuth authentication, schedule analysis, conflict detection, and interactive application development using Python and Streamlit.
