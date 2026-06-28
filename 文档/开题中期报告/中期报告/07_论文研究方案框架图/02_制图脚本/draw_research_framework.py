from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.font_manager import FontProperties


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "01_图件成果"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PNG_PATH = OUT_DIR / "论文研究方案总体框架图_1000ppi.png"
PDF_PATH = OUT_DIR / "论文研究方案总体框架图.pdf"
SVG_PATH = OUT_DIR / "论文研究方案总体框架图.svg"

FONT_SONG = FontProperties(fname=r"C:\Windows\Fonts\STSONG.TTF")
FONT_ZHONGSONG = FontProperties(fname=r"C:\Windows\Fonts\STZHONGS.TTF")
FONT_TIMES = FontProperties(fname=r"C:\Windows\Fonts\times.ttf")

mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.facecolor"] = "white"
mpl.rcParams["savefig.facecolor"] = "white"


def dashed_box(ax, x, y, w, h, lw=1.25):
    ax.add_patch(
        Rectangle(
            (x, y),
            w,
            h,
            linewidth=lw,
            edgecolor="#222222",
            facecolor="none",
            linestyle=(0, (5, 3)),
            zorder=1,
        )
    )


def rounded_box(
    ax,
    x,
    y,
    w,
    h,
    text,
    fc="#FFFFFF",
    ec="#424242",
    lw=1.0,
    size=9.0,
    bold=False,
    color="#222222",
):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.006,rounding_size=0.004",
            linewidth=lw,
            edgecolor=ec,
            facecolor=fc,
            zorder=3,
        )
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=size,
        color=color,
        fontproperties=FONT_ZHONGSONG if bold else FONT_SONG,
        fontweight="bold" if bold else "normal",
        zorder=4,
    )


def label_box(ax, x, y, w, h, text, vertical=False):
    ax.add_patch(
        Rectangle((x, y), w, h, linewidth=0, facecolor="#E4E4E4", zorder=2)
    )
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=9.2,
        color="#333333",
        fontproperties=FONT_ZHONGSONG,
        fontweight="bold",
        rotation=90 if vertical else 0,
        zorder=4,
    )


def arrow(ax, start, end, lw=1.2, ms=13):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=ms,
            linewidth=lw,
            edgecolor="#333333",
            facecolor="#333333",
            shrinkA=0,
            shrinkB=0,
            connectionstyle="arc3,rad=0",
            zorder=2,
        )
    )


def double_arrow(ax, start, end, lw=1.1, ms=11):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="<->",
            mutation_scale=ms,
            linewidth=lw,
            color="#333333",
            shrinkA=0,
            shrinkB=0,
            connectionstyle="arc3,rad=0",
            zorder=2,
        )
    )


fig = plt.figure(figsize=(15.0, 10.2), dpi=220)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Title layer
dashed_box(ax, 0.035, 0.905, 0.930, 0.062, lw=1.35)
ax.text(
    0.5,
    0.936,
    "广州市高新技术企业空间集聚的多尺度影响因素与时空预测研究",
    ha="center",
    va="center",
    fontsize=16.2,
    color="#222222",
    fontproperties=FONT_ZHONGSONG,
    fontweight="bold",
)
arrow(ax, (0.5, 0.905), (0.5, 0.858), lw=1.3, ms=18)

# Data layer
dashed_box(ax, 0.035, 0.760, 0.930, 0.095, lw=1.25)
label_box(ax, 0.055, 0.789, 0.088, 0.036, "数据层")
data_items = [
    ("高新技术企业POI\n工商属性数据", 0.190),
    ("多源外部数据", 0.390),
    ("区域网格化处理", 0.590),
    ("特征矩阵构建", 0.790),
]
for text, x in data_items:
    rounded_box(ax, x, 0.780, 0.150, 0.052, text, size=8.6, bold=True)

for x in [0.255, 0.500, 0.745]:
    double_arrow(ax, (x, 0.760), (x, 0.720), lw=1.05, ms=12)

# Research framework layer
dashed_box(ax, 0.035, 0.280, 0.930, 0.420, lw=1.25)
label_box(ax, 0.055, 0.395, 0.070, 0.190, "研究框架", vertical=True)

