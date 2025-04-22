
# 🎮 Telegram PlayStation Card Bot

A Telegram bot that automatically generates PlayStation Store card images, customized for **FGGSTORE**.

---

## ✨ Features

✅ Select card value (e.g., 10$, 25$, 50$)  
✅ Choose country (USA, KSA, UAE)  
✅ Enter and auto-format the activation code  
✅ Add customer name  
✅ Automatically include issue date and time  
✅ Generate a professional card image with all details  

---

## 🛠 Technologies Used

- **Python**
- **Pillow** – for image manipulation
- **python-telegram-bot** – for Telegram bot interaction
- **arabic_reshaper** + **python-bidi** – for proper Arabic text rendering

---

## 📸 Output Example

![Sample Output](sample_card.png)

---

## 🚀 How to Run

1. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Add your card template image and name it exactly:

   ```
   card.png
   ```

3. Start the bot:

   ```bash
   python main.py
   ```

🔐 **Note:**  
Make sure to:
- Update your Telegram **Bot Token**  
- Set the correct **font path** inside the script (if using custom Arabic font)

---

## ☁️ Deploying for Free (24/7)

You can deploy this bot for free using:

- [Render](https://render.com)
- [Railway](https://railway.app)

### ⚡ Quick Steps:

1. Push your code to a GitHub repository  
2. Connect your repo to **Render** or **Railway**  
3. Add environment variable:
   - `TOKEN` → *Your Telegram Bot Token*  
4. Set the start command:

   ```bash
   python main.py
   ```

Your bot will now run **24/7** 🎉

---

## 📂 Project Structure

| File               | Description                                   |
|--------------------|-----------------------------------------------|
| `main.py`          | Main bot script                               |
| `card.png`         | Base card template image                      |
| `sample_card.png`  | Sample output card image                      |
| `tahoma.ttf`       | Arabic font used in rendering text            |
| `Amiri-Regular.ttf`| Optional Arabic font                          |
| `requirements.txt` | Required Python packages                      |
| `.env`             | Environment variables (BOT_TOKEN, USER_ID)    |
| `Procfile`         | For deployment on Heroku / Render             |

```

---

> Made with ❤️ for FGGSTORE
