import os
import google.generativeai as genai

os.environ['GEMINI_API_KEY'] = "AIzaSyAiGNKEwwj0PnZL05yoxdUlU62cGaJgV1s"
os.environ['GOOGLE_API_KEY'] = os.environ['GEMINI_API_KEY']
print('key set?', bool(os.environ['GEMINI_API_KEY']))

system_instruction = 'You are a motivational chatbot. Always be positive.'

try:
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    print('genai module has list_models?', hasattr(genai, 'list_models'))
    if hasattr(genai, 'list_models'):
        models = genai.list_models()
        print('available models (first 5):')
        for i, m in enumerate(models):
            if i >= 5:
                break
            print('  ', m)

    # Use a supported model for generate_content
    model = genai.GenerativeModel('models/gemini-2.5-flash', system_instruction=system_instruction)
    print('model created', model)
    resp = model.generate_content('Hello, how are you?')
    print('resp', resp)
    print('resp.text', getattr(resp, 'text', None))
except Exception as e:
    import traceback; traceback.print_exc()
