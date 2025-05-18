# import google.generativeai as genai
# from PIL import Image
# import io
# from config import GEMINI_API_KEY

# genai.configure(api_key=GEMINI_API_KEY)

# def analyze_text_and_image(prompt, image_file):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     image_bytes = image_file.read()
#     image_file.seek(0)
#     img = Image.open(io.BytesIO(image_bytes))

#     response = model.generate_content([prompt, img])
#     return response.text

# # def is_food_image(image_file):
# #     model = genai.GenerativeModel('gemini-1.5-flash')
# #     image_bytes = image_file.read()
# #     image_file.seek(0)
# #     img = Image.open(io.BytesIO(image_bytes))

# #     response = model.generate_content([
# #         "Describe this image briefly. Is it food or not?"])

# #     description = response.text.lower()
# #     food_keywords = ['food', 'dish', 'meal', 'plate', 'fruit', 'vegetable', 'bread', 'rice', 'snack']
# #     return any(keyword in description for keyword in food_keywords), description


# import io
# from PIL import Image
# import google.generativeai as genai

# def is_food_image(image_file):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     image_bytes = image_file.read()
#     image_file.seek(0)
#     img = Image.open(io.BytesIO(image_bytes))

#     response = model.generate_content([
#         """Look at the image and identify the clearly visible objects based on the user's question. Respond in clean bullet points, listing only what you can see clearly. Do not speculate or give extra explanations. At the end, summarize with: "→ Total: X [object name]".

# Keep the answer short, visual-based, and focused only on the question.""",img
# ])


#     description = response.text.lower()
#     food_keywords = ['food', 'dish', 'meal', 'plate', 'fruit', 'vegetable', 'bread', 'rice', 'snack']

#     # Check if any food keyword is present in the response
#     is_food = any(keyword in description for keyword in food_keywords)

#     if is_food:
#         return True, description
#     else:
#         return False, None  # No description if not food

# chat_model = genai.GenerativeModel("gemini-2.0-flash-001")
# chat_session = chat_model.start_chat()


import os
import io
from PIL import Image
import google.generativeai as genai

#from config import GEMINI_API_KEY
# new config....
from config import Config
genai.configure(api_key=Config.GEMINI_API_KEY)

from config import Config

# ✅ Use the config class to get the API key
genai.configure(api_key=Config.GEMINI_API_KEY)


# Configure Gemini once
# genai.configure(api_key=GEMINI_API_KEY)

# Reuse models
multimodal_model = genai.GenerativeModel('gemini-1.5-flash')
chat_model = genai.GenerativeModel('gemini-2.0-flash-001')
chat_session = chat_model.start_chat()

def analyze_text_and_image(prompt, image_file):
    try:
        image_bytes = image_file.read()
        image_file.seek(0)
        img = Image.open(io.BytesIO(image_bytes))
        response = multimodal_model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"❌ Error analyzing image: {str(e)}"

def is_food_image(image_file):
    try:
        image_bytes = image_file.read()
        image_file.seek(0)
        img = Image.open(io.BytesIO(image_bytes))
        response = multimodal_model.generate_content([
            """Look at the image and identify the clearly visible objects..""", img
        ])
        description = response.text.lower()
        food_keywords = ['food', 'dish', 'meal', 'plate', 'fruit', 'vegetable', 'bread', 'rice', 'snack']
        return any(k in description for k in food_keywords), description
    except Exception as e:
        return False, f"Error: {str(e)}"

def chat_with_gemini(prompt):
    allowed_keywords = ['health', 'diet', 'food', 'nutrition', 'meal', 'calories', 'fitness', 'exercise', 'protein', 'fat', 'carbs']
    if not any(keyword in prompt.lower() for keyword in allowed_keywords):
        return "⚠️ Please ask health, diet, or food-related questions only."

    try:
        modified_prompt = (
            "You are a smart nutrition assistant. "
            "Answer ONLY in bullet points (max 5 lines).\n\n"
            f"User: {prompt}"
        )
        response = chat_session.send_message(modified_prompt)
        return response.text
    except Exception as e:
        return f"❌ Chat error: {str(e)}"



