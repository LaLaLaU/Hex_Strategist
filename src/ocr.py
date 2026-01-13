"""OCR 模块 （ step 1.4 )

提供：
-recognize_text(image_path) -> str:返回图片中识别到的文本（拼接后的字符串）
"""


from functools import lru_cache
from paddleocr import PaddleOCR

@lru_cache(maxsize=1)
def _get_ocr() -> PaddleOCR:
    """初始化 PaddleOCR 3.x Pipeline 
    使用PP-OCRv5_mobile_det检测模型、PP-OCRv5_mobile_rec识别两个轻量模型
    实例化教程来自于官方文档“快速开始” https://www.paddleocr.ai/latest/quick_start.html#_2
    ，并缓存，避免每次调用都重新加载模型"""
    return PaddleOCR(
        text_detection_model_name="PP-OCRv5_mobile_det",
        text_recognition_model_name="PP-OCRv5_mobile_rec",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        device = 'gpu',
    )

def recognize_text(image_path:str) -> str:
   """识别图片中的文本，返回拼接后的字符串"""
   ocr = _get_ocr()
   result = ocr.predict(image_path)

   texts: list[str] = []

   # 文档输出示例：每个元素像{'res':{...}}
   for item in result or []:
       if not isinstance(item,dict):
           continue

       rec_texts = item.get("rec_texts")

       if isinstance(rec_texts,list):
           for t in rec_texts:
               s = str(t).strip()
               if s:
                   texts.append(s)
   return "".join(texts).strip()
