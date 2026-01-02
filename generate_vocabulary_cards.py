#!/usr/bin/env python3
"""
Vocabulary Card Generator for moin-journo project
Generates printable vocabulary cards from markdown files
Version 5.0 - Wide format with Origin field support
"""

from PIL import Image, ImageDraw, ImageFont
import re
import os
import sys
from pathlib import Path

class VocabularyCardGenerator:
    def __init__(self, output_dir="vocabulary_cards"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Image settings - WIDER format
        self.width = 1000
        self.height = 500
        self.bg_color = (255, 255, 255)
        self.text_color = (50, 50, 50)
        self.highlight_color = (41, 128, 185)
        self.origin_color = (150, 150, 150)  # Light gray for origin
        
        # Load fonts
        self._load_fonts()
    
    def _load_fonts(self):
        """Load fonts with fallback options"""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        try:
            self.font_large = ImageFont.truetype(font_paths[0], 80)
            self.font_medium = ImageFont.truetype(font_paths[1], 40)
            self.font_small = ImageFont.truetype(font_paths[1], 24)
            self.font_tiny = ImageFont.truetype(font_paths[1], 20)
        except:
            print("⚠️  Using default fonts (install DejaVu fonts for better results)")
            self.font_large = ImageFont.load_default()
            self.font_medium = ImageFont.load_default()
            self.font_small = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()
    
    def parse_markdown_file(self, filepath):
        """Parse a markdown file and extract vocabulary entries"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entries = []
        # Updated pattern to capture Origin field (optional)
        pattern = r'##\s+([^\n]+?)\s*(?:\((\d+\.?)\))?\s*\n\s*\*\*Lautsprache:\*\*\s*\[([^\]]+)\]\s*\n\s*(?:\*\*Origin:\*\*\s*([^\n]+?)\s*\n)?\s*\*\*Bedeutung:\*\*\s*([^\n]+?)(?:\s*\n\s*\*\*Language:\*\*\s*([A-Z]{2}))?'
        
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            word = match.group(1).strip()
            number = match.group(2) if match.group(2) else "1"
            pronunciation = match.group(3).strip()
            origin = match.group(4).strip() if match.group(4) else ""
            meaning = match.group(5).strip()
            language = match.group(6).strip().upper() if match.group(6) else "DE"
            
            # Extract article and clean word
            article_match = re.match(r'(der|die|das|ein|eine)\s+(.+)', word, re.IGNORECASE)
            if article_match:
                article = article_match.group(1)
                clean_word = article_match.group(2)
            else:
                article = ""
                clean_word = word
            
            entries.append({
                'word': clean_word,
                'article': article,
                'pronunciation': pronunciation,
                'origin': origin,
                'meaning': meaning,
                'language': language,
                'number': number
            })
        
        return entries
    
    def create_card(self, entry, output_filename):
        """Create a wide vocabulary card image with origin"""
        img = Image.new('RGB', (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw top info (pronunciation) - CENTERED
        top_info = f"[{entry['pronunciation']}]"
        bbox = draw.textbbox((0, 0), top_info, font=self.font_small)
        text_width = bbox[2] - bbox[0]
        draw.text(((self.width - text_width) / 2, 30), top_info, fill=self.text_color, font=self.font_small)
        
        # Draw top separator line
        draw.line([(120, 105), (self.width - 120, 105)], fill=self.text_color, width=2)
        
        # Draw main word with origin - CENTERED
        word_text = entry['word']
        article = entry.get('article', '')
        origin = entry.get('origin', '')
        
        # Calculate centered position for article + word + origin
        bbox_article = draw.textbbox((0, 0), article + " " if article else "", font=self.font_large)
        article_width = bbox_article[2] - bbox_article[0]
        
        bbox_word = draw.textbbox((0, 0), word_text, font=self.font_large)
        word_width = bbox_word[2] - bbox_word[0]
        
        # Origin in smaller font and gray
        origin_text = f" ({origin})" if origin else ""
        bbox_origin = draw.textbbox((0, 0), origin_text, font=self.font_medium)
        origin_width = bbox_origin[2] - bbox_origin[0]
        
        total_width = article_width + word_width + origin_width
        start_x = (self.width - total_width) / 2
        
        # Draw article in black (if exists)
        current_x = start_x
        if article:
            draw.text((current_x, 130), article, fill=self.text_color, font=self.font_large)
            current_x += article_width
        
        # Draw word in blue
        draw.text((current_x, 130), word_text, fill=self.highlight_color, font=self.font_large)
        current_x += word_width
        
        # Draw origin in light gray (slightly lower to align)
        if origin:
            draw.text((current_x, 145), origin_text, fill=self.origin_color, font=self.font_medium)
        
        # Draw middle separator line
        draw.line([(120, 250), (self.width - 120, 250)], fill=self.text_color, width=2)
        
        # Draw meaning (wrapped and centered)
        meaning_lines = self._wrap_text(entry['meaning'], self.font_small, self.width - 240)
        y_pos = 285
        for line in meaning_lines[:5]:  # Max 5 lines
            bbox = draw.textbbox((0, 0), line, font=self.font_small)
            line_width = bbox[2] - bbox[0]
            x_centered = (self.width - line_width) / 2
            draw.text((x_centered, y_pos), line, fill=self.text_color, font=self.font_small)
            y_pos += 35
        
        # Draw bottom separator line
        draw.line([(120, self.height - 70), (self.width - 120, self.height - 70)], fill=self.text_color, width=2)
        
        # Draw footer - CENTERED
        footer_text = "moin-journo · CC BY-SA 4.0"
        bbox = draw.textbbox((0, 0), footer_text, font=self.font_tiny)
        text_width = bbox[2] - bbox[0]
        draw.text(((self.width - text_width) / 2, self.height - 50), footer_text, fill=(120, 120, 120), font=self.font_tiny)
        
        # Save image
        img.save(output_filename)
        return output_filename
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def process_file(self, markdown_file):
        """Process a single markdown file"""
        print(f"\n📖 Processing: {markdown_file}")
        entries = self.parse_markdown_file(markdown_file)
        
        if not entries:
            print(f"  ⚠️  No vocabulary entries found")
            return []
        
        output_files = []
        for i, entry in enumerate(entries, 1):
            # Create safe filename
            safe_word = re.sub(r'[^a-zA-Z0-9äöüÄÖÜß]', '_', entry['word'])
            output_filename = os.path.join(self.output_dir, f"{safe_word}_{entry['number']}.png")
            
            self.create_card(entry, output_filename)
            output_files.append(output_filename)
            
            origin_display = f" (Origin: {entry['origin']})" if entry['origin'] else ""
            print(f"  ✓ Created: {output_filename}{origin_display}")
        
        return output_files
    
    def process_directory(self, directory):
        """Process all markdown files in a directory"""
        directory = Path(directory)
        markdown_files = list(directory.glob("*.md")) + list(directory.glob("**/*.md"))
        
        if not markdown_files:
            print(f"❌ No markdown files found in {directory}")
            return []
        
        print(f"\n🔍 Found {len(markdown_files)} markdown file(s)")
        
        all_output_files = []
        for md_file in markdown_files:
            output_files = self.process_file(md_file)
            all_output_files.extend(output_files)
        
        return all_output_files

def main():
    """Main entry point"""
    print("=" * 60)
    print("📚 moin-journo Vocabulary Card Generator v5.0")
    print("🎨 Wide Format with Origin Support")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  python generate_vocabulary_cards.py <markdown_file_or_directory>")
        print("\nExample:")
        print("  python generate_vocabulary_cards.py moin-kw-kalender-2026.md")
        print("  python generate_vocabulary_cards.py ./moin-journo/")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    # Create generator
    generator = VocabularyCardGenerator()
    
    # Process input
    if os.path.isfile(input_path):
        output_files = generator.process_file(input_path)
    elif os.path.isdir(input_path):
        output_files = generator.process_directory(input_path)
    else:
        print(f"❌ Error: {input_path} not found")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Success! Created {len(output_files)} vocabulary cards")
    print(f"📁 Output directory: {generator.output_dir}")
    print(f"📐 Card size: {generator.width}x{generator.height} pixels")
    print("=" * 60)

if __name__ == "__main__":
    main()
