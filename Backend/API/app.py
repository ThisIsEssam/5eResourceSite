from flask import Flask, jsonify, request
from flask_cors import CORS
from getResource import get_backgrounds 
from LLM import LLM_Class, LLM_Worker

app = Flask(__name__)
CORS(app)
@app.route('/api/backgrounds', methods=['GET'])
def backgrounds():
    background = request.args.get('background', '')
    data = get_backgrounds(background)
    return jsonify(data)

@app.route("/api/llm", methods=["POST"])
def llm():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        chat_history = data.get("chat_history", [])

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        response, updated_chat_history = LLM_Worker.get_llm_response(prompt, chat_history)
        return jsonify({
            "response": response,
            "chat_history": updated_chat_history
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)




