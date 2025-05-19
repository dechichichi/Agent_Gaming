from flask import Flask, request, jsonify
from agent.agent import GamingAgent

app = Flask(__name__)

# 初始化 Agent
agent = GamingAgent()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction_result = agent.predict(data)
    return jsonify({'prediction': prediction_result})

if __name__ == '__main__':
    app.run(debug=True)