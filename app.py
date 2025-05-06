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
        company_name = data.get('company_name', 'a company')
        project = data.get('project', 'relevant projects')
        experience_level = data.get('experience_level', 'mid-level')
        
        if not job_role:
            return jsonify({'error': 'Job role is required'}), 400
        
        prompt = f"""
        You are an expert interview coach. Generate 5 common interview questions for a {experience_level} 
        {job_role} position at {company_name}. The candidate has experience with {project}.
        
        Make sure the questions are:
        1. Relevant to {company_name}'s likely needs
        2. Tailored to the {job_role} position
        3. Cover technical skills, behavioral situations, and problem-solving
        4. Consider the candidate's background in {project}
        
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
        company_name = data.get('company_name', '')
        project = data.get('project', '')
        context = data.get('context', '')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
        
        # prompt = f"""
        # You are helping a candidate prepare for a {job_role} position at {company_name}.
        # The candidate has experience with {project} and provided this context: {context}
        
        # Provide a comprehensive answer to this interview question:
        # Question: {question}
        
        # The answer should:
        # 1. Be tailored for {company_name}
        # 2. Highlight relevant experience with {project}
        # 3. Be concise but detailed (2-3 paragraphs)
        # 4. Include specific examples
        # 5. Use professional language
        
        # Answer:
        # """
        prompt = f"""
        **Role**: You're a senior {job_role} interviewing at {company_name}. 
        **Task**: Answer this question: "{question}" 

        **Context**:
        - Company Research: {company_name} is known for: [AI will insert relevant facts]
        - My Project: {project} ({context})
        - Job Requirements: {job_role} needs [AI will infer key skills]

        **Answer Requirements**:
        1. **Company Alignment**:
        - Open with how your experience relates to {company_name}'s mission/products
        - Use 1-2 facts about the company's tech stack/approach if known
        - Example: "At {company_name} where [specific observation], I..."

        2. **Project Demonstration**:
        - Use {project} as your primary case study
        - Include:
            - Technical specifics ("Used TensorFlow to...")
            - Quantifiable impact ("Improved efficiency by 30%...")
            - Lessons learned

        3. **Role-Specific**:
        - Highlight 3 {job_role} core competencies
        - Show progression from junior to senior thinking

        4. **Structure**:
        - 1-2 paragraphs max
        - STAR method (Situation-Task-Action-Result)
        - Action verbs: "Architected", "Optimized", "Led"

        **Example Framework**:
        "As [Company] emphasizes [value], my work on [Project] required [skill]. 
        When faced with [challenge], I [action] using [tech], resulting in [metric] improvement. 
        This experience directly applies to your [specific team/product] because..." 

        **Generate Answer**: 
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