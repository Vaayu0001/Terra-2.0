"""
Terra 2.0 — Meme Generator
Creates eco-themed memes using Pillow.
All templates are generated programmatically — no external images needed.
"""

from io import BytesIO
from datetime import datetime, timezone

from PIL import Image, ImageDraw, ImageFont

from database.db_setup import get_engine, get_session, MemeLog


class EcoMemeGenerator:
    """Generates eco-themed memes using PIL."""

    TEMPLATES = {
        "drake": {
            "name": "Drake Pointing",
            "top_label": "Drake disapproves",
            "bottom_label": "Drake approves",
            "layout": "two_panel_vertical",
        },
        "distracted": {
            "name": "Distracted Boyfriend",
            "labels": ["You", "Bad eco habit", "Planet Earth"],
            "layout": "three_label",
        },
        "this_is_fine": {
            "name": "This Is Fine",
            "layout": "single_panel",
        },
        "change_my_mind": {
            "name": "Change My Mind",
            "layout": "table_sign",
        },
        "always_has_been": {
            "name": "Always Has Been",
            "layout": "astronaut_dialogue",
        },
        "brain_size": {
            "name": "Expanding Brain",
            "layout": "four_panel_vertical",
        },
    }

    ECO_CAPTIONS = {
        "drake": [
            ("Buying bottled water every day", "Carrying a reusable bottle"),
            ("Taking 30-min showers", "5-min power showers"),
            ("Eating beef every meal", "Trying a plant-based lunch"),
            ("Driving alone to college", "Carpooling with friends"),
            ("Fast fashion hauls", "Thrift shopping adventures"),
        ],
        "this_is_fine": [
            ("The planet at 2°C warming", ""),
            ("My carbon footprint results", ""),
            ("Sea levels in 2050", ""),
        ],
        "change_my_mind": [
            ("Gen Z can actually save the planet", ""),
            ("Switching to veggie meals is not that hard", ""),
            ("Thrift stores have better drip than malls", ""),
        ],
        "distracted": [
            ("Me", "Fast fashion sale", "My reusable bag collection"),
            ("Students", "AC at 18°C", "A nice ceiling fan"),
        ],
        "always_has_been": [
            ("Wait, recycling alone won't save us?", "Never has been"),
            ("Wait, the planet is dying?", "Always has been"),
        ],
        "brain_size": [
            ("Using plastic bags", "Reusable bags", "Growing own veggies", "Zero-waste lifestyle"),
            ("Driving everywhere", "Taking the bus", "Cycling", "Walking barefoot on grass"),
        ],
    }

    @staticmethod
    def _get_font(size: int = 24) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Try to load a nice font, fall back to default."""
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\Impact.ttf",
        ]
        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue
        return ImageFont.load_default()

    @staticmethod
    def _draw_text_with_outline(draw: ImageDraw.ImageDraw,
                                 position: tuple,
                                 text: str,
                                 font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                                 fill: tuple = (255, 255, 255),
                                 outline: tuple = (0, 0, 0)):
        """Draw text with outline by drawing in 8 directions."""
        x, y = position
        offsets = [(-2, -2), (-2, 0), (-2, 2), (0, -2),
                   (0, 2), (2, -2), (2, 0), (2, 2)]
        for ox, oy in offsets:
            draw.text((x + ox, y + oy), text, font=font, fill=outline)
        draw.text((x, y), text, font=font, fill=fill)

    @staticmethod
    def _create_base_image(width: int = 600, height: int = 500,
                            bg_color: tuple = (255, 255, 255)) -> Image.Image:
        """Create a base image with given dimensions and color."""
        return Image.new("RGB", (width, height), bg_color)

    @staticmethod
    def _wrap_text(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                   max_width: int, draw: ImageDraw.ImageDraw) -> list:
        """Word-wrap text to fit within max_width."""
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines if lines else [text]

    @staticmethod
    def generate_meme(template_key: str, top_text: str,
                      bottom_text: str) -> Image.Image:
        """
        Generate a meme image based on template layout.
        Returns PIL Image object.
        """
        template = EcoMemeGenerator.TEMPLATES.get(
            template_key,
            EcoMemeGenerator.TEMPLATES["drake"]
        )
        layout = template.get("layout", "two_panel_vertical")

        if layout == "two_panel_vertical":
            return EcoMemeGenerator._generate_drake(top_text, bottom_text)
        elif layout == "three_label":
            return EcoMemeGenerator._generate_distracted(top_text, bottom_text)
        elif layout == "single_panel":
            return EcoMemeGenerator._generate_this_is_fine(top_text, bottom_text)
        elif layout == "table_sign":
            return EcoMemeGenerator._generate_change_my_mind(top_text, bottom_text)
        elif layout == "astronaut_dialogue":
            return EcoMemeGenerator._generate_always_has_been(top_text, bottom_text)
        elif layout == "four_panel_vertical":
            return EcoMemeGenerator._generate_brain_size(top_text, bottom_text)
        else:
            return EcoMemeGenerator._generate_drake(top_text, bottom_text)

    @staticmethod
    def _generate_drake(top_text: str, bottom_text: str) -> Image.Image:
        """Drake-style two panel meme."""
        img = EcoMemeGenerator._create_base_image(600, 500)
        draw = ImageDraw.Draw(img)

        # Top panel (red/disapprove)
        draw.rectangle([(0, 0), (600, 250)], fill=(220, 50, 50))
        draw.rectangle([(0, 0), (150, 250)], fill=(180, 40, 40))

        # Big X for disapprove
        font_big = EcoMemeGenerator._get_font(60)
        draw.text((45, 85), "✋", font=font_big, fill=(255, 255, 255))

        # Bottom panel (green/approve)
        draw.rectangle([(0, 250), (600, 500)], fill=(46, 204, 113))
        draw.rectangle([(0, 250), (150, 500)], fill=(39, 174, 96))

        # Checkmark for approve
        draw.text((45, 335), "👉", font=font_big, fill=(255, 255, 255))

        font = EcoMemeGenerator._get_font(28)

        # Top text
        lines = EcoMemeGenerator._wrap_text(top_text, font, 400, draw)
        y_start = 125 - len(lines) * 18
        for i, line in enumerate(lines):
            EcoMemeGenerator._draw_text_with_outline(
                draw, (180, y_start + i * 36), line, font
            )

        # Bottom text
        lines = EcoMemeGenerator._wrap_text(bottom_text, font, 400, draw)
        y_start = 375 - len(lines) * 18
        for i, line in enumerate(lines):
            EcoMemeGenerator._draw_text_with_outline(
                draw, (180, y_start + i * 36), line, font
            )

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 480), "Terra 2.0 🌍", font=font_small,
                  fill=(255, 255, 255, 180))

        return img

    @staticmethod
    def _generate_distracted(top_text: str, bottom_text: str) -> Image.Image:
        """Distracted boyfriend-style three panel."""
        img = EcoMemeGenerator._create_base_image(600, 400, (45, 74, 62))
        draw = ImageDraw.Draw(img)

        # Three character blocks
        colors_list = [(126, 200, 227), (244, 196, 48), (46, 204, 113)]
        labels_list = ["YOU", top_text or "Bad Habit", bottom_text or "Planet"]

        x_positions = [50, 220, 390]
        font = EcoMemeGenerator._get_font(22)
        font_label = EcoMemeGenerator._get_font(16)

        for i, (x_pos, color, label) in enumerate(
            zip(x_positions, colors_list, labels_list)
        ):
            # Character circle
            draw.ellipse(
                [(x_pos, 80), (x_pos + 130, 210)],
                fill=color, outline=(255, 255, 255), width=3
            )
            # Emoji in circle
            emojis = ["🧑", "🔥", "🌍"]
            font_emoji = EcoMemeGenerator._get_font(40)
            draw.text((x_pos + 35, 120), emojis[i],
                      font=font_emoji, fill=(0, 0, 0))

            # Label below
            lines = EcoMemeGenerator._wrap_text(label, font_label, 150, draw)
            for j, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=font_label)
                text_w = bbox[2] - bbox[0]
                EcoMemeGenerator._draw_text_with_outline(
                    draw,
                    (x_pos + 65 - text_w // 2, 230 + j * 22),
                    line, font_label
                )

        # Arrow from person to bad habit
        draw.line([(140, 145), (240, 145)], fill=(255, 107, 53), width=4)
        draw.polygon([(240, 135), (260, 145), (240, 155)],
                     fill=(255, 107, 53))

        # Title
        EcoMemeGenerator._draw_text_with_outline(
            draw, (200, 20), "DISTRACTED",
            EcoMemeGenerator._get_font(30),
            fill=(255, 255, 255)
        )

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 380), "Terra 2.0 🌍", font=font_small,
                  fill=(255, 255, 255, 180))

        return img

    @staticmethod
    def _generate_this_is_fine(top_text: str, bottom_text: str) -> Image.Image:
        """This Is Fine meme — single panel with fire."""
        img = EcoMemeGenerator._create_base_image(600, 400)
        draw = ImageDraw.Draw(img)

        # Fiery background gradient
        for y in range(400):
            r = min(255, 200 + y // 5)
            g = max(0, 150 - y // 3)
            b = 0
            draw.line([(0, y), (600, y)], fill=(r, g, b))

        # Character in the middle
        draw.ellipse([(230, 150), (370, 290)],
                     fill=(244, 196, 48), outline=(0, 0, 0), width=3)
        font_emoji = EcoMemeGenerator._get_font(50)
        draw.text((270, 190), "☕", font=font_emoji, fill=(0, 0, 0))

        # "This is fine" text
        font = EcoMemeGenerator._get_font(24)
        draw.text((220, 310), "This is fine. 🔥", font=font,
                  fill=(255, 255, 255))

        # Top text
        font_big = EcoMemeGenerator._get_font(28)
        lines = EcoMemeGenerator._wrap_text(
            top_text or "The planet at 2°C warming",
            font_big, 550, draw
        )
        for i, line in enumerate(lines):
            EcoMemeGenerator._draw_text_with_outline(
                draw, (30, 20 + i * 35), line, font_big
            )

        # Fire emojis
        fire_positions = [(30, 100), (520, 80), (100, 300),
                          (450, 280), (50, 200), (500, 180)]
        font_fire = EcoMemeGenerator._get_font(30)
        for fx, fy in fire_positions:
            draw.text((fx, fy), "🔥", font=font_fire, fill=(255, 0, 0))

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 380), "Terra 2.0 🌍", font=font_small,
                  fill=(255, 255, 255, 180))

        return img

    @staticmethod
    def _generate_change_my_mind(top_text: str,
                                  bottom_text: str) -> Image.Image:
        """Change My Mind — table with sign."""
        img = EcoMemeGenerator._create_base_image(600, 400, (135, 206, 235))
        draw = ImageDraw.Draw(img)

        # Ground
        draw.rectangle([(0, 300), (600, 400)], fill=(34, 139, 34))

        # Table
        draw.rectangle([(150, 200), (500, 280)],
                       fill=(139, 90, 43), outline=(101, 67, 33), width=2)
        # Table legs
        draw.rectangle([(200, 280), (210, 340)], fill=(101, 67, 33))
        draw.rectangle([(440, 280), (450, 340)], fill=(101, 67, 33))

        # Sign text
        font = EcoMemeGenerator._get_font(20)
        sign_text = top_text or "Gen Z can save the planet"
        lines = EcoMemeGenerator._wrap_text(sign_text, font, 330, draw)
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_w = bbox[2] - bbox[0]
            draw.text((325 - text_w // 2, 215 + i * 25),
                      line, font=font, fill=(0, 0, 0))

        # Person behind table (circle head + body)
        draw.ellipse([(70, 120), (140, 190)],
                     fill=(244, 196, 48), outline=(0, 0, 0), width=2)
        draw.rectangle([(85, 190), (125, 300)],
                       fill=(46, 204, 113), outline=(0, 0, 0), width=1)

        # "Change my mind" text at bottom
        font_title = EcoMemeGenerator._get_font(26)
        EcoMemeGenerator._draw_text_with_outline(
            draw, (180, 350), "CHANGE MY MIND",
            font_title, fill=(255, 255, 255)
        )

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 380), "Terra 2.0 🌍", font=font_small,
                  fill=(255, 255, 255, 180))

        return img

    @staticmethod
    def _generate_always_has_been(top_text: str,
                                   bottom_text: str) -> Image.Image:
        """Always Has Been — two astronauts in space."""
        img = EcoMemeGenerator._create_base_image(600, 400, (10, 10, 40))
        draw = ImageDraw.Draw(img)

        # Stars
        import random
        rng = random.Random(42)
        for _ in range(80):
            x = rng.randint(0, 600)
            y = rng.randint(0, 400)
            size = rng.randint(1, 3)
            draw.ellipse([(x, y), (x + size, y + size)],
                         fill=(255, 255, 255))

        # Earth
        draw.ellipse([(200, 100), (400, 300)],
                     fill=(46, 204, 113),
                     outline=(126, 200, 227), width=3)
        # Continents
        draw.ellipse([(250, 140), (310, 200)], fill=(34, 139, 34))
        draw.ellipse([(300, 180), (370, 250)], fill=(34, 139, 34))

        # Astronaut 1 (left)
        draw.ellipse([(40, 150), (110, 220)],
                     fill=(200, 200, 200), outline=(150, 150, 150), width=2)
        draw.ellipse([(55, 160), (95, 195)], fill=(135, 206, 235))

        # Astronaut 2 (right, with gun)
        draw.ellipse([(490, 140), (560, 210)],
                     fill=(200, 200, 200), outline=(150, 150, 150), width=2)
        draw.ellipse([(505, 150), (545, 185)], fill=(135, 206, 235))
        # Gun
        draw.rectangle([(440, 170), (495, 180)], fill=(100, 100, 100))

        # Dialogue
        font = EcoMemeGenerator._get_font(18)

        # Astronaut 1 text (speech bubble)
        text1 = top_text or "Wait, the planet is dying?"
        lines1 = EcoMemeGenerator._wrap_text(text1, font, 220, draw)
        for i, line in enumerate(lines1):
            EcoMemeGenerator._draw_text_with_outline(
                draw, (20, 50 + i * 22), line, font,
                fill=(255, 255, 255)
            )

        # Astronaut 2 text
        text2 = bottom_text or "Always has been 🔫"
        lines2 = EcoMemeGenerator._wrap_text(text2, font, 200, draw)
        for i, line in enumerate(lines2):
            EcoMemeGenerator._draw_text_with_outline(
                draw, (430, 50 + i * 22), line, font,
                fill=(255, 255, 255)
            )

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 380), "Terra 2.0 🌍", font=font_small,
                  fill=(255, 255, 255, 180))

        return img

    @staticmethod
    def _generate_brain_size(top_text: str,
                              bottom_text: str) -> Image.Image:
        """Expanding Brain — four panel vertical."""
        img = EcoMemeGenerator._create_base_image(600, 600)
        draw = ImageDraw.Draw(img)

        # Parse texts — try to split by comma or use defaults
        texts = [t.strip() for t in top_text.split(",") if t.strip()]
        while len(texts) < 4:
            defaults = ["Using plastic bags", "Reusable bags",
                        "Growing own veggies", "Zero-waste lifestyle"]
            texts.append(defaults[len(texts)])
        texts = texts[:4]

        brain_sizes = [30, 45, 60, 80]
        bg_colors = [
            (240, 240, 240), (220, 235, 220),
            (200, 230, 255), (255, 220, 180)
        ]
        glow_colors = [
            (200, 200, 200), (150, 220, 150),
            (100, 180, 255), (255, 200, 50)
        ]

        font = EcoMemeGenerator._get_font(20)
        panel_h = 150

        for i, (text, brain_s, bg_c, glow_c) in enumerate(
            zip(texts, brain_sizes, bg_colors, glow_colors)
        ):
            y_start = i * panel_h

            # Panel background
            draw.rectangle([(0, y_start), (600, y_start + panel_h)],
                           fill=bg_c)
            # Divider
            draw.line([(0, y_start + panel_h - 1),
                       (600, y_start + panel_h - 1)],
                      fill=(200, 200, 200), width=1)

            # Brain glow
            cx, cy = 500, y_start + 75
            draw.ellipse(
                [(cx - brain_s - 10, cy - brain_s - 10),
                 (cx + brain_s + 10, cy + brain_s + 10)],
                fill=glow_c
            )
            # Brain
            draw.ellipse(
                [(cx - brain_s, cy - brain_s),
                 (cx + brain_s, cy + brain_s)],
                fill=(255, 180, 200),
                outline=(200, 100, 120), width=2
            )
            # Brain label
            brain_emoji = ["🧠", "🧠✨", "🧠💡", "🧠🔥"][i]
            font_e = EcoMemeGenerator._get_font(20)
            draw.text((cx - 15, cy - 10), brain_emoji,
                      font=font_e, fill=(0, 0, 0))

            # Text
            lines = EcoMemeGenerator._wrap_text(text, font, 400, draw)
            text_y = y_start + 75 - len(lines) * 13
            for j, line in enumerate(lines):
                draw.text((30, text_y + j * 26), line,
                          font=font, fill=(0, 0, 0))

        # Watermark
        font_small = EcoMemeGenerator._get_font(14)
        draw.text((480, 580), "Terra 2.0 🌍", font=font_small,
                  fill=(100, 100, 100))

        return img

    @staticmethod
    def image_to_bytes(img: Image.Image) -> bytes:
        """Convert PIL Image to PNG bytes."""
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def save_log(user_id: int, template: str,
                 top_text: str, bottom_text: str) -> bool:
        """Save meme creation to database."""
        engine = get_engine()
        try:
            with get_session(engine) as session:
                log = MemeLog(
                    user_id=user_id,
                    template_name=template,
                    top_text=top_text,
                    bottom_text=bottom_text,
                    created_at=datetime.utcnow(),
                )
                session.add(log)
                session.commit()
                return True
        except Exception:
            return False
