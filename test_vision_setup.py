"""
Test script to verify Visualization Converter dependencies are installed correctly
"""

def test_installations():
    print("=" * 60)
    print("Testing Visualization Converter Dependencies")
    print("=" * 60)
    
    # Test OpenAI
    try:
        import openai
        print(f"[OK] OpenAI: {openai.__version__}")
    except ImportError as e:
        print(f"[FAIL] OpenAI: Not installed - {e}")
        return False
    
    # Test OpenCV
    try:
        import cv2
        print(f"[OK] OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"[FAIL] OpenCV: Not installed - {e}")
        return False
    
    # Test Pytesseract
    try:
        import pytesseract
        print(f"[OK] Pytesseract: {pytesseract.__version__}")
    except ImportError as e:
        print(f"[FAIL] Pytesseract: Not installed - {e}")
        return False
    
    # Test NumPy
    try:
        import numpy as np
        print(f"[OK] NumPy: {np.__version__}")
    except ImportError as e:
        print(f"[FAIL] NumPy: Not installed - {e}")
        return False
    
    # Test Magic
    try:
        import magic
        print(f"[OK] Python-magic-bin: Installed")
    except ImportError as e:
        print(f"[FAIL] Python-magic-bin: Not installed - {e}")
        return False
    
    # Test Pillow (already installed)
    try:
        from PIL import Image
        import PIL
        print(f"[OK] Pillow: {PIL.__version__}")
    except ImportError as e:
        print(f"[FAIL] Pillow: Not installed - {e}")
        return False
    
    print("\n" + "=" * 60)
    print("SUCCESS: All dependencies installed successfully!")
    print("=" * 60)
    
    print("\nIMPORTANT NEXT STEPS:")
    print("1. Get OpenAI API key from: https://platform.openai.com/api-keys")
    print("2. Set environment variable: OPENAI_API_KEY=sk-your-key")
    print("3. Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki")
    print("\nSee VISUALIZATION_SETUP.md for detailed instructions")
    
    return True

if __name__ == "__main__":
    test_installations()