module_specs = [
    (
        0.165,
        "空间集聚化特征分析",
        [
            "核密度分析",
            "空间自相关分析",
            "热点分析",
            "标准差椭圆分析",
            "LISA时空演化分析",
        ],
    ),
    (
        0.415,
        "多尺度影响因素研究",
        [
            "变量设计与筛选",
            "GeoDetector因子探测",
            "OLS基准回归",
            "GWR地理加权回归",
            "MGWR多尺度回归",
        ],
    ),
    (
        0.700,
        "时空预测研究",
        [
            "事件流特征工程",
            "多关系格网图构建",
            "EF-STGNN模型",
            "滚动验证与评估",
            "未来预测与风险识别",
        ],
    ),
]

module_w = 0.190
module_h = 0.345
module_y = 0.320
for x, title, steps in module_specs:
    dashed_box(ax, x, module_y, module_w, module_h, lw=1.15)
    rounded_box(
        ax,
        x + 0.018,
        module_y + module_h - 0.058,
        module_w - 0.036,
        0.040,
        title,
        fc="#FFFFFF",
        size=8.6,
        bold=True,
    )
    step_h = 0.038
    step_gap = 0.014
    start_y = module_y + module_h - 0.103
    for i, step in enumerate(steps):
        rounded_box(
            ax,
            x + 0.028,
            start_y - i * (step_h + step_gap),
            module_w - 0.056,
            step_h,
            step,
            fc="#FFFFFF",
            ec="#888888",
            size=8.3,
            bold=i == 2 and "EF-STGNN" in step,
        )

# Straight module arrows
arrow(ax, (0.365, 0.490), (0.405, 0.490), lw=1.2, ms=17)
arrow(ax, (0.620, 0.490), (0.690, 0.490), lw=1.2, ms=17)

# Data to framework vertical links
for x in [0.255, 0.500, 0.795]:
    arrow(ax, (x, 0.720), (x, 0.700), lw=1.1, ms=12)

# Output layer
dashed_box(ax, 0.035, 0.165, 0.930, 0.075, lw=1.25)
label_box(ax, 0.055, 0.191, 0.088, 0.032, "产出层")
rounded_box(ax, 0.170, 0.185, 0.210, 0.038, "空间演化特征成果图表", size=8.6)
rounded_box(ax, 0.430, 0.185, 0.210, 0.038, "多尺度影响因素图表", size=8.6)
rounded_box(ax, 0.735, 0.185, 0.210, 0.038, "时空预测分布图表", size=8.6)

for x in [0.255, 0.535, 0.840]:
    arrow(ax, (x, module_y), (x, 0.240), lw=1.1, ms=14)

# Policy layer
dashed_box(ax, 0.035, 0.050, 0.930, 0.075, lw=1.25)
label_box(ax, 0.055, 0.076, 0.088, 0.032, "策略建议")
rounded_box(ax, 0.185, 0.070, 0.190, 0.038, "企业未来空间布局优化", size=8.6)
rounded_box(ax, 0.430, 0.070, 0.190, 0.038, "精准政策体系", size=8.6)
rounded_box(ax, 0.735, 0.070, 0.190, 0.038, "企业选址方案推荐", size=8.6)

for x in [0.270, 0.535, 0.840]:
    arrow(ax, (x, 0.165), (x, 0.125), lw=1.1, ms=14)

# Small method note
ax.text(
    0.700,
    0.305,
    "注：ConvLSTM仅作为探索性对照，不作为主模型",
    ha="left",
    va="center",
    fontsize=7.4,
    color="#555555",
    fontproperties=FONT_SONG,
)

fig.savefig(PNG_PATH, dpi=1000, bbox_inches="tight", pad_inches=0.14)
fig.savefig(PDF_PATH, bbox_inches="tight", pad_inches=0.14)
fig.savefig(SVG_PATH, bbox_inches="tight", pad_inches=0.14)
plt.close(fig)

print(PNG_PATH)
print(PDF_PATH)
print(SVG_PATH)
