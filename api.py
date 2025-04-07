import json
import os
import sys

from dotenv import load_dotenv  # Import dotenv to load .env file
from flask import Flask, jsonify, request

from app.core.bk_asr.asr_data import ASRData
from app.core.entities import SubtitleConfig
from app.core.subtitle_processor.run import run

# Load environment variables from .env file
load_dotenv(override=True)

# Read environment variables
base_url = os.getenv("OPENAI_BASE_URL", "http://default-base-url.com/v1")
api_key = os.getenv("OPENAI_API_KEY", "default-api-key")
llm_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
thread_num = int(os.getenv("THREAD_NUM", 3))
print("thread_num=", thread_num)

if not base_url or not api_key:
    raise ValueError("OPENAI_BASE_URL and OPENAI_API_KEY must be set in the environment")

# Initialize Flask app
app = Flask(__name__)

def gen_srt(asr_data) -> ASRData:
    config = SubtitleConfig(
        # 翻译配置
		#base_url=base_url,
		#api_key=api_key,
		llm_model=llm_model,
		#deeplx_endpoint=cfg.deeplx_endpoint.value,
		# 翻译服务
		#translator_service=cfg.translator_service.value,
		# 字幕处理
		split_type="semantic", #"sentence"
		need_reflect=True,
		need_translate=True,
		need_optimize=True,
		thread_num=thread_num,
		#batch_size=cfg.batch_size.value,
		# 字幕布局、样式
		#subtitle_layout="译文在上", #["原文在上", "译文在上", "仅原文", "仅译文"]
		#subtitle_style=TaskFactory.get_subtitle_style(
		#	cfg.subtitle_style_name.value
		#),
		# 字幕分割
		#max_word_count_cjk=cfg.max_word_count_cjk.value,
		#max_word_count_english=cfg.max_word_count_english.value,
		need_split=True,
		# 字幕翻译
		#target_language=cfg.target_language.value.value,
		# 字幕优化
		#need_remove_punctuation=cfg.needs_remove_punctuation.value,
		# 字幕提示
		#custom_prompt_text=cfg.custom_prompt_text.value,
    )
   
    asr_data = run(
        asr_data=asr_data,
        config=config,
        callback=print,
    )
    return asr_data


@app.route('/translate_srt', methods=['POST'])
def generate_srt():
    try:
        data = request.get_data().decode('utf-8')

        asr_data = ASRData.from_srt(data)

        # Call gen_srt function
        asr_data = gen_srt(asr_data)

        # Return the result as plain text (SRT format)
        return asr_data.to_srt(), 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def process_local_srt(file_path):
    try:
        # Read the SRT file
        with open(file_path, 'r', encoding='utf-8') as file:
            srt_content = file.read()

        # Convert SRT content to JSON format (assuming a utility function exists)
        asr_data = ASRData.from_srt(srt_content)

        # Call gen_srt function
        asr_data = gen_srt(asr_data)

        # Save the result back to an SRT file
        output_path = file_path.replace('.srt', '_processed.srt')
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(asr_data.to_srt())
        output_path = file_path.replace('.srt', '_processed.json')

        print(f"Processed SRT file saved to: {output_path}")
    except Exception as e:
        print(f"Error processing SRT file: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        # If a file path is provided as an argument, process the local SRT file
        process_local_srt(sys.argv[1])
    else:
        # Otherwise, run the Flask server
        app.run(host="0.0.0.0", port=8502)
