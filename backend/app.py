import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from services.supabase_client import supabase
from utils.password_generator import generate_password

# 1. Import the Google Gen AI SDK
from google import genai
from google.genai import types

app = Flask(__name__)

# Health check / Render root endpoint
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "Bharath Portfolio Backend is running successfully"
    }), 200

CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://bharath-portfolio-psi.vercel.app"
            ]
        }
    },
    supports_credentials=True
)

# 2. Initialize the Gemini Client 
# (It will read GEMINI_API_KEY from your Render environment variables)
client = genai.Client()

# =============================
# LOGIN
# =============================
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    password = data.get("password")
    response = supabase.table("admin_auth").select("*").limit(1).execute()
    stored_password = response.data[0]["current_password"]

    if password == stored_password:
        return jsonify({"success": True, "message": "Login successful"})
    return jsonify({"success": False, "message": "Invalid password"})

# =============================
# GENERATE NEW PASSWORD
# =============================
@app.route("/logout", methods=["POST"])
def logout():
    new_password = generate_password()
    supabase.table("admin_auth").update({"current_password": new_password}).eq("id", 1).execute()
    return jsonify({"message": "Password regenerated"})

# =============================
# VIEW CURRENT PASSWORD
# =============================
@app.route("/current-password")
def current_password():
    response = supabase.table("admin_auth").select("current_password").limit(1).execute()
    return jsonify({"password": response.data[0]["current_password"]})

# =============================
# HOME CONTENT
# =============================
@app.route("/home-content")
def get_home_content():
    response = supabase.table("home_content").select("*").limit(1).execute()
    return jsonify(response.data[0])

@app.route("/home-content", methods=["PUT"])
def update_home_content():
    data = request.json
    response = supabase.table("home_content").update({
        "welcome_note": data.get("welcome_note"),
        "greeting_name": data.get("greeting_name"),
        "typing_titles": data.get("typing_titles"),
        "description": data.get("description"),
        "hero_image": data.get("hero_image"),
        "primary_button_text": data.get("primary_button_text"),
        "primary_button_link": data.get("primary_button_link"),
        "secondary_button_text": data.get("secondary_button_text"),
        "secondary_button_link": data.get("secondary_button_link"),
    }).eq("id", 1).execute()
    return jsonify({"message": "Home content updated", "data": response.data})

# =============================
# PROJECTS
# =============================
@app.route("/projects")
def get_projects():
    response = supabase.table("projects").select("*").order("id", desc=True).execute()
    return jsonify(response.data)

@app.route("/projects", methods=["POST"])
def create_project():
    data = request.json
    response = supabase.table("projects").insert({
        "title": data.get("title"),
        "short_description": data.get("short_description"),
        "full_description": data.get("full_description"),
        "problem": data.get("problem"),
        "features": data.get("features"),
        "result_images": data.get("result_images"),
        "image_url": data.get("image_url"),
        "github_url": data.get("github_url"),
        "live_url": data.get("live_url"),
        "tech_stack": data.get("tech_stack"),
        "category": data.get("category"),
        "featured": data.get("featured"),
        "completion_date": data.get("completion_date"),
    }).execute()
    return jsonify(response.data)

@app.route("/projects/<int:id>", methods=["PUT"])
def update_project(id):
    data = request.json
    response = supabase.table("projects").update({
        "title": data.get("title"),
        "short_description": data.get("short_description"),
        "full_description": data.get("full_description"),
        "problem": data.get("problem"),
        "features": data.get("features"),
        "result_images": data.get("result_images"),
        "image_url": data.get("image_url"),
        "github_url": data.get("github_url"),
        "live_url": data.get("live_url"),
        "tech_stack": data.get("tech_stack"),
        "category": data.get("category"),
        "featured": data.get("featured"),
        "completion_date": data.get("completion_date"),
    }).eq("id", id).execute()
    return jsonify(response.data)

@app.route("/projects/<int:id>", methods=["DELETE"])
def delete_project(id):
    supabase.table("projects").delete().eq("id", id).execute()
    return jsonify({"message": "Project deleted"})

@app.route("/projects/<int:id>", methods=["GET"])
def get_project_by_id(id):
    response = supabase.table("projects").select("*").eq("id", id).single().execute()
    return jsonify(response.data)

# =============================
# ABOUT
# =============================
@app.route("/about")
def get_about():
    response = supabase.table("about").select("*").limit(1).execute()
    if response.data:
        return jsonify(response.data[0])
    return jsonify({})

@app.route("/about/<int:id>", methods=["PUT"])
def update_about(id):
    data = request.json
    response = supabase.table("about").update({
        "profile_image": data.get("profile_image"),
        "full_name": data.get("full_name"),
        "role_title": data.get("role_title"),
        "short_bio": data.get("short_bio"),
        "long_bio": data.get("long_bio"),
        "years_experience": data.get("years_experience"),
        "projects_completed": data.get("projects_completed"),
        "skills": data.get("skills"),
        "technologies": data.get("technologies"),
    }).eq("id", id).execute()
    return jsonify(response.data)

# =============================
# RESUME
# =============================
@app.route("/resume")
def get_resume():
    response = supabase.table("resume").select("*").limit(1).execute()
    if response.data:
        return jsonify(response.data[0])
    return jsonify({})

@app.route("/resume/<int:id>", methods=["PUT"])
def update_resume(id):
    data = request.json
    response = supabase.table("resume").update({
        "resume_title": data.get("resume_title"),
        "resume_description": data.get("resume_description"),
        "resume_url": data.get("resume_url"),
        "preview_image": data.get("preview_image"),
    }).eq("id", id).execute()
    return jsonify(response.data)

