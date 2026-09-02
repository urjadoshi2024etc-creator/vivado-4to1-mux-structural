from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

WIDTH, HEIGHT = 1200, 700
OUTPUT = "mux4_1-logic-animation.gif"

BG = "#0d1117"
PANEL = "#111827"
BORDER = "#30363d"
WHITE = "#f0f6fc"
MUTED = "#8b949e"
BLUE = "#58a6ff"
CYAN = "#7dd3fc"
YELLOW = "#facc15"
GREEN = "#4ade80"
PURPLE = "#c084fc"
INACTIVE = "#4b5563"


def get_font(size, bold=False):
    """
    Find an installed font automatically.
    Works better across Fedora/Linux, Windows and macOS.
    """

    font_candidates = []

    if bold:
        font_candidates = [
            "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
    else:
        font_candidates = [
            "/usr/share/fonts/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        ]

    for path in font_candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue

    # Final fallback
    return ImageFont.load_default(size=size)

FONT_SMALL = get_font(14)
FONT = get_font(18)
FONT_BOLD = get_font(18, True)
FONT_TITLE = get_font(28, True)
FONT_BIG = get_font(22, True)


def draw_glow_line(base, points, color, width=5):
    """
    Draws a glowing signal wire.
    """
    glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    rgb = tuple(int(color[i:i + 2], 16)
                for i in (1, 3, 5))

    glow_draw.line(
        points,
        fill=(*rgb, 120),
        width=width + 18,
        joint="curve"
    )

    glow = glow.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(glow)

    draw = ImageDraw.Draw(base)
    draw.line(
        points,
        fill=color,
        width=width,
        joint="curve"
    )


def draw_arrow(draw, start, end, color, width=3):
    """
    Draws a line with an arrow head.
    """
    draw.line(
        [start, end],
        fill=color,
        width=width
    )

    angle = math.atan2(
        end[1] - start[1],
        end[0] - start[0]
    )

    arrow_length = 12

    p1 = (
        end[0] - arrow_length * math.cos(angle - math.pi / 6),
        end[1] - arrow_length * math.sin(angle - math.pi / 6)
    )

    p2 = (
        end[0] - arrow_length * math.cos(angle + math.pi / 6),
        end[1] - arrow_length * math.sin(angle + math.pi / 6)
    )

    draw.polygon(
        [end, p1, p2],
        fill=color
    )


def draw_mux(draw, x, y, label, accent):
    """
    Draws a 2:1 MUX symbol.
    """

    points = [
        (x, y),
        (x, y + 110),
        (x + 100, y + 82),
        (x + 100, y + 28)
    ]

    draw.polygon(
        points,
        fill="#161b22",
        outline=accent
    )

    draw.line(
        points + [points[0]],
        fill=accent,
        width=3
    )

    draw.text(
        (x + 50, y + 48),
        label,
        anchor="mm",
        font=FONT_BOLD,
        fill=accent
    )

    draw.text(
        (x + 50, y + 75),
        "2:1",
        anchor="mm",
        font=FONT,
        fill=WHITE
    )

    # Input numbers
    draw.text(
        (x + 12, y + 25),
        "0",
        font=FONT_SMALL,
        fill=WHITE
    )

    draw.text(
        (x + 12, y + 82),
        "1",
        font=FONT_SMALL,
        fill=WHITE
    )


def create_frame(active_input):
    """
    Creates one animation frame.

    active_input:
        0 -> d0
        1 -> d1
        2 -> d2
        3 -> d3
    """

    img = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        BG
    )

    draw = ImageDraw.Draw(img)

    # -------------------------------------------------
    # Main panel
    # -------------------------------------------------

    draw.rounded_rectangle(
        (25, 20, 1175, 680),
        radius=18,
        fill=PANEL,
        outline=BORDER,
        width=2
    )

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    draw.text(
        (600, 55),
        "4:1 MULTIPLEXER USING THREE 2:1 MUXES",
        anchor="mm",
        font=FONT_TITLE,
        fill=WHITE
    )

    draw.text(
        (600, 87),
        "Animated Signal Flow",
        anchor="mm",
        font=FONT_BIG,
        fill=CYAN
    )

    # -------------------------------------------------
    # MUX blocks
    # -------------------------------------------------

    draw_mux(draw, 330, 200, "MUX 0", BLUE)
    draw_mux(draw, 330, 410, "MUX 1", BLUE)
    draw_mux(draw, 680, 305, "MUX 2", GREEN)

    # -------------------------------------------------
    # Data inputs
    # -------------------------------------------------

    inputs = [
        ("d0", 225),
        ("d1", 290),
        ("d2", 435),
        ("d3", 500),
    ]

    for index, (name, y) in enumerate(inputs):

        active = index == active_input

        color = YELLOW if active else INACTIVE
        width = 5 if active else 3

        if active:
            draw_glow_line(
                img,
                [(100, y), (330, y)],
                color,
                width
            )

            draw_arrow(
                draw,
                (310, y),
                (330, y),
                color,
                width
            )

        else:
            draw_arrow(
                draw,
                (100, y),
                (330, y),
                color,
                width
            )

        draw.text(
            (80, y),
            name,
            anchor="rm",
            font=FONT_BIG,
            fill=CYAN
        )

    # -------------------------------------------------
    # s0 select signal
    # -------------------------------------------------

    draw.line(
        [(280, 170), (280, 550)],
        fill=YELLOW,
        width=3
    )

    draw_arrow(
        draw,
        (280, 255),
        (330, 255),
        YELLOW,
        3
    )

    draw_arrow(
        draw,
        (280, 465),
        (330, 465),
        YELLOW,
        3
    )

    draw.text(
        (280, 155),
        "s0",
        anchor="mm",
        font=FONT_BIG,
        fill=YELLOW
    )

    # -------------------------------------------------
    # Intermediate signals
    # -------------------------------------------------

    first_mux_active = active_input in (0, 1)
    second_mux_active = active_input in (2, 3)

    w0_color = YELLOW if first_mux_active else INACTIVE
    w1_color = YELLOW if second_mux_active else INACTIVE

    w0_path = [
        (430, 255),
        (520, 255),
        (560, 255),
        (560, 340),
        (680, 340)
    ]

    w1_path = [
        (430, 465),
        (520, 465),
        (560, 465),
        (560, 380),
        (680, 380)
    ]

    if first_mux_active:
        draw_glow_line(
            img,
            w0_path,
            w0_color,
            5
        )
        draw_arrow(
            draw,
            (650, 340),
            (680, 340),
            w0_color,
            5
        )
    else:
        draw.line(
            w0_path,
            fill=w0_color,
            width=3
        )
        draw_arrow(
            draw,
            (650, 340),
            (680, 340),
            w0_color,
            3
        )

    if second_mux_active:
        draw_glow_line(
            img,
            w1_path,
            w1_color,
            5
        )
        draw_arrow(
            draw,
            (650, 380),
            (680, 380),
            w1_color,
            5
        )
    else:
        draw.line(
            w1_path,
            fill=w1_color,
            width=3
        )
        draw_arrow(
            draw,
            (650, 380),
            (680, 380),
            w1_color,
            3
        )

    draw.text(
        (480, 240),
        "w0",
        anchor="mm",
        font=FONT_BOLD,
        fill=YELLOW
    )

    draw.text(
        (480, 450),
        "w1",
        anchor="mm",
        font=FONT_BOLD,
        fill=YELLOW
    )

    # -------------------------------------------------
    # s1 select signal
    # -------------------------------------------------

    draw.line(
        [(635, 360), (680, 360)],
        fill=GREEN,
        width=3
    )

    draw_arrow(
        draw,
        (655, 360),
        (680, 360),
        GREEN,
        3
    )

    draw.text(
        (630, 340),
        "s1",
        anchor="mm",
        font=FONT_BIG,
        fill=GREEN
    )

    # -------------------------------------------------
    # Output
    # -------------------------------------------------

    draw_glow_line(
        img,
        [(780, 360), (930, 360)],
        PURPLE,
        5
    )

    draw_arrow(
        draw,
        (900, 360),
        (930, 360),
        PURPLE,
        5
    )

    draw.text(
        (950, 360),
        "y",
        anchor="lm",
        font=FONT_BIG,
        fill=PURPLE
    )

    # -------------------------------------------------
    # Current state
    # -------------------------------------------------

    select_values = [
        ("00", "d0"),
        ("01", "d1"),
        ("10", "d2"),
        ("11", "d3"),
    ]

    select, output = select_values[active_input]

    draw.rounded_rectangle(
        (960, 115, 1135, 215),
        radius=12,
        fill=BG,
        outline=PURPLE,
        width=2
    )

    draw.text(
        (1047, 140),
        f"STEP {active_input + 1} / 4",
        anchor="mm",
        font=FONT_BOLD,
        fill=WHITE
    )

    draw.text(
        (1047, 172),
        f"s1 s0 = {select}",
        anchor="mm",
        font=FONT_BOLD,
        fill=YELLOW
    )

    draw.text(
        (1047, 200),
        f"y = {output}",
        anchor="mm",
        font=FONT_BIG,
        fill=PURPLE
    )

    # -------------------------------------------------
    # Truth table
    # -------------------------------------------------

    draw.rounded_rectangle(
        (960, 240, 1135, 410),
        radius=12,
        fill=BG,
        outline=BORDER,
        width=2
    )

    draw.text(
        (1047, 265),
        "TRUTH TABLE",
        anchor="mm",
        font=FONT_BOLD,
        fill=CYAN
    )

    rows = [
        ("0", "0", "d0"),
        ("0", "1", "d1"),
        ("1", "0", "d2"),
        ("1", "1", "d3"),
    ]

    for i, row in enumerate(rows):

        y = 295 + i * 28

        if i == active_input:
            row_fill = "#29240d"
            row_outline = YELLOW
        else:
            row_fill = "#161b22"
            row_outline = BORDER

        draw.rounded_rectangle(
            (975, y - 12, 1120, y + 12),
            radius=5,
            fill=row_fill,
            outline=row_outline,
            width=2
        )

        draw.text(
            (1005, y),
            row[0],
            anchor="mm",
            font=FONT,
            fill=GREEN
        )

        draw.text(
            (1040, y),
            row[1],
            anchor="mm",
            font=FONT,
            fill=YELLOW
        )

        draw.text(
            (1090, y),
            row[2],
            anchor="mm",
            font=FONT,
            fill=CYAN
        )

    # -------------------------------------------------
    # Equations
    # -------------------------------------------------

    draw.rounded_rectangle(
        (960, 440, 1135, 600),
        radius=12,
        fill=BG,
        outline=BORDER,
        width=2
    )

    draw.text(
        (1047, 465),
        "KEY EQUATIONS",
        anchor="mm",
        font=FONT_BOLD,
        fill=CYAN
    )

    draw.text(
        (975, 505),
        "w0 = s0 ? d1 : d0",
        font=FONT_SMALL,
        fill=YELLOW
    )

    draw.text(
        (975, 535),
        "w1 = s0 ? d3 : d2",
        font=FONT_SMALL,
        fill=YELLOW
    )

    draw.text(
        (975, 565),
        "y  = s1 ? w1 : w0",
        font=FONT_SMALL,
        fill=PURPLE
    )

    # -------------------------------------------------
    # Bottom animation indicator
    # -------------------------------------------------

    draw.text(
        (480, 625),
        "00 → d0     01 → d1     10 → d2     11 → d3",
        anchor="mm",
        font=FONT_BOLD,
        fill=WHITE
    )

    draw.text(
        (480, 650),
        "s0 selects within each pair  •  s1 selects the pair",
        anchor="mm",
        font=FONT_SMALL,
        fill=MUTED
    )

    return img.convert("RGB")


# =====================================================
# CREATE ANIMATION
# =====================================================

frames = []

for state in range(4):

    # Hold each state for several frames.
    # This makes the animation easier to read.
    for _ in range(3):
        frames.append(create_frame(state))


# =====================================================
# SAVE GIF
# =====================================================

frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=400,
    loop=0,
    optimize=False
)

print(f"Created: {OUTPUT}")

