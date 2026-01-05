from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False, 
    use_doc_unwarping=False, 
    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="PP-OCRv5_mobile_rec",
    device="cpu",
    use_textline_orientation=False) # 文本检测+文本识别
# ocr = PaddleOCR(use_doc_orientation_classify=True, use_doc_unwarping=True) # 文本图像预处理+文本检测+方向分类+文本识别
# ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False) # 文本检测+文本行方向分类+文本识别
# ocr = PaddleOCR(

#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False) # 更换 PP-OCRv5_mobile 模型
result = ocr.predict("./output/roi/capture_20260103_225336.png_roi_hex_name_1.png")
for res in result:
    res.print()
    res.save_to_img("output")
    res.save_to_json("output")