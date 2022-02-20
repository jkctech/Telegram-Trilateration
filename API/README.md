# API Method

We are not gonna talk about the fact that I never even tried using this approach... M'kay? ANYWAYSSSS...

By using the <a href="https://docs.telethon.dev/en/stable/" target="_blank">Telethon</a> module for Python, we can create a Telegram client to request the data.
This method also does not even require any GPS spoofing since we can just pass coördinates to the API call... (Yeah this is not a problem at all Telegram, keep telling yourself that)

## Getting started

1. Make sure you have a Telegram account and an API key. (Register your key  <a href="https://my.telegram.org/" target="_blank">Here</a>)
1. Clone the repository and move your terminal over to this folder
1. **OPTIONAL**: I recommend and prefer creating a virtual environment using `python -m venv venv`
1. Install the required Python modules: `python -m pip install -r requirements.txt`
1. Make a copy of `config_default.json` and name it `config.json`
1. Edit `config.json` to your preference and place in your API ID and hash
1. Run the program by using `python nearby.py`

**First run only**
On your first run of the program, the bot will ask for your phone number, Telegram password and will let you verify these by a 2FA code.
This information will be stored in `trilat.session` and should be remembered automatically.

**Compatability**
When run on Windows 7, I had trouble getting the Telethon Client to start and ask for my credentials. I had no trouble doing so on Windows 10.

## Parsing the data

When the bot is done gathering data. the result will be saved into the `data` folder inside this folder. These `.json` files are compatible with the **Webview** part of this project and allow you to render a map of people's locations.

## Notes

 - Rate limiting still applies on this endpoint. I did not bother to detect issues by comparing timestamps, you have to check for this for yourself.
 I found that I can make 3 consecutive API calls before the rate-limiting kicks-in and requires you to wait for about ~15 minutes. (There are ways to bypass this, but again, this is a proof-of-concept)