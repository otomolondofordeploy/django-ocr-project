import ocrmypdf
import requests
from pathlib import Path
from typing import Optional, Union
import os


class OCRProcessor:
    """
    Class xử lý OCR cho cả file ảnh và PDF
    Hỗ trợ download từ URL hoặc xử lý file local
    """
    
    SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    SUPPORTED_PDF_FORMAT = ['.pdf']
    
    def __init__(self, output_dir: str = "output"):
        """
        Khởi tạo OCR Processor
        
        Args:
            output_dir: Thư mục lưu output (mặc định: 'output')
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def download_file(self, url: str, save_path: Optional[str] = None) -> str:
        """
        Download file từ URL
        
        Args:
            url: URL của file cần download
            save_path: Đường dẫn lưu file (optional)
            
        Returns:
            Đường dẫn file đã download
        """
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            if save_path is None:
                filename = url.split('/')[-1]
                save_path = self.output_dir / filename
            
            with open(save_path, "wb") as f:
                f.write(response.content)
            
            print(f"✅ Download thành công: {save_path}")
            return str(save_path)
            
        except Exception as e:
            print(f"❌ Lỗi khi download: {e}")
            raise
    
    def _is_image(self, file_path: str) -> bool:
        """Kiểm tra file có phải ảnh không"""
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_IMAGE_FORMATS
    
    def _is_pdf(self, file_path: str) -> bool:
        """Kiểm tra file có phải PDF không"""
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_PDF_FORMAT
    
    def process_image(self, 
                     image_path: str, 
                     output_path: Optional[str] = None,
                     **ocr_kwargs) -> str:
        """
        Xử lý OCR cho ảnh (chuyển thành PDF có thể search)
        
        Args:
            image_path: Đường dẫn ảnh input
            output_path: Đường dẫn PDF output (optional)
            **ocr_kwargs: Tham số bổ sung cho ocrmypdf
            
        Returns:
            Đường dẫn file PDF output
        """
        if not self._is_image(image_path):
            raise ValueError(f"File không phải ảnh: {image_path}")
        
        if output_path is None:
            base_name = Path(image_path).stem
            output_path = self.output_dir / f"{base_name}_OCR.pdf"
        
        # Merge default params với user params
        default_params = {
            'deskew': True,
            'progress_bar': True,
            'rotate_pages': True,
            'remove_background': False
        }
        params = {**default_params, **ocr_kwargs}
        
        print(f"🔄 Đang xử lý OCR ảnh: {image_path}")
        ocrmypdf.ocr(image_path, output_path, **params)
        print(f"✅ OCR ảnh xong: {output_path}")
        
        return str(output_path)
    
    def process_pdf(self, 
                   pdf_path: str, 
                   output_path: Optional[str] = None,
                   **ocr_kwargs) -> str:
        """
        Xử lý OCR cho PDF
        
        Args:
            pdf_path: Đường dẫn PDF input
            output_path: Đường dẫn PDF output (optional)
            **ocr_kwargs: Tham số bổ sung cho ocrmypdf
            
        Returns:
            Đường dẫn file PDF output
        """
        if not self._is_pdf(pdf_path):
            raise ValueError(f"File không phải PDF: {pdf_path}")
        
        if output_path is None:
            base_name = Path(pdf_path).stem
            output_path = self.output_dir / f"{base_name}_OCR.pdf"
        
        # Merge default params với user params
        default_params = {
            'deskew': True,
            'progress_bar': True,
            'rotate_pages': True,
            'remove_background': False
        }
        params = {**default_params, **ocr_kwargs}
        
        print(f"🔄 Đang xử lý OCR PDF: {pdf_path}")
        ocrmypdf.ocr(pdf_path, output_path, **params)
        print(f"✅ OCR PDF xong: {output_path}")
        
        return str(output_path)
    
    def process_file(self, 
                    file_path: str, 
                    output_path: Optional[str] = None,
                    **ocr_kwargs) -> str:
        """
        Tự động detect và xử lý OCR cho ảnh hoặc PDF
        
        Args:
            file_path: Đường dẫn file input
            output_path: Đường dẫn file output (optional)
            **ocr_kwargs: Tham số bổ sung cho ocrmypdf
            
        Returns:
            Đường dẫn file output
        """
        if self._is_image(file_path):
            return self.process_image(file_path, output_path, **ocr_kwargs)
        elif self._is_pdf(file_path):
            return self.process_pdf(file_path, output_path, **ocr_kwargs)
        else:
            raise ValueError(f"Định dạng file không được hỗ trợ: {file_path}")
    
    def process_from_url(self, 
                        url: str, 
                        output_path: Optional[str] = None,
                        **ocr_kwargs) -> str:
        """
        Download và xử lý OCR file từ URL
        
        Args:
            url: URL của file
            output_path: Đường dẫn file output (optional)
            **ocr_kwargs: Tham số bổ sung cho ocrmypdf
            
        Returns:
            Đường dẫn file output
        """
        # Download file
        downloaded_path = self.download_file(url)
        
        # Xử lý OCR
        return self.process_file(downloaded_path, output_path, **ocr_kwargs)


# ==================== CÁCH SỬ DỤNG ====================

# if __name__ == "__main__":
#     # Khởi tạo processor
#     processor = OCRProcessor(output_dir="output")
    
#     # Example 1: Xử lý PDF từ URL (code gốc của bạn)
#     print("\n=== Example 1: PDF từ URL ===")
#     url = "https://github.com/fraponyo94/Text-Extraction-Scanned-Pdf/raw/master/sample-scanned-pdfs/pdf_sample2.pdf"
#     output = processor.process_from_url(url)
    
#     # Example 2: Xử lý PDF local
#     print("\n=== Example 2: PDF local ===")
#     # output = processor.process_pdf("sample.pdf")
    
#     # Example 3: Xử lý ảnh local
#     print("\n=== Example 3: Ảnh local ===")
#     # output = processor.process_image("scanned_document.jpg")
    
#     # Example 4: Tự động detect file type
#     print("\n=== Example 4: Auto-detect ===")
#     # output = processor.process_file("document.pdf")
#     # output = processor.process_file("image.png")
    
#     # Example 5: Custom parameters
#     print("\n=== Example 5: Custom params ===")
#     # output = processor.process_pdf(
#     #     "sample.pdf",
#     #     output_path="custom_output.pdf",
#     #     deskew=True,
#     #     rotate_pages=True,
#     #     remove_background=True,
#     #     optimize=3
#     # )