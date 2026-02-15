import os
from PIL import Image
from io import BytesIO
import requests
import time
from tqdm import tqdm
import random


def handle_svg(source):
    """
    Convert SVG to PNG using external API and return as PIL Image.
    Works on all platforms including Windows!

    Args:
        source: Local path or URL to SVG file
    """

    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        svg_content = response.text
    else:
        with open(source, "r", encoding="utf-8") as f:
            svg_content = f.read()

    api_url = "https://svgtopng.onrender.com/convert"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"svg": svg_content}

    response = requests.post(api_url, data=data, headers=headers)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return img.convert("RGBA")
    else:
        print("API OUTPUT:", response.text)
        raise Exception(f"SVG conversion failed: {response.status_code}")


def load_image(source):
    """
    Load image from local path OR URL.
    Returns RGBA image.
    Handles SVG files automatically.
    """

    if source.lower().endswith(".svg"):
        return handle_svg(source)

    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(source)

    return img.convert("RGBA")


def place_image(base, img, position=(0, 0), rotation=0, color=None):
    """
    base      -> Background image
    img       -> Image to place
    position  -> (x, y)
    rotation  -> degrees
    color     -> HEX color string like "#FF0000" (optional tint)
    """
    img = img.copy()
    if color:
        overlay = Image.new("RGBA", img.size, color)
        img = Image.blend(img, overlay, 0.5)

    if rotation != 0:
        img = img.rotate(rotation, expand=True)
    base.paste(img, position, img)

    return base


def download_devicons():
    folder_path = "./icons"
    backup_icon_paths_file = "./backup-icon-paths.txt"
    output = []

    if os.path.exists(folder_path) == True:
        if os.path.exists(backup_icon_paths_file) == True:
            with open(backup_icon_paths_file, "r") as f:
                for line in f:
                    output_filter = line.replace("\n", "")
                    output.append(output_filter)
            return output

    devicon_urls = [
        # Web Dev
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-plain.svg",
        # Web Frameworks
        "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/vitejs/vitejs-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-plain.svg",
        # Backend
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/rust/rust-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-plain.svg",
        # Interests
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/raspberrypi/raspberrypi-plain.svg",
        # OS
        "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linuxmint/linuxmint-plain.svg",
        "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/debian/debian-plain.svg",
    ]

    api_url = "https://svgtopng.onrender.com/convert"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    print(" > Loading SVG content...")
    for url in devicon_urls:
        res = requests.get(url)
        svg_content = res.text

        data = {"svg": svg_content}
        response = requests.post(api_url, data=data, headers=headers)

        print(" > Converting to PNG...")
        if response.status_code == 200:
            file_name = url.split("/")[-1].replace(".svg", ".png")
            full_file_path = f"{folder_path}/{file_name}"

            with open(full_file_path, "wb") as f:
                f.write(response.content)

            output.append(full_file_path)
            print(f"[OK] > Converted and saved: {file_name}")
            time.sleep(0.5)
        else:
            print(f"[ERROR] > Failed: {url.split('/')[-1]} - {response.status_code}")

    with open("backup-icons-paths.txt", "w") as f:
        f.write("\n".join(output))
        print(" > Created backup of Icon paths")

    return output


def arrange_icon(order: int, spacing: int = 100, cols: int = 5):
    row = order // cols
    col = order % cols

    x = 50 + col * spacing
    y = 50 + row * spacing

    return (x, y)


def randomly_arrange(canvas: tuple = (200, 200), icon_size: int = 20, margin: int = 50):
    canvas_width, canvas_height = canvas
    x = random.randint(margin, canvas_width - icon_size - margin)
    y = random.randint(margin, canvas_height - icon_size - margin)

    deg = random.randint(0, 360)

    return (x, y), deg


def main():
    canvas = (1000, 400)  # (W,H)
    icon_size = 40
    devicons = download_devicons()
    print(" > Loading Icons...")
    devicon_objs = []
    for url in devicons:
        devicon_objs.append(load_image(url))
        time.sleep(0.5)
    print(f" > Canvas Created - {canvas}")
    base = Image.new("RGBA", canvas, "#253142")  # Background color format is `HEX`

    drawing = []
    # ----- DRAW HERE -----
    for i in range(0, 800):  # Generate 800 positions
        # position,deg = randomly_arrange(canvas=canvas,icon_size=40)
        # drawing.append((position,deg))

        x, y = arrange_icon(i)
        deg = random.randint(0,270)

        position = (x, y)
        drawing.append((position, deg))
    # ------...------------

    for idx, (position, deg) in enumerate(drawing):
        # Cycle through icons using modulo
        icon_idx = idx % len(devicon_objs)
        icon = devicon_objs[icon_idx]
        icon = icon.resize((icon_size, icon_size))
        base = place_image(base, icon, position=position, rotation=deg)

    base.show()
    base.save(f"skills-showcase-{random.randint(1,100)}.png")


if __name__ == "__main__":
    main()
