# backend/ai_debugger.py
from openai import OpenAI
import google.generativeai as genai

# 🔐 Your API keys (direct version — use only for local testing)
OPENAI_API_KEY = "your-openai-api-key"
GEMINI_API_KEY = "api key"


# ✅ Initialize both clients
client = OpenAI(api_key=OPENAI_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)


# ------------------------------------------
# 🧠 1️⃣ Single File Analyzer
# ------------------------------------------
def analyze_code(code: str):
    """
    AI-powered code analyzer using OpenAI (fallback to Gemini if OpenAI fails)
    """
    prompt = f"""
    You are an AI debugger. Analyze the following Python code:
    - Find syntax or logic errors.
    - Identify potential runtime or import issues.
    - Suggest safe minimal fixes.
    - Give short, clear, human-friendly explanation.

    Code:
    {code}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert Python code debugger and mentor."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return {
            "summary": "✅ OpenAI analysis complete",
            "suggestion": ai_reply
        }

    except Exception as e:
        print("⚠️ OpenAI failed, switching to Gemini:", e)
        try:
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            gemini_response = gemini_model.generate_content(prompt)
            return {
                "summary": "✅ Gemini analysis complete",
                "suggestion": gemini_response.text
            }
        except Exception as gerr:
            return {"error": f"Both APIs failed. OpenAI: {str(e)}, Gemini: {str(gerr)}"}


# ------------------------------------------
# ⚡ 2️⃣ Real-Time Multi-File Agent Debugger
# ------------------------------------------
def analyze_live_code(current_file: str, all_files: dict):
    """
    Real-time AI agent debugger that analyzes code as user types.
    Detects dependency issues between multiple project files.
    """

    # Combine all project files into one big context for analysis
    project_context = "\n\n".join([
        f"### FILE: {name}\n{content}"
        for name, content in all_files.items()
    ])

    prompt = f"""
    You are a real-time AI debugging assistant.
    Analyze the currently edited file in context of the full project.

    --- Current File Being Edited ---
    {current_file}

    --- All Other Project Files ---
    {project_context}

    Check for:
    1. Syntax or indentation errors.
    2. Undefined functions or variables imported from other files.
    3. Cross-file dependency mismatches.
    4. Quick suggestions (1–2 lines) to fix or improve it.

    Return result as a short message like a coding mentor.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a real-time AI coding mentor that detects issues live."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return {"mode": "live", "result": ai_reply}

    except Exception as e:
        print("⚠️ Live analysis via OpenAI failed, switching to Gemini:", e)
        try:
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            gemini_response = gemini_model.generate_content(prompt)
            return {"mode": "live", "result": gemini_response.text}
        except Exception as gerr:
            return {"error": f"Both AI models failed. OpenAI: {str(e)}, Gemini: {str(gerr)}"}


# ------------------------------------------
# 🧩 3️⃣ Full Project Dependency Analyzer
# ------------------------------------------
def analyze_project_dependencies(files: dict):
    """
    Takes multiple files (e.g., index.js, app.js, utils.py) and checks:
    - Missing imports or undefined references across files
    - File-to-file dependency issues
    - Circular imports or function mismatch
    - Suggests corrections and best practices
    """

    # Merge files into a single context
    project_context = "\n\n".join([
        f"### FILE: {filename}\n{content}"
        for filename, content in files.items()
    ])

    prompt = f"""
    You are an expert multi-file AI code reviewer and dependency analyzer.

    Analyze the following project which contains multiple files:
    {project_context}

    Your tasks:
    1. Detect if any file uses a function/class/variable from another file without importing it.
    2. Identify any circular imports or unused imports.
    3. Point out missing or duplicate function names across files.
    4. Suggest clear fixes — e.g. “import X from Y” or “move this function to utils.js”.
    5. Keep your response short and formatted with bullet points.

    Output Example:
    - ⚠️ File `index.js` calls `renderApp()` but it’s not imported from `app.js`.
    - 💡 Add `import {{ renderApp }} from './app.js';`
    - ✅ No circular dependency found.
    """

    try:
        # Use OpenAI model first
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI code reviewer that specializes in multi-file debugging."},
                {"role": "user", "content": prompt}
            ]
        )
        ai_reply = response.choices[0].message.content
        return {"summary": "✅ Project dependency analysis complete", "suggestion": ai_reply}

    except Exception as e:
        print("⚠️ Project analysis via OpenAI failed, switching to Gemini:", e)
        try:
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            gemini_response = gemini_model.generate_content(prompt)
            return {
                "summary": "✅ Gemini project analysis complete",
                "suggestion": gemini_response.text
            }
        except Exception as gerr:
            return {"error": f"Both APIs failed. OpenAI: {str(e)}, Gemini: {str(gerr)}"}
