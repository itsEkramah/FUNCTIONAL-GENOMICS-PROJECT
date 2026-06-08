import traceback
from backend.config.settings import settings

print("OPENAI KEY:", settings.openai_api_key)
print("GEMINI KEY:", settings.gemini_api_key)

print("\n--- Testing Gemini ---\n")
try:
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("Gemini model instantiated successfully.")
    # Attempt a small generation
    response = model.generate_content("Say hello")
    print("Gemini response:", response.text)
except Exception as e:
    print("Gemini error:")
    traceback.print_exc()

print("\n--- Testing OpenAI ---\n")
try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    print("OpenAI client instantiated successfully.")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say hello"}],
        temperature=0.2
    )
    print("OpenAI response:", response.choices[0].message.content)
except Exception as e:
    print("OpenAI error:")
    traceback.print_exc()