# =============================
# BLOG
# =============================
@app.route("/blog")
def get_blog():
    response = supabase.table("blog").select("*").order("id", desc=True).execute()
    return jsonify(response.data)

@app.route("/blog", methods=["POST"])
def create_blog():
    data = request.json
    response = supabase.table("blog").insert({
        "title": data.get("title"),
        "excerpt": data.get("excerpt"),
        "content": data.get("content"),
        "image_url": data.get("image_url"),
        "tags": data.get("tags"),
    }).execute()
    return jsonify(response.data)

@app.route("/blog/<int:id>", methods=["PUT"])
def update_blog(id):
    data = request.json
    response = supabase.table("blog").update({
        "title": data.get("title"),
        "excerpt": data.get("excerpt"),
        "content": data.get("content"),
        "image_url": data.get("image_url"),
        "tags": data.get("tags"),
    }).eq("id", id).execute()
    return jsonify(response.data)

@app.route("/blog/<int:id>", methods=["DELETE"])
def delete_blog(id):
    supabase.table("blog").delete().eq("id", id).execute()
    return jsonify({"message": "Blog deleted"})

@app.route("/blog/<int:id>", methods=["GET"])
def get_blog_by_id(id):
    response = supabase.table("blog").select("*").eq("id", id).limit(1).single().execute()
    return jsonify(response.data)

# =============================
# CONTACT
# =============================
@app.route("/contact")
def get_contact():
    response = supabase.table("contact").select("*").limit(1).execute()
    return jsonify(response.data[0] if response.data else {})

@app.route("/contact", methods=["PUT"])
def update_contact():
    data = request.json
    response = supabase.table("contact").update({
        "email": data.get("email"),
        "phone": data.get("phone"),
        "location": data.get("location"),
        "github": data.get("github"),
        "linkedin": data.get("linkedin"),
        "form_title": data.get("form_title"),
        "form_description": data.get("form_description"),
    }).eq("id", 1).execute()
    return jsonify({"message": "updated", "data": response.data})

# =============================
# CONTACT FORM SUBMISSION
# =============================
@app.route('/contact-submit', methods=['POST'])
def handle_contact_submission():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"error": "All fields are required"}), 400

        response = supabase.table("contact_messages").insert({
            "name": name,
            "email": email,
            "message": message
        }).execute()

        return jsonify({
            "success": True,
            "message": "Message sent successfully!",
            "data": response.data
        }), 200

    except Exception as e:
        print("CONTACT FORM ERROR:", str(e))
        return jsonify({"success": False, "error": "Internal server error"}), 500


# =============================
# PORTFOLIO AI CHATBOT (INTEGRATED WITH GEMINI)
# =============================
@app.route("/portfolio-ai", methods=["POST"])
def portfolio_ai():
    data = request.json
    
    if not data or "message" not in data:
        return jsonify({"error": "Message content is required"}), 400
        
    user_message = data.get("message")

    # Fetch live data blocks from your database tables
    projects = supabase.table("projects").select("*").execute().data
    about = supabase.table("about").select("*").limit(1).execute().data
    resume = supabase.table("resume").select("*").limit(1).execute().data
    contact = supabase.table("contact").select("*").limit(1).execute().data
    blogs = supabase.table("blog").select("*").order("id", desc=True).execute().data

    # Format database items as JSON strings to feed securely into system instructions
    context_about = json.dumps(about[0] if about else {}, indent=2)
    context_projects = json.dumps(projects if projects else [], indent=2)
    context_resume = json.dumps(resume[0] if resume else {}, indent=2)
    context_contact = json.dumps(contact[0] if contact else {}, indent=2)
    context_blogs = json.dumps(blogs if blogs else [], indent=2)

    # Dynamic System Instructions including your live database records
    SYSTEM_INSTRUCTION = f"""
    You are the personal AI Assistant for Bharath, working directly on his portfolio web application. 
    Your purpose is to answer user queries with intelligence, helpfulness, and a touch of engaging wit using exclusively the real-time background context below.

    --- LIVE PORTFOLIO DATABASE CONTEXT ---
    
    [ABOUT BHARATH]:
    {context_about}

    [PROJECTS CAROUSEL]:
    {context_projects}

    [RESUME CREDENTIALS]:
    {context_resume}

    [CONTACT & SOCIAL LINKS]:
    {context_contact}
    
    [BLOG POSTS]:
    {context_blogs}
    
    ---------------------------------------

    Behavior Constraints:
    1. Respond naturally in the third person or as Bharath's professional AI proxy representing his interests.
    2. Keep descriptions clear and easy to swallow in a fast-scrolling mobile chat panel (use small formatting adjustments or short line-breaks).
    3. Use technical project details (like tools, problems, features, live_url, github_url) dynamically when someone requests details about his builds.
    4. Share context on his written articles, technical blogs, or travel write-ups using the blog records when users ask about his insights or recent posts.
    5. Mention his "Bharath Vlogs & Tech" YouTube channel naturally when users ask for video content or more about his hobbies.
    6. If a metric or detailed question falls beyond this context data, politely guide them to check his profiles using his contact records.
    """

    try:
        # Generate completion with gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            )
        )
        return jsonify({"reply": response.text})

    except Exception as e:
        print("PORTFOLIO AI ERROR:", str(e))
        return jsonify({
            "reply": "My response matrix is cycling through a quick update right now. Mind running that question by me once more?"
        }), 500


if __name__ == "__main__":
    # Ensure production environment bindings are used
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
