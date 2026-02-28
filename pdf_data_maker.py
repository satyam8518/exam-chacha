from google import genai
from google.genai import types
import json
import os

# 1. आपकी API Key
API_KEY = "AIzaSyCxCianaWuLDkJ4zk3l0jeOZoFDHmgHiV8"

# 2. नया Client सेटअप (Google के नए SDK के अनुसार)
client = genai.Client(api_key=API_KEY)

print("==================================================")
print("🚀 Exam Chacha - Direct PDF to JSON Maker (New SDK) 🚀")
print("==================================================")

# 3. यूज़र से PDF का नाम पूछना
pdf_filename = input("📄 अपनी PDF फाइल का नाम डालें (जैसे history.pdf): ")

if not os.path.exists(pdf_filename):
    print(f"❌ एरर: '{pdf_filename}' नाम की कोई फाइल नहीं मिली! ध्यान रखें कि PDF उसी फोल्डर में हो।")
    exit()

# 4. PDF को AI के पास अपलोड करना
print(f"⏳ '{pdf_filename}' को AI के पास भेजा जा रहा है...")
try:
    # नई फाइल अपलोड कमांड
    uploaded_file = client.files.upload(file=pdf_filename)
    print(f"✅ फाइल अपलोड हो गई! (File URI: {uploaded_file.uri})")
except Exception as e:
    print(f"❌ फाइल अपलोड करने में एरर: {e}")
    exit()

# 5. AI के लिए सुपर-प्रॉम्प्ट
prompt = """
You are the Chief Content Creator for the 'Exam Chacha' competitive exam app.
I have uploaded a PDF document. It may contain Maths, Algebra, or general text.
Please read the entire document carefully and convert the educational content into a strict JSON format.

RULES FOR GENERATION:
1. MAXIMUM 20 QUESTIONS PER CLASS: A single class JSON must NOT exceed 20 questions.
2. AUTO-SPLIT LOGIC: If the PDF is large, split the content logically into multiple classes (Part 1, Part 2, etc.).
3. FORMAT: Output a JSON object containing an array named "classes".
4. SLIDES: Summarize the concepts into informative 'slides' using bullet points (•) and \\n for new lines.
5. EXAM FOCUS: Make the MCQs tough and standard for competitive exams (4 options, 1 correct answer).

REQUIRED JSON OUTPUT STRUCTURE:
{
  "classes": [
    {
      "subjectId": "auto_gen_subject_part_1",
      "subjectTitle": "Chapter Name - Part 1",
      "topics": [
        {
          "title": "Topic Name",
          "slides": [
            "• Point 1\\n• Point 2"
          ],
          "questions": [
            {
              "questionText": "Question?",
              "options": ["A", "B", "C", "D"],
              "correctAnswer": "A"
            }
          ]
        }
      ]
    }
  ]
}
"""

print(f"🧠 AI आपकी PDF पढ़ रहा है और नोट्स बना रहा है... (बड़ी PDF में 1-2 मिनट लग सकते हैं)")

try:
    # 6. नया Generate Content कमांड (सबसे नए मॉडल के साथ)
    response = client.models.generate_content(
        model='gemini-2.5-flash', # नया और सबसे तेज़ मॉडल
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )
    
    # 7. JSON को समझना और अलग-अलग फाइलों में तोड़ना
    data = json.loads(response.text)
    classes_list = data.get("classes", [])
    
    if not classes_list:
        print("❌ AI ने कोई डेटा नहीं दिया।")
        exit()

    print(f"\n✅ AI ने PDF को {len(classes_list)} भागों (Classes) में बाँट दिया है!")
    
    generated_files = []
    base_name = pdf_filename.replace('.pdf', '') 
    
    for i, class_data in enumerate(classes_list):
        filename = f"{base_name}_part_{i+1}.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(class_data, f, indent=2, ensure_ascii=False)
            
        generated_files.append({"title": class_data.get("subjectTitle", f"Class Part {i+1}"), "file": filename})
        print(f"   💾 सेव हो गई: {filename} ({len(class_data.get('topics', []))} Topics)")

    print("\n==================================================")
    print("🛠️  Index Update Code:")
    for item in generated_files:
        print(f"""    {{
      "title": "{item['title']}",
      "type": "class",
      "url": "https://exam-chacha.pages.dev/{item['file']}"
    }},""")
    print("==================================================")

    # 8. सर्वर से फाइल डिलीट करना
    client.files.delete(name=uploaded_file.name)

except Exception as e:
    print(f"❌ कुछ गड़बड़ हो गई: {e}")