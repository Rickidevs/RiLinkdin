# LinkedIn Connection Bot

A simple Python-based automation tool using Selenium to send connection requests on LinkedIn. This bot can send requests either to random suggested connections or based on a search keyword. It includes basic anti-detection measures and session management via cookies.

**Note:** This is for educational purposes only. Automating actions on LinkedIn may violate their terms of service. Use at your own risk.

## Features
- Login to LinkedIn with email/password (first time) or saved cookies for subsequent runs.
- Send connection requests to random people from the "My Network" page.
- Search for people by keyword and send targeted connection requests.
- Basic rate limiting and random delays to mimic human behavior.
- Logging of actions to a file (`linkedin_bot.log`).
- Statistics saved to `bot_stats.json`.
- Daily limit enforcement (configurable, default max 100, but recommended 20-30).

## Requirements
- Python 3.6 or higher.
- Google Chrome browser installed (the bot uses ChromeDriver via Selenium).
- Dependencies:
  - Selenium: For browser automation.
  - Other standard libraries: `time`, `random`, `logging`, `json`, `datetime`, `os`, `pickle`.

## Installation
1. Clone the repository:
   `git clone https://github.com/Rickidevs/RiLinkdin.git
    cd RiLinkdin`

2. Install required Python packages:
   `pip install selenium`

3. Download the appropriate ChromeDriver version matching your Chrome browser from [chromedriver.chromium.org](https://chromedriver.chromium.org/downloads). Place it in your system's PATH or in the project directory.

## Usage
1. Run the script:
   `python main.py`

2. On first run, provide your LinkedIn email/phone and password when prompted. Cookies will be saved for future sessions.

3. Select the number of connections to send (max 50 for safety).

4. Choose mode:
- 1: Random connections from "My Network".
- 2: Search by keyword (e.g., "CEO" or "Developer").

5. The bot will handle navigation, sending requests, and logging. Check `linkedin_bot.log` for details and `bot_stats.json` for stats.

Example output:
`✅ Total connections sent: 10
 📅 Date: 2025-09-16 12:00:00`


## Anti-Detection Measures
To avoid LinkedIn's bot detection:
- **User-Agent Spoofing:** Sets a common browser user-agent to mimic a real user.
- **Disable Automation Flags:** Removes Selenium's detectable flags like `navigator.webdriver` and disables blink features.
- **Random Delays and Actions:** Introduces random sleep times (e.g., 0.05-0.15s per keystroke, 2-5s between actions) and mouse movements via ActionChains to simulate human input.
- **No Headless Mode:** Runs in maximized window mode for more natural behavior.
- **Cookie-Based Sessions:** Reuses saved cookies to avoid frequent logins, reducing suspicious activity.

These measures help bypass basic detection, but LinkedIn may still flag excessive automation. Monitor your account closely.

## Session Management
- **Cookies Handling:** On successful login, cookies are saved to `linkedin_cookies.pkl` using `pickle`. Subsequent runs load these cookies to restore the session, skipping manual login.
- **Fallback to Manual Login:** If cookies are invalid (e.g., expired), the bot prompts for credentials again and resaves cookies.
- **State Preservation:** The bot tracks connection counts in-memory and saves stats to JSON. No persistent database is used.

## Important Notes and Warnings
- **Rate Limits:** LinkedIn has undisclosed daily/weekly limits on connections (typically 100-200/week for free accounts). The bot enforces a configurable daily limit (default 100), but it's recommended to stay under 20-30/day to avoid restrictions or bans.
- **Account Safety:** Overuse can lead to temporary restrictions, captchas, or permanent bans. Use a secondary account for testing.
- **Error Handling:** The bot logs errors to `linkedin_bot.log`. Common issues include network problems, UI changes on LinkedIn, or invalid selectors.
- **Localization Support:** Handles English and Turkish UI elements (e.g., button texts like "Connect" or "Bağlan").
- **Dependencies on LinkedIn UI:** Selenium relies on XPath/CSS selectors, which may break if LinkedIn updates their site. Update selectors as needed.
- **No Personalization:** The bot sends requests without notes. Adding custom messages is not implemented.

## Legal Disclaimer
This tool is provided for educational and research purposes only. Automating interactions on LinkedIn violates their [User Agreement](https://www.linkedin.com/legal/user-agreement), which prohibits the use of bots, scrapers, or automation software. Using this bot may result in account suspension or legal action from LinkedIn/Microsoft.

The author is not responsible for any consequences arising from its use. You are solely responsible for complying with all applicable laws, including data privacy regulations (e.g., GDPR if handling EU data). Do not use this for spamming, harassment, or any unethical purposes.

If you're unsure about legality in your jurisdiction, consult a legal professional. This project does not encourage or endorse violating platform terms.
