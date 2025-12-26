from PIL import Image, ImageDraw, ImageFont
import os

# 配置路径
WORKDIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(WORKDIR, "template.jpg")
OUTPUT_PATH = os.path.join(WORKDIR, "final_post.jpg")

# 文案内容（请按需修改）
TITLE = "🎤提升气场·每日口才挑战🔥"
BODY = (
    "今日练习为即兴评述：主题《提升气场》。请围绕站姿、目光与语速展开，"
    "先提出观点：气场源于稳定的呼吸与清晰的节奏；接着举例说明在会议发言中如何"
    "通过三段式陈述（背景—观点—行动）传达可信度；最后以一句收束：声音稳、眼神定、"
    "结构清，气场自然来。"
)


def load_font(preferred_paths, size):
    for p in preferred_paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    # 兜底：可能无法正确显示中文
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    # 按空格和中文标点估算换行
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = draw.textbbox((0, 0), test, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def main():
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(
            f"未找到模板图片：{TEMPLATE_PATH}，请将 template.jpg 放在 docker/images 目录下。"
        )

    img = Image.open(TEMPLATE_PATH).convert("RGB")
    w, h = img.size
    draw = ImageDraw.Draw(img)

    # 字体路径优先选择中文字体
    font_paths = [
        r"C:/Windows/Fonts/msyh.ttc",
        r"C:/Windows/Fonts/msyh.ttf",
        r"C:/Windows/Fonts/simhei.ttf",
        r"/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]

    title_font = load_font(font_paths, size=int(h * 0.085))
    body_font = load_font(font_paths, size=int(h * 0.045))

    # 在顶部居中绘制标题
    title_bbox = draw.textbbox((0, 0), TITLE, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_h = title_bbox[3] - title_bbox[1]
    title_x = (w - title_w) // 2
    title_y = int(h * 0.08)
    draw.text((title_x, title_y), TITLE, font=title_font, fill=(0, 0, 0))

    # 绘制正文，自动换行
    max_body_width = int(w * 0.82)
    body_lines = wrap_text(BODY, body_font, max_body_width, draw)
    line_spacing = int(body_font.size * 1.6)
    start_y = title_y + title_h + int(h * 0.06)
    x = int(w * 0.09)

    for i, line in enumerate(body_lines):
        draw.text((x, start_y + i * line_spacing), line, font=body_font, fill=(0, 0, 0))

    img.save(OUTPUT_PATH, quality=92)
    print(f"已生成图片：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
