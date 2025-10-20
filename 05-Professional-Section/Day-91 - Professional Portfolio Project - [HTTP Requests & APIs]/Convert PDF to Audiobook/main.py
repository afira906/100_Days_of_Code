import PyPDF2
import requests
import os
from pathlib import Path


class PDFToAudiobook:
    def __init__(self):
        self.output_dir = "audiobooks"
        os.makedirs(self.output_dir, exist_ok=True)

    def extract_text_from_pdf(self, pdf_path):
        """Extract and clean text from PDF"""
        print("📖 Extracting text from PDF...")
        text = ""

        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                for page_num, page in enumerate(pdf_reader.pages, 1):
                    print(f"Processing page {page_num}...")
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return None

        return text.strip()

    def text_to_speech(self, text, output_filename):
        """Convert text to speech using free TTS API"""
        print("🎵 Converting to speech...")

        # Split text into chunks (API limit)
        chunks = self._split_text(text, max_chars=1000)
        audio_files = []

        for i, chunk in enumerate(chunks):
            print(f"Creating audio part {i + 1}/{len(chunks)}...")

            # Use Google Translate's TTS (free, no API key)
            tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl=en&q={chunk}&client=tw-ob"

            try:
                response = requests.get(tts_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })

                if response.status_code == 200:
                    audio_path = os.path.join(self.output_dir, f"{output_filename}_part{i + 1}.mp3")
                    with open(audio_path, 'wb') as f:
                        f.write(response.content)
                    audio_files.append(audio_path)
                else:
                    print(f"❌ Error with part {i + 1}")

            except Exception as e:
                print(f"❌ API error: {e}")

        return audio_files

    def _split_text(self, text, max_chars=1000):
        """Split text into chunks without breaking words"""
        chunks = []
        words = text.split()
        current_chunk = ""

        for word in words:
            if len(current_chunk) + len(word) + 1 <= max_chars:
                current_chunk += word + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = word + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def convert(self, pdf_path):
        """Main conversion method"""
        if not os.path.exists(pdf_path):
            print("❌ PDF file not found!")
            return

        # Get PDF filename without extension
        filename = Path(pdf_path).stem

        # Extract text
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            return

        print(f"✅ Extracted {len(text)} characters")

        # Convert to speech
        audio_files = self.text_to_speech(text, filename)

        if audio_files:
            print(f"\n🎉 Audiobook created successfully!")
            print(f"📁 Files saved in: {self.output_dir}/")
            print(f"🎵 Total parts: {len(audio_files)}")
        else:
            print("❌ Failed to create audiobook")


# Simple usage
if __name__ == "__main__":
    converter = PDFToAudiobook()

    # Ask user for PDF file path
    pdf_path = input("Enter the path to your PDF file: ").strip().strip('"')

    # Convert PDF to audiobook
    converter.convert(pdf_path)

    input("\nPress Enter to exit...")
