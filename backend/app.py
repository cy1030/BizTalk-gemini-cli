import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# 모든 출처에서 /api/* 경로에 대한 CORS 허용
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Groq 클라이언트 초기화 (1단계에서는 실제 API 호출 대신 더미 데이터를 사용하므로, 키가 없어도 동작 가능)
# 실제 연동 시에는 API 키가 필요합니다.
try:
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        print("Warning: GROQ_API_KEY environment variable not set. Real API calls will fail.")
    client = Groq(api_key=groq_api_key)
except Exception as e:
    print(f"Error initializing Groq client: {e}")
    client = None

@app.route('/api/convert', methods=['POST'])
def convert_text():
    """
    사용자의 텍스트를 받아서 업무용 말투로 변환하는 API 엔드포인트.
    1단계에서는 실제 변환 로직 대신 더미 응답을 반환합니다.
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'target' not in data:
            return jsonify({"error": "Missing 'text' or 'target' in request"}), 400

        original_text = data.get('text')
        target = data.get('target')

        # 1단계: 더미 변환 로직
        # 실제 Groq API를 호출하는 대신, 선택된 대상에 따라 미리 정의된 더미 텍스트를 반환합니다.
        dummy_converted_text = f"'{original_text}'에 대한 '{target}' 대상의 더미 변환 결과입니다. 2단계에서 실제 변환 기능이 구현될 예정입니다."

        response_data = {
            "original_text": original_text,
            "converted_text": dummy_converted_text,
            "target": target
        }

        return jsonify(response_data)

    except Exception as e:
        # 오류 로깅 (실제 프로덕션에서는 더 정교한 로깅 시스템 사용)
        print(f"An error occurred: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    서버의 상태를 확인하는 헬스 체크 엔드포인트.
    """
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    # Vercel 환경에서는 gunicorn과 같은 WSGI 서버가 app 객체를 직접 실행하므로,
    # 이 부분은 로컬 개발 시에만 사용됩니다.
    app.run(debug=True, port=5000)
