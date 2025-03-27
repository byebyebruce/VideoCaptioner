from pathlib import Path
from typing import Callable, Dict, Optional

from app.core.bk_asr.asr_data import ASRData
from app.core.entities import SubtitleConfig
from app.core.subtitle_processor.optimize import SubtitleOptimizer
from app.core.subtitle_processor.split import SubtitleSplitter
from app.core.subtitle_processor.translate import (TranslatorFactory,
                                                   TranslatorType)
from app.core.utils.logger import setup_logger

logger = setup_logger("subtitle_processor")


def run_fromfile(
    subtitle_path: str,
    config: SubtitleConfig,
    callback: Optional[Callable[[Dict], None]] = None,
) -> ASRData:
        # 1. 加载字幕文件
    asr_data = ASRData.from_subtitle_file(subtitle_path)
    return run(asr_data, config, callback)

def run(
    asr_data: ASRData,
    config: SubtitleConfig,
    callback: Optional[Callable[[Dict], None]] = None,
) -> ASRData:
    """
    运行字幕处理流程

    Args:
        subtitle_path: 字幕文件路径
        config: 字幕处理配置
        callback: 回调函数，用于更新进度

    Returns:
        ASRData: 处理后的字幕数据
    """
    logger.info(f"\n===========字幕处理任务开始===========")



    # 2. 如果需要分割字幕
    # 检查是否需要合并重新断句
    if config.need_split:
        asr_data.split_to_word_segments()

    if asr_data.is_word_timestamp():
        logger.info("正在进行字幕断句...")
        splitter = SubtitleSplitter(
            thread_num=config.thread_num,
            model=config.llm_model,
            temperature=0.3,
            timeout=60,
            retry_times=1,
            split_type=config.split_type,
            max_word_count_cjk=config.max_word_count_cjk,
            max_word_count_english=config.max_word_count_english,
        )

        asr_data = splitter.split_subtitle(asr_data)
        #asr_data.save(save_path=split_path)
        #self.update_all.emit(asr_data.to_json())

    # 3. 优化字幕
    if config.need_optimize:
        logger.info("正在优化字幕...")
        optimizer = SubtitleOptimizer(
            #custom_prompt=custom_prompt,
            model=config.llm_model,
            batch_num=config.batch_size,
            thread_num=config.thread_num,
            #update_callback=self.callback,
        )
        asr_data = optimizer.optimize_subtitle(asr_data)
        #asr_data.save(save_path=subtitle_path+".opt.srt")
        #self.update_all.emit(asr_data.to_json())

    # 4. 翻译字幕

    if config.need_translate:
        #self.progress.emit(0, self.tr("翻译字幕..."))
        logger.info("正在翻译字幕...")
        #self.finished_subtitle_length = 0  # 重置计数器
        #os.environ["DEEPLX_ENDPOINT"] = config.deeplx_endpoint
        translator = TranslatorFactory.create_translator(
            translator_type=TranslatorType.OPENAI,
            thread_num=config.thread_num,
            batch_num=config.batch_size,
            target_language=config.target_language,
            model=config.llm_model,
            #custom_prompt=custom_prompt,
            is_reflect=config.need_reflect,
            #update_callback=self.callback,
        )
        asr_data = translator.translate_subtitle(asr_data)
        # 移除末尾标点符号
        if config.need_remove_punctuation:
            asr_data.remove_punctuation()
        #self.update_all.emit(asr_data.to_json())
        # 保存翻译结果(单语、双语)
        
        """
        if self.task.need_next_task and self.task.video_path:
            for subtitle_layout in ["原文在上", "译文在上", "仅原文", "仅译文"]:
                save_path = str(
                    Path(self.task.subtitle_path).parent
                    / f"{Path(self.task.video_path).stem}-{subtitle_layout}.srt"
                )
                asr_data.save(
                    save_path=save_path,
                    ass_style=config.subtitle_style,
                    layout=subtitle_layout,
                )
                logger.info(f"字幕保存到 {save_path}")
        """

    return asr_data
