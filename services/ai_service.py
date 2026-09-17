import os

def ask_gemini(question: str, department: str, departments: dict) -> str:
    """
    Gemini integration.

    The requested model is read from GEMINI_MODEL.
    Default: gemini-3.6-flash

    If the installed Gemini SDK/model name changes, update only .env and/or this file.
    The application itself remains unchanged.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

    if not api_key or api_key == "your_api_key_here":
        return (
            "Gemini API key is not configured yet. Add GEMINI_API_KEY in the .env file. "
            f"Selected model: {model_name}."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        department_context = departments.get(department, {})
        prompt = f"""
You are GovConnect AI, a citizen information assistant for India/Tamil Nadu.

Current department context: {department}
Department description: {department_context.get("description", "")}
Topics: {", ".join(department_context.get("topics", []))}

User question:
{question}

Rules:
1. Answer only about government schemes, public services, education, agriculture,
   departments, citizen services or the selected department.
2. Do not invent scheme names, eligibility, amounts, deadlines, orders or statistics.
3. If the question needs current information, clearly say that the answer must be
   verified against the latest official government source.
4. Never claim that GovConnect AI is an official government department.
5. Keep the answer simple and useful. Tamil or English is acceptable.
6. If the question is unrelated, politely say that you only handle government/public-service topics.
"""

        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text or "No answer was returned by the AI."

    except Exception as exc:
        return (
            "Gemini service could not be reached right now. "
            "Please verify GEMINI_API_KEY and GEMINI_MODEL in .env. "
            f"Configured model: {model_name}. "
            f"Technical detail: {type(exc).__name__}"
        )
