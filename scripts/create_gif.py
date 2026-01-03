from PIL import Image
from pathlib import Path

in_dir = Path('outputs/evidence')
out_dir = Path('outputs/videos')
out_dir.mkdir(parents=True, exist_ok=True)

# collect png files sorted by name
images = sorted(in_dir.glob('*.png'))
if not images:
    print('No images to make GIF')
    raise SystemExit(1)

frames = []
for p in images:
    try:
        im = Image.open(p)
        frames.append(im.convert('RGBA'))
    except Exception as e:
        # fallback: create a placeholder image using the HTML content if available
        print('creating placeholder for', p)
        html_p = p.with_suffix('.html')
        text = p.name
        if html_p.exists():
            try:
                text = html_p.read_text(encoding='utf-8').strip()[:200]
            except Exception:
                text = p.name
        # create placeholder
        img = Image.new('RGBA', (900, 600), (255, 255, 255, 255))
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype('DejaVuSans.ttf', 20)
        except Exception:
            font = ImageFont.load_default()
        lines = []
        # wrap text
        words = text.split()
        line = ''
        for w in words:
            if len(line) + len(w) + 1 > 60:
                lines.append(line)
                line = w
            else:
                line = (line + ' ' + w).strip()
        if line:
            lines.append(line)
        y = 40
        draw.text((40, 10), p.name, fill='black', font=font)
        for ln in lines[:20]:
            draw.text((40, y), ln, fill='black', font=font)
            y += 25
        frames.append(img)

# ensure at least one frame
if not frames:
    print('No valid frames')
    raise SystemExit(1)

out_path = out_dir / 'simulated_run.gif'
# Save as GIF
frames[0].save(out_path, format='GIF', save_all=True, append_images=frames[1:], duration=800, loop=0)
print('Wrote', out_path)
