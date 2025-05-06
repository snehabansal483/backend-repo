from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY set in environment variables")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Function to get the correct model name
def get_generative_model():
    try:
        # List all available models
        available_models = genai.list_models()
        
        # Preferred model names in order of preference
        model_preferences = [
            'models/gemini-1.5-pro-latest',
            'models/gemini-pro',
            'gemini-pro',
            'gemini-1.0-pro'
        ]
        
        # Check which preferred model is available
        for model_name in model_preferences:
            if any(m.name == model_name for m in available_models):
                return genai.GenerativeModel(model_name)
        
        # If no preferred model found, use the first available model that supports generation
        for model in available_models:
            if 'generateContent' in model.supported_generation_methods:
                return genai.GenerativeModel(model.name)
        
        raise ValueError("No suitable generative model found")
    except Exception as e:
        raise ValueError(f"Error finding model: {str(e)}")

# Initialize model
try:
    model = get_generative_model()
except ValueError as e:
    print(f"Model initialization error: {str(e)}")
    exit(1)

def generate_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            return "Error: No response text generated"
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        return f"Error generating response: {str(e)}"


@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    try:
        data = request.json
        job_role = data.get('job_role')
        experience_level = data.get('experience_level', 'mid-level')
        
        if not job_role:
            return jsonify({'error': 'Job role is required'}), 400
        
        prompt = f"""
        You are an expert interview coach. Generate 5 common interview questions for a {experience_level} 
        {job_role} position. Make sure the questions are relevant to the role and cover different aspects 
        like technical skills, behavioral situations, and problem-solving abilities.
        
        Format the questions as a numbered list with one question per line.
        """
        
        questions = generate_with_gemini(prompt)
        return jsonify({'questions': questions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-answer', methods=['POST'])
def generate_answer():
    try:
        data = request.json
        question = data.get('question')
        job_role = data.get('job_role', '')
        context = data.get('context', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        prompt = f"""
        You are an expert interview coach helping a candidate prepare for a {job_role} position.
        The candidate has provided this context about themselves: {context}
        
        Please provide a comprehensive, well-structured answer to the following interview question:
        Question: {question}
        
        The answer should be tailored to the {job_role} position and should:
        1. Be concise but detailed
        2. Include relevant examples if appropriate
        3. Highlight skills and experiences that would be valuable for this role
        4. Use professional language
        
        Answer:
        """
        
        answer = generate_with_gemini(prompt)
        return jsonify({
            'question': question,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)