import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

load_dotenv()

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
api_key = os.getenv('GOOGLE_API_KEY')
MODEL_NAME = 'gemini-1.5-pro' 

async def run_chat(user_input):
    generation_config = {
        "temperature": 0.5,
        "top_p": 0.7,
        "top_k": 50,
        "max_output_tokens": 250,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=[
            {
                "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
                "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
        ]
    )
    
    try:
        chat = model.start_chat(
            history=[{
                "role": "user",
                "parts": [""" Hello! I'm Sam, Abhishek's friendly assistant. Here's a quick overview of Abhishek's profile:

    **Education:**
    Final-year B.Tech student in Computer Engineering at IET, Lucknow, with a strong foundation in competitive programming and development.

    **Technical Skills:**
    Proficient in C++, JavaScript, SQL, HTML, CSS, and experienced with the MERN stack (MongoDB, Express.js, React.js, Node.js).

    **Key Projects:**

    **To-Do List App:**
    Developed a full-stack task management app with a user-friendly interface, allowing users to register, manage, and delete tasks. Backend APIs are powered by Express.js, with MongoDB handling data storage. This project showcases efficient data interaction and seamless task management.

    **Social Media Website (Instagram Clone):**
    Built using the MERN stack, this project includes real-time chat via Socket.io, image and video posts, comments, and likes. Secure authentication with JWT and Bcrypt, dynamic following systems, and admin group management demonstrate Abhishek's full-stack development skills. 
    [GitHub Repository](https://github.com/AbhishekChetiya)

    **Telegram Bot:**
    Personalized bot using Gemini AI, offering an engaging virtual introduction to Abhishek's skills and achievements. It provides real-time answers to user queries, reflecting his commitment to enhancing user interaction with innovative solutions.

    **Competitive Programming Achievements:**

    **Codeforces:**
    Expert (Highest Rating: 1633), Global Rank 869 in Educational Codeforces Round 163 (Div. 2), Global Rank 641 in Codeforces Round 962 (Div. 3).
    Profile Link: [https://codeforces.com/profile/abhishek_0123]

    **LeetCode:**
    Knight (Highest Rating: 2145), Top 16% globally, Global Rank 133 in Weekly Contest 412.
    Profile Link: [https://leetcode.com/u/abhishek_iet/]

    **CodeChef:**
    4-Star (Highest Rating: 1858), Global Rank 54 in CodeChef Starters 113 Division 2.
    Profile Link: [https://www.codechef.com/users/abhishek_072]

    **GeeksforGeeks:**
    5-Star (Highest Rating: 2098).
    Profile Link: [https://www.geeksforgeeks.org/user/abhishek_0123/]

    **TCS CodeVita Season 11:**
    Global Rank 175 out of 10,000 participants.

    **GitHub:**
    [https://github.com/AbhishekChetiya]

    Things To Notice:-
    Give Answer that only related to the abhishek only
    Does not Give any sexual and adult answer
    You use the given links to search any things other then that you conn't use 
    search you can say to users make the google search"""]
            }]
        )
        result = chat.send_message(user_input)
        return result.text
    except Exception as e:
        print(f"Error in run_chat: {e}")
        return "An error occurred while processing your request. Please try again."

async def perform_chat(user_message: str) -> str:
    try:
        response = await run_chat(user_message)
        return response if response else "I'm sorry, I didn't understand that."
    except Exception as e:
        print(f"Error in perform_chat: {e}")
        return "An error occurred while generating a response."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_message = update.message.text
        result = await perform_chat(user_message)
        await update.message.reply_text(result)
    except Exception as e:
        print(f"Error in handle_message: {e}")
        await update.message.reply_text("An error occurred while handling your message.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("Welcome! Send any message to start chatting.")
    except Exception as e:
        print(f"Error in start: {e}")
        await update.message.reply_text("An error occurred while starting the bot.")

if __name__ == '__main__':
    try:
        TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        if TELEGRAM_TOKEN is None:
            print("Error: TELEGRAM_TOKEN is not set. Please check your .env file.")
        else:
            # Ensure only one instance of the bot runs and clear any pending updates
            application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            application.add_handler(CommandHandler('start', start))  # Add a start command handler

            # Run polling with drop_pending_updates to prevent conflicts
            application.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"Error in bot setup: {e}")
