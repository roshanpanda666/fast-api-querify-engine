import os
from fastapi import FastAPI, BackgroundTasks
from dotenv import load_dotenv
from config.database import db
from routes.watch_queries import watch_queries_stream
import google.generativeai as genai
from bson import ObjectId
from datetime import datetime

# ---------------------------
# FastAPI App
# ---------------------------
app = FastAPI()

# ---------------------------
# Load Gemini API Key
# ---------------------------
load_dotenv(override=True)
apikey = os.getenv("GEMINI_API_KEY")
if not apikey:
    raise ValueError("Please set your GEMINI_API_KEY in .env file!")

genai.configure(api_key=apikey)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ---------------------------
# System Prompt
# ---------------------------
SYSTEM_PROMPT = """
You are an AI that analyzes a user query and a list of moderators.
Each moderator has certain skills (listed below).
Your task is to determine which moderator is the best fit to handle the query.
Respond ONLY with the username(s) of the best-suited moderator(s), comma-separated if multiple.
"""

# ---------------------------
# LLM & Moderator Functions
# ---------------------------
def select_best_moderators(query: str, moderators: list):
    try:
        mod_descriptions = "\n".join(
            [f"{mod['username']}: {', '.join(mod.get('skills', []))}" for mod in moderators]
        )
        user_prompt = f"Query: {query}\nModerators:\n{mod_descriptions}\nWhich moderator(s) is best suited to solve this query?"

        chat = model.start_chat(history=[{"role": "user", "parts": [SYSTEM_PROMPT]}])
        response = chat.send_message({"role": "user", "parts": [user_prompt]})
        usernames = [u.strip() for u in response.text.split(",") if u.strip()]
        return usernames
    except Exception as e:
        print("⚠️ Error selecting moderators:", e)
        return []

def assign_query_to_selected_moderators(query_obj):
    moderators = list(db["queries"].find({"role": "Moderator"}, {"username": 1, "skills": 1}))
    if not moderators:
        print("⚠️ No moderators found in DB!")
        return

    best_mods_usernames = select_best_moderators(query_obj["queryText"], moderators)
    if not best_mods_usernames:
        print("⚠️ LLM could not determine suitable moderators. Assigning to all.")
        best_mods_usernames = [mod["username"] for mod in moderators]

    best_mods_docs = [mod for mod in moderators if mod["username"] in best_mods_usernames]

    for mod in best_mods_docs:
        result = db["queries"].update_one(
            {"_id": mod["_id"]},
            {"$push": {"queriesGot": query_obj}}
        )
        print(
            f"✅ Pushed to {mod['username']} (ID: {mod['_id']}): "
            f"Matched={result.matched_count}, Modified={result.modified_count}"
        )

    print(
        f"🚀 Query '{query_obj['queryText']}' assigned to moderators: "
        f"{[mod['username'] for mod in best_mods_docs]}"
    )

# ---------------------------
# MongoDB Watcher Background Task
# ---------------------------
def rose_watcher():
    print("💻 R.O.S.E is now monitoring MongoDB queries...\n")

    for update in watch_queries_stream():
        updated_queries = update.get("updated_queries", [])
        for q_text in updated_queries:
            if not q_text:
                continue

            user_doc = db["queries"].find_one({"queries.query": q_text})
            if not user_doc:
                print(f"⚠️ Could not fetch user document for query '{q_text}', skipping.")
                continue

            query_data = next((q for q in user_doc.get("queries", []) if q["query"] == q_text), None)
            if not query_data:
                print(f"⚠️ Could not find query object inside user document for '{q_text}', skipping.")
                continue

            same_query_id = query_data["_id"]

            query_obj = {
                "userId": user_doc["_id"],
                "queryId": str(same_query_id),
                "queryText": query_data["query"],
                "answered": False,
                "response": "",
                "createdAt": datetime.utcnow(),
            }

            print(
                f"\n🆕 New Query Detected: {q_text} from User: {user_doc['username']} (UserID: {user_doc['_id']})"
            )
            print(f"🔗 Shared queryId: {same_query_id}")

            assign_query_to_selected_moderators(query_obj)

# ---------------------------
# Home Route "/" to Start ROSE
# ---------------------------
@app.get("/")
async def home(background_tasks: BackgroundTasks):
    background_tasks.add_task(rose_watcher)
    return {"message": "🌹 R.O.S.E AI is running in background and monitoring MongoDB!"}
