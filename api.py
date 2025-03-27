import os

from app.core.bk_asr.asr_data import ASRData
from app.core.entities import SubtitleConfig
from app.core.subtitle_processor.run import run

os.environ["OPENAI_BASE_URL"] = base_url
os.environ["OPENAI_API_KEY"] = api_key

if __name__ == "__main__":
	config = SubtitleConfig(
		# 翻译配置
		#base_url=base_url,
		#api_key=api_key,
		llm_model=llm_model,
		#deeplx_endpoint=cfg.deeplx_endpoint.value,
		# 翻译服务
		#translator_service=cfg.translator_service.value,
		# 字幕处理
		#split_type=SplitTypeEnum.SENTENCE,
		#split_type="sentence",
		split_type="semantic",
		need_reflect=True,
		need_translate=True,
		need_optimize=True,
		thread_num=3,
		#batch_size=cfg.batch_size.value,
		# 字幕布局、样式
		subtitle_layout="译文在上", #["原文在上", "译文在上", "仅原文", "仅译文"]
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
	subtitle_path = "1.srt"
	asr_data = run(
		subtitle_path=subtitle_path,
		config=config,
		callback=print,
	)
	
	save_path = subtitle_path+".zh.srt"
	asr_data.save(
		save_path=save_path,
		ass_style=config.subtitle_style,
		layout=config.subtitle_layout,
	)
	print(asr_data.to_json())
	#logger.info(f"字幕保存到 {save_path}")
