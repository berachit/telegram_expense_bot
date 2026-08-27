import os

from dotenv import load_dotenv
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters)

from db import add_user

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user.id,
        user.username
    )

    await update.message.reply_text(
        "👋 Welcome to Expense Tracker!\n"
        "I can help you track your expenses.\n\n"
        "Commands:\n"
        "/add - Add an expense\n"
        "/expenses - View expenses\n"
        "/total - View total spending\n"
        "/delete - Delete an expense\n"
        "/help - Show help\n"
    )

async def add_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["adding_expense"] = True

    await update.message.reply_text(
         "💰 How much did you spend?"
    )

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("adding_expense"):
        return

    amount = update.message.text
    context.user_data["amount"] = amount

    keyboard = [
        [
            InlineKeyboardButton("🍔 Food", callback_data="category_food"),
            InlineKeyboardButton("🚕 Travel",
            callback_data="category_travel")
        ],
        [
            InlineKeyboardButton("🛍 Shopping", callback_data="category_shopping"),
            InlineKeyboardButton("🏠 Bills", callback_data="category_bills")
        ],
        [
            InlineKeyboardButton("🎬 Entertainment", callback_data="category_entertainment"),
            InlineKeyboardButton("💊 Health", callback_data="category_health")
        ],
        [
            InlineKeyboardButton("📚 Education", callback_data="category_education"),
            InlineKeyboardButton("📦 Others", callback_data="category_other")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📂 What category?:",
        reply_markup=reply_markup
    )

async def handle_category(update:Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    category = query.data.replace("category_","")

    context.user_data["category"] = category

    if category == "other":
        await query.message.reply_text(
            "✏️ Please enter your category:"
        )
        return

    await query.message.reply_text(
        f"✅ Category selected: {category.title()}\n"
        "📝 What was the expense for?"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add",add_expense))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))
    app.add_handler(CallbackQueryHandler(handle_category, pattern="^category_"))

    print("Bot is running...")

    app.run_polling()

if __name__ == "__main__":
    main()