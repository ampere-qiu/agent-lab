"""Generate original classroom image/HTML assets locally; no model or network."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent


def prepare():
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    image = Image.new("RGB", (800, 500), "#f5f3ff")
    draw = ImageDraw.Draw(image)
    label_font = ImageFont.load_default(size=26)
    title_font = ImageFont.load_default(size=24)
    draw.text((35, 25), "WAYNE MANOR - FICTIONAL VENUE PLAN", fill="black", font=title_font)
    for box, color, label in [((40, 90, 260, 230), "#86efac", "ENTRANCE"),
                              ((300, 90, 750, 230), "#c4b5fd", "STAGE"),
                              ((40, 280, 540, 450), "#fde68a", "BUFFET"),
                              ((580, 280, 750, 450), "#fca5a5", "EXIT")]:
        draw.rectangle(box, fill=color, outline="black", width=3)
        draw.text((box[0]+15, box[1]+20), label, fill="black", font=label_font)
    image.save(assets / "venue.png")
    (assets / "venue.html").write_text('''<!doctype html><html lang="en"><meta charset="utf-8">
<title>Wayne Manor practice page</title>
<style>body{font:22px system-ui;margin:32px;background:#f5f3ff}img{width:600px;max-width:100%}button{font:inherit;padding:12px}#details{padding:20px;background:#fff}</style>
<h1>Wayne Manor — fictional practice page</h1><img src="venue.png" alt="Fictional venue plan">
<p><button onclick="document.getElementById('details').hidden=false">Show access details</button></p>
<section id="details" hidden><h2>Access details</h2><p>The east exit is closed for maintenance. Use the north entrance for accessible entry.</p></section>
</html>''', encoding="utf-8")
    print("Created assets/venue.png and assets/venue.html (no LLM).")


if __name__ == "__main__":
    prepare()
