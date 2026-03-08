import os
import requests
import random
import textwrap
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from datetime import datetime

class PinguinPinGenerator:
    def __init__(self):
        self.output_dir = "generated_pins"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        
        # We will use _get_font helper to load the font into memory

        # Database of topics for Pinguin-Umzuege!
        self.topics = [
            {
                "title": "5 Tipps für einen stressfreien Umzug in Berlin",
                "description": "Ein Umzug in Berlin kann anstrengend sein – muss er aber nicht! Mit diesen 5 einfachen Tipps von Pinguin Umzüge gelingt Ihr Wohnungswechsel garantiert entspannt. Holt euch jetzt euer unverbindliches Angebot! 🐧📦 #UmzugBerlin #PinguinUmzuege #Umzugstipps",
                "link": "https://www.pinguin-umzuege.de/leistungen/",
                "bg_source": "bg_berlin.png", # The AI image we just generated!
                "is_local": True
            },
            {
                "title": "Kisten packen wie ein Profi",
                "description": "Wie packt man Kartons richtig, ohne dass Gutes kaputt geht? Wir bei Pinguin Umzüge zeigen es Ihnen! Unsere Profi-Packer helfen auf Wunsch auch beim Packen vor Ort. #Umzugstipps #Packen #Berlin",
                "link": "https://www.pinguin-umzuege.de/umzugsmaterial/",
                "bg_source": "https://picsum.photos/id/30/1000/1500",
                "is_local": False
            },
            {
                "title": "Büroumzug ohne Stillstand",
                "description": "Ein Firmenumzug in Berlin erfordert perfekte Planung. Pinguin Umzüge sorgt dafür, dass Ihr Betrieb so schnell wie möglich wieder läuft. Jetzt unverbindliches Angebot für Ihren Büroumzug sichern! #Büroumzug #Firmenumzug #BerlinBusiness",
                "link": "https://www.pinguin-umzuege.de/leistungen/",
                "bg_source": "bg_office.png",
                "is_local": True
            }
        ]

    def _get_font(self, size):
        """Downloads the Roboto font into bytes for PIL to use."""
        try:
            # We fetch a known TTF font directly from Google Fonts repository
            url = "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
            r = requests.get(url)
            r.raise_for_status()
            font_bytes = BytesIO(r.content)
            return ImageFont.truetype(font_bytes, size)
        except Exception as e:
            print(f"Failed to load font '{e}'. Using default.")
            return ImageFont.load_default()

    def download_image(self, url):
        """Downloads an image from a URL and converts it to a PIL Image."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return Image.open(BytesIO(response.content)).convert("RGBA")
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            # Create a solid color fallback image if download fails
            return Image.new("RGBA", (1000, 1500), color=(20, 30, 40))

    def generate_pin_image(self, topic):
        """Generates a high-quality vertical Pinterest image with text overlaid."""
        title = topic["title"]
        source = topic["bg_source"]
        is_local = topic["is_local"]
        
        print(f"Generating Pin image for: '{title}'...")
        
        # 1. Get base image
        if is_local:
            if os.path.exists(source):
                base_img = Image.open(source).convert("RGBA")
            else:
                print(f"Local file {source} not found, using fallback.")
                base_img = Image.new("RGBA", (1000, 1500), color=(20, 30, 40))
        else:
            base_img = self.download_image(source)
        
        # 2. Resize and crop to Pinterest optimal ratio (1000x1500px, 2:3 ratio)
        target_size = (1000, 1500)
        
        # Simple crop/resize logic to fill target size
        width, height = base_img.size
        target_ratio = target_size[0] / target_size[1]
        img_ratio = width / height
        
        if img_ratio > target_ratio:
            # Image is wider than target ratio
            new_width = int(target_ratio * height)
            offset = (width - new_width) // 2
            base_img = base_img.crop((offset, 0, offset + new_width, height))
        else:
            # Image is taller than target ratio
            new_height = int(width / target_ratio)
            offset = (height - new_height) // 2
            base_img = base_img.crop((0, offset, width, offset + new_height))
            
        base_img = base_img.resize(target_size, Image.LANCZOS)
        
        # 3. Add a dark gradient/overlay so white text is readable
        overlay = Image.new("RGBA", target_size, (0, 0, 0, 120)) # Semi-transparent black
        img_with_overlay = Image.alpha_composite(base_img, overlay)
        
        # 4. Add Text
        draw = ImageDraw.Draw(img_with_overlay)
        
        # Load font directly from bytes helper
        font = self._get_font(80)
        brand_font = self._get_font(40)

        # Wrap text and draw
        wrapped_text = textwrap.fill(title, width=18)
        
        # Get text bounding box for centering
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align='center')
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Coordinates for text block (centered)
        x_text = (target_size[0] - text_width) / 2
        y_text = (target_size[1] - text_height) / 2 - 100
        
        # Draw shadow
        draw.multiline_text((x_text+5, y_text+5), wrapped_text, font=font, fill=(0,0,0,180), align='center')
        # Draw main text
        draw.multiline_text((x_text, y_text), wrapped_text, font=font, fill=(255,255,255,255), align='center')
        
        # 5. Add Brand tag at the bottom
        brand_text = "PINGUIN UMZÜGE | BERLIN"
        bbox_brand = draw.textbbox((0, 0), brand_text, font=brand_font)
        brand_w = bbox_brand[2] - bbox_brand[0]
        draw.text(((target_size[0] - brand_w) / 2, target_size[1] - 150), brand_text, font=brand_font, fill=(255, 180, 0, 255)) # Pinguin yellow-orange color
        
        # Convert back to RGB for JPEG saving
        final_img = img_with_overlay.convert("RGB")
        
        # Save output
        timestamp = datetime.now().strftime("%Y%md_%H%M%S")
        safe_title = "".join([c if c.isalnum() else "_" for c in title[:15]])
        filename = f"pin_{safe_title}_{timestamp}.jpg"
        filepath = os.path.join(self.output_dir, filename)
        
        final_img.save(filepath, quality=95)
        print(f"✅ Saved visually optimized Pin to: {filepath}")
        return filepath

    def generate_random_pin(self):
        """Picks a random topic and generates both the content and the image."""
        topic = random.choice(self.topics)
        
        image_path = self.generate_pin_image(topic)
        
        pin_data = {
            "title": topic["title"],
            "description": topic["description"],
            "link": topic["link"],
            "local_image_path": image_path
        }
        
        return pin_data

if __name__ == "__main__":
    print("Initializing Pinguin Pin Generator...")
    generator = PinguinPinGenerator()
    
    print("\nStarting generation of 2 Pins...")
    for i in range(2):
        print(f"\n--- Pin {i+1} ---")
        pin_data = generator.generate_random_pin()
        print("Generated Data:")
        print(f"Title: {pin_data['title']}")
        print(f"Desc:  {pin_data['description'][:60]}...")
        print(f"Image: {pin_data['local_image_path']}")
    
    print("\n✅ Generation complete! Check the 'generated_pins' folder.")
