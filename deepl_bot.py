from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

TELEGRAM_BOT_TOKEN = "8371850976:AAFaOTOfEbewipk0lg3vn6D2ySL1Iwa7eCo"
DEEPL_API_KEY = "728bbeb5-3ef0-4ad3-ae72-05ecc9f8a1c3:fx"


# ===== 語言指令對照 =====
LANG_MAP = {
    "/en": "EN",
    "/ja": "JA",
    "/zh": "ZH",
    "/ko": "KO",
    "/de": "DE",
}

DEEPL_URL = "https://api-free.deepl.com/v2/translate"

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # 必須有空白，例如：/ja 內容
    parts = text.split(" ", 1)
    if len(parts) < 2:
        await update.message.reply_text(
            "請用以下格式：\n"
            "/ja 文字（日文）\n"
            "/en 文字（英文）\n"
            "/zh 文字（中文）\n"
            "/ko 文字（韓文）\n"
            "/de 文字（德文）"
        )
        return

    command = parts[0].lower()   # 指令不分大小寫
    content = parts[1]

    if command not in LANG_MAP:
        await update.message.reply_text(
            "不支援的指令，請使用：\n"
            "/ja /en /zh /ko /de"
        )
        return

    target_lang = LANG_MAP[command]

    try:
        response = requests.post(
            DEEPL_URL,
            data={
                "auth_key": DEEPL_API_KEY,
                "text": content,
                "target_lang": target_lang
            },
            timeout=10
        )
        result = response.json()

        if "translations" not in result:
            await update.message.reply_text(
                "翻譯失敗，可能是免費額度已用完或 API 異常"
            )
            return

        translated_text = result["translations"][0]["text"]
        await update.message.reply_text(translated_text)

    except Exception as e:
        await update.message.reply_text("系統錯誤，請稍後再試")

# ===== 啟動 Bot =====
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, translate))

print("✅ DeepL 多語言翻譯 Bot 已啟動")
app.run_polling()