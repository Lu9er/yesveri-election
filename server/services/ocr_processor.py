import io

from PIL import Image


class OCRProcessor:
    """Extract text from images using Tesseract OCR."""

    def __init__(self, tesseract_cmd: str = "/usr/bin/tesseract"):
        try:
            import pytesseract

            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            self._pytesseract = pytesseract
            self._available = True
        except ImportError:
            self._available = False

    def extract_text(self, image_bytes: bytes) -> str:
        if not self._available:
            raise RuntimeError(
                "pytesseract is not installed. Install it with: pip install pytesseract"
            )

        image = Image.open(io.BytesIO(image_bytes))

        # Convert to grayscale for better OCR accuracy
        image = image.convert("L")

        # Resize if very large (improves speed without hurting accuracy much)
        max_dim = 2000
        if max(image.size) > max_dim:
            ratio = max_dim / max(image.size)
            new_size = (int(image.width * ratio), int(image.height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)

        text = self._pytesseract.image_to_string(image, lang="eng")
        return text.strip()
