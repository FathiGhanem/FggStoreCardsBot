Telegram PlayStation Card Bot
A Telegram bot that automatically generates PlayStation Store card images, customized for FGGSTORE.

Features
Select card value (e.g., 10$, 25$, 50$)

Choose country (USA, KSA, UAE)

Enter and auto-format the activation code

Add customer name

Automatically include issue date and time

Generate a professional image output with all details

Technologies Used
Python

Pillow – for image manipulation

python-telegram-bot – for Telegram bot handling

arabic_reshaper + python-bidi – for proper Arabic text rendering

Output Example

(You can upload a real output image here)

How to Run
Install the required packages:

pip install -r requirements.txt
Add your template image and name it:


card.png
Start the bot:

python main.py
Note: Make sure to update your Telegram Bot Token and the correct font path if needed.

Deploying for Free (24/7)
You can deploy this bot for free using:

Render (https://render.com)

Railway (https://railway.app)

Quick Steps
Push your code to a GitHub repository

Connect your GitHub repo to Render or Railway

Add the environment variable TOKEN with your bot's token

Set the start command to:

python main.py
Your bot will now run 24/7.

Project Structure
main.py: The main bot script

requirements.txt: Required dependencies

card.png: The template image

Support
This bot is private and used exclusively by FGGSTORE.

