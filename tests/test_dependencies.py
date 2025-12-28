def test_import_mss():
    import mss
    assert mss is not None
    print ("✅ mss 导入成功")
def test_import_pillow():
    from PIL import Image
    assert Image is not None
    print ("✅ pillow 导入成功")
def test_import_paddleocr():
    from paddleocr import PaddleOCR
    assert PaddleOCR is not None
    print ("✅ paddleocr 导入成功")
def test_import_imagehash():
    import imagehash
    assert imagehash is not None
    print ("✅ imagehash 导入成功")
def test_import_keyboard():
    import keyboard
    assert keyboard is not None
    print ("✅ keyboard 导入成功")


if __name__ == "__main__":
    test_import_mss()
    test_import_pillow()
    test_import_paddleocr()
    test_import_imagehash()
    test_import_keyboard()
    