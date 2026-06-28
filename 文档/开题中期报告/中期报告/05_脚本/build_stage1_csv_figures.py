# -*- coding: utf-8 -*-
"""Build enhanced midterm figures from stage-one CSV outputs.

The figures in this script are descriptive CSV-data-result figures. They are
not ArcGIS Pro spatial-clustering experiment maps.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import math
import shutil
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Rectangle


warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parents[4]
REPORT_DIR = ROOT / "文档" / "开题中期报告" / "中期报告"
FIG_DIR = REPORT_DIR / "03_汇报图件"
TABLE_DIR = REPORT_DIR / "02_统计表格"

DIRS = {
    "structure": FIG_DIR / "01_数据底板结构",
    "dynamic": FIG_DIR / "02_年度增长与动态变量",
    "grid_load": FIG_DIR / "03_格网扩展与承载",
    "attribute": FIG_DIR / "04_企业属性结构",
    "lifecycle": FIG_DIR / "05_企业生命周期",
    "grid_structure": FIG_DIR / "06_格网结构特征",
    "dl": FIG_DIR / "07_DL矩阵预测底板",
    "validation": FIG_DIR / "08_数据一致性校验",
}

OLD_DIRS = [
    "01_数据底板结构",
    "02_年度动态变量",
    "02_年度增长与动态变量",
    "03_企业属性结构",
    "03_格网扩展与承载",
    "04_格网化成果展示",
    "04_企业属性结构",
    "05_DL矩阵数据底板",
    "05_企业生命周期",
    "06_格网结构特征",
    "07_DL矩阵预测底板",
    "08_数据一致性校验",
]


def find_required(name: str, required_parts: list[str]) -> Path:
    matches = []
    for p in ROOT.rglob(name):
        s = str(p)
        if all(part in s for part in required_parts):
            matches.append(p)
    if not matches:
        raise FileNotFoundError(f"Cannot find {name} with parts {required_parts}")
    return matches[0]


P7 = find_required("master_grid_year_panel.csv", ["阶段一：企业动态变量研究", "7、最终格网标准数据"])
P8 = find_required("firm_year_points_2015_2024.csv", ["阶段一：企业动态变量研究", "8、最终点位数据"])
P9 = find_required("master_full_grid_year_panel.csv", ["阶段一：企业动态变量研究", "9、最终DL格网标准数据"])


def setup_dirs() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    for d in OLD_DIRS:
        p = FIG_DIR / d
        if p.exists():
            shutil.rmtree(p)
    for d in DIRS.values():
        d.mkdir(parents=True, exist_ok=True)


def setup_style() -> None:
    fonts = {Path(f.fname).stem.lower(): f.fname for f in font_manager.fontManager.ttflist}
    font_names = {f.name.lower(): f.fname for f in font_manager.fontManager.ttflist}
    chinese_font = None
    # STZhongsong is still Song-style but visually heavier than plain SimSun,
    # which makes exported PNG text more legible after PPT scaling.
    for candidate in ["stzhongsong", "stsong", "simsun", "microsoft yahei", "simhei"]:
        if candidate in font_names:
            chinese_font = font_names[candidate]
            break
        if candidate in fonts:
            chinese_font = fonts[candidate]
            break
    if chinese_font:
        font_manager.fontManager.addfont(chinese_font)
        zh_name = font_manager.FontProperties(fname=chinese_font).get_name()
    else:
        zh_name = "SimSun"

    plt.rcParams.update({
        "font.family": [zh_name, "Times New Roman"],
        "font.serif": ["Times New Roman"],
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "text.color": "#111111",
        "axes.labelcolor": "#111111",
        "xtick.color": "#111111",
        "ytick.color": "#111111",
        "axes.edgecolor": "#111111",
        "axes.linewidth": 1.35,
        "axes.titlesize": 21,
        "axes.titleweight": "bold",
        "axes.labelsize": 17,
        "axes.labelweight": "bold",
        "xtick.labelsize": 15,
        "ytick.labelsize": 15,
        "legend.fontsize": 14,
        "legend.frameon": False,
        "grid.color": "#ECECEC",
        "grid.linewidth": 0.9,
        "lines.linewidth": 3.1,
        "lines.markersize": 8.6,
        "patch.linewidth": 1.2,
    })


def savefig(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path.with_suffix(".png"), dpi=600, bbox_inches="tight", facecolor="white", pil_kwargs={"compress_level": 1})
    plt.savefig(path.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.savefig(path.with_suffix(".svg"), bbox_inches="tight", facecolor="white")
    plt.close()


def fmt_int(x) -> str:
    return f"{int(round(float(x))):,}"


def fmt_plain(x) -> str:
    return str(int(round(float(x))))


def gini(values: pd.Series | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0 or arr.sum() == 0:
        return 0.0
    arr = np.sort(arr)
    n = arr.size
    return float((2 * np.arange(1, n + 1) @ arr) / (n * arr.sum()) - (n + 1) / n)


def hhi(values: pd.Series | np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    total = arr.sum()
    if total == 0:
        return 0.0
    shares = arr / total
    return float(np.sum(shares ** 2))


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df7 = pd.read_csv(P7)
    df8 = pd.read_csv(P8)
    df9 = pd.read_csv(P9)
    return df7, df8, df9


def build_tables(df7: pd.DataFrame, df8: pd.DataFrame, df9: pd.DataFrame) -> dict[str, pd.DataFrame]:
    y7 = df7.groupby("year").agg(
        active_total=("active_cnt", "sum"),
        entry_total=("entry_cnt", "sum"),
        persist_total=("persist_cnt", "sum"),
        renew_total=("renew_cnt", "sum"),
        exit_next_total=("exit_next_cnt", "sum"),
        active_grids=("active_cnt", lambda s: int((s > 0).sum())),
        valid_grids=("valid_mask", "sum"),
        max_grid_active=("active_cnt", "max"),
        mean_active_per_active_grid=("active_cnt", lambda s: float(s[s > 0].mean()) if (s > 0).any() else 0.0),
        high_grid_5=("active_cnt", lambda s: int((s >= 5).sum())),
        high_grid_10=("active_cnt", lambda s: int((s >= 10).sum())),
        high_grid_20=("active_cnt", lambda s: int((s >= 20).sum())),
    ).reset_index()
    y7["active_grid_ratio"] = y7["active_grids"] / y7["valid_grids"]
    y7["net_growth"] = y7["active_total"].diff()
    y7["growth_rate"] = y7["active_total"].pct_change()
    y7["entry_rate"] = y7["entry_total"] / y7["active_total"]
    y7["persist_rate"] = y7["persist_total"] / y7["active_total"]
    y7["renew_rate"] = y7["renew_total"] / y7["active_total"]
    y7["exit_next_rate"] = y7["exit_next_total"] / y7["active_total"]

    y8 = df8.groupby("year").agg(
        point_records=("firm_id", "size"),
        unique_firms=("firm_id", "nunique"),
        median_capital=("capital_wan", "median"),
    ).reset_index()

    y9 = df9.groupby("year").agg(
        full_cells=("grid_id", "size"),
        valid_cells=("valid_mask", "sum"),
        active_total_full=("active_cnt", "sum"),
        nonzero_cells=("active_cnt", lambda s: int((s > 0).sum())),
    ).reset_index()
    y9["valid_ratio"] = y9["valid_cells"] / y9["full_cells"]
    y9["nonzero_ratio_full"] = y9["nonzero_cells"] / y9["full_cells"]
    y9["nonzero_ratio_valid"] = y9["nonzero_cells"] / y9["valid_cells"]

    annual = y7.merge(y8, on="year", how="left").merge(y9, on="year", how="left")
    annual["point_grid_diff"] = annual["point_records"] - annual["active_total"]
    annual["full_valid_grid_diff"] = annual["valid_cells"] - annual["valid_grids"]
    annual.to_csv(TABLE_DIR / "阶段一_增强版年度汇总表.csv", index=False, encoding="utf-8-sig")

    category_cols = [c for c in df7.columns if c.startswith("n_cat_")]
    size_cols = [c for c in df7.columns if c.startswith("n_size_")]
    cat_year = df7.groupby("year")[category_cols].sum().reset_index()
    size_year = df7.groupby("year")[size_cols].sum().reset_index()
    cat_year.to_csv(TABLE_DIR / "阶段一_年度技术门类汇总表.csv", index=False, encoding="utf-8-sig")
    size_year.to_csv(TABLE_DIR / "阶段一_年度企业规模汇总表.csv", index=False, encoding="utf-8-sig")

    conc_rows = []
    for year, g in df7.groupby("year"):
        active = g["active_cnt"].sort_values(ascending=False)
        total = active.sum()
        n = len(active)
        row = {
            "year": year,
            "gini": gini(active),
            "hhi": hhi(active),
            "max_grid_active": active.max(),
        }
        for q in [0.01, 0.05, 0.10]:
            k = max(1, math.ceil(n * q))
            row[f"top_{int(q * 100)}_share"] = active.iloc[:k].sum() / total if total else 0
        conc_rows.append(row)
    concentration = pd.DataFrame(conc_rows)
    concentration.to_csv(TABLE_DIR / "阶段一_格网承载集中度表.csv", index=False, encoding="utf-8-sig")

    firm_life = df8.groupby("firm_id").agg(
        active_years=("year", "nunique"),
        first_year=("year", "min"),
        last_year=("year", "max"),
        grid_count=("grid_id", "nunique"),
        category=("hi_category", lambda s: s.dropna().iloc[0] if len(s.dropna()) else "未知"),
        size_class=("size_class", lambda s: s.dropna().iloc[0] if len(s.dropna()) else "未知"),
    ).reset_index()
    firm_life["grid_change_flag"] = firm_life["grid_count"] > 1
    firm_life.to_csv(TABLE_DIR / "阶段一_企业生命周期汇总表.csv", index=False, encoding="utf-8-sig")

    grid_life = df7.groupby("grid_id").agg(
        active_years=("active_cnt", lambda s: int((s > 0).sum())),
        max_active=("active_cnt", "max"),
        mean_active=("active_cnt", "mean"),
    ).reset_index()
    grid_life["type"] = pd.cut(
        grid_life["active_years"],
        bins=[-1, 0, 2, 5, 9, 10],
        labels=["从未活跃", "短期活跃", "间歇活跃", "长期活跃", "十年持续活跃"],
    )
    grid_life.to_csv(TABLE_DIR / "阶段一_格网活跃稳定性表.csv", index=False, encoding="utf-8-sig")

    validation = pd.DataFrame([
        {
            "check_item": "点位表年度记录数 = 有效格网面板active_cnt年度总和",
            "result": "PASS" if (annual["point_grid_diff"].abs() == 0).all() else "FAIL",
            "max_abs_diff": int(annual["point_grid_diff"].abs().max()),
        },
        {
            "check_item": "完整格网面板valid_mask年度总数 = 有效格网面板valid_mask年度总数",
            "result": "PASS" if (annual["full_valid_grid_diff"].abs() == 0).all() else "FAIL",
            "max_abs_diff": int(annual["full_valid_grid_diff"].abs().max()),
        },
        {
            "check_item": "完整格网年度单元数稳定",
            "result": "PASS" if annual["full_cells"].nunique() == 1 else "FAIL",
            "max_abs_diff": int(annual["full_cells"].max() - annual["full_cells"].min()),
        },
        {
            "check_item": "年份范围为2015-2024",
            "result": "PASS" if list(annual["year"]) == list(range(2015, 2025)) else "FAIL",
            "max_abs_diff": 0,
        },
    ])
    validation.to_csv(TABLE_DIR / "阶段一_CSV数据一致性校验表.csv", index=False, encoding="utf-8-sig")

    cross = pd.crosstab(df8["hi_category"], df8["size_class"])
    cross.to_csv(TABLE_DIR / "阶段一_门类规模交叉表.csv", encoding="utf-8-sig")

    return {
        "annual": annual,
        "cat_year": cat_year,
        "size_year": size_year,
        "concentration": concentration,
        "firm_life": firm_life,
        "grid_life": grid_life,
        "validation": validation,
        "cross": cross,
    }


def annotate_endpoints(ax, x, y, fmt="{:,.0f}", color="#333333") -> None:
    ax.annotate(fmt.format(y.iloc[0]), (x.iloc[0], y.iloc[0]), xytext=(0, 12),
                textcoords="offset points", ha="center", fontsize=13, color=color)
    ax.annotate(fmt.format(y.iloc[-1]), (x.iloc[-1], y.iloc[-1]), xytext=(0, 12),
                textcoords="offset points", ha="center", fontsize=13, color=color)


def fig_structure(df7, df8, df9) -> None:
    labels = ["企业年度点位表", "有效格网年度面板", "完整DL格网面板"]
    values = [len(df8), len(df7), len(df9)]
    colors = ["#5F8DB3", "#78A878", "#C49A52"]
    fig, ax = plt.subplots(figsize=(11, 6.2))
    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_title("阶段一核心CSV数据底板规模", pad=16)
    ax.set_ylabel("记录数")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_ylim(0, max(values) * 1.18)
    for b, v in zip(bars, values):
        ax.annotate(fmt_int(v), (b.get_x() + b.get_width() / 2, v), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=15)
    savefig(DIRS["structure"] / "fig01_阶段一核心CSV数据底板规模")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.axis("off")
    boxes = [
        ("8 企业年度点位表", "99,498条企业-年份记录\n企业属性、坐标、动态状态"),
        ("7 有效格网年度面板", "29,755个有效格网 × 10年\n数量、动态变量、属性结构"),
        ("9 完整DL格网面板", "68,930个完整矩阵格网 × 10年\n305行 × 226列"),
    ]
    xs = [0.07, 0.38, 0.69]
    for x, (title, text) in zip(xs, boxes):
        box = FancyBboxPatch((x, 0.36), 0.24, 0.33, boxstyle="round,pad=0.02,rounding_size=0.018",
                             lw=1.2, edgecolor="#555555", facecolor="#F7F7F7")
        ax.add_patch(box)
        ax.text(x + 0.12, 0.59, title, ha="center", va="center", fontsize=17, fontweight="bold")
        ax.text(x + 0.12, 0.46, text, ha="center", va="center", fontsize=15, linespacing=1.45)
    for x in [0.32, 0.63]:
        ax.annotate("", xy=(x + 0.06, 0.525), xytext=(x, 0.525),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#555555"))
    ax.set_title("阶段一CSV数据底板关系", fontsize=23, pad=8, fontweight="bold")
    savefig(DIRS["structure"] / "fig02_阶段一CSV数据底板关系")


def fig_dynamic(t: dict[str, pd.DataFrame]) -> None:
    a = t["annual"]
    years = a["year"]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8.2), sharex=True)
    axes[0].plot(years, a["active_total"], marker="o", color="#2E6F9E")
    axes[0].set_title("活跃企业数量变化", fontsize=18, fontweight="bold")
    axes[0].set_ylabel("活跃企业数量")
    axes[0].grid(axis="y")
    axes[0].spines[["top", "right"]].set_visible(False)
    axes[0].annotate(fmt_plain(a["active_total"].iloc[0]), (years.iloc[0], a["active_total"].iloc[0]),
                     xytext=(0, 12), textcoords="offset points", ha="center", fontsize=14)
    axes[0].annotate(fmt_plain(a["active_total"].iloc[-1]), (years.iloc[-1], a["active_total"].iloc[-1]),
                     xytext=(0, 12), textcoords="offset points", ha="center", fontsize=14)

    net = a["net_growth"].fillna(0)
    bar_colors = np.where(net >= 0, "#C9D8E8", "#F2C4C4")
    axes[1].bar(years, net, width=0.56, color=bar_colors)
    axes[1].axhline(0, color="#333333", lw=1)
    axes[1].set_title("年度净增长", fontsize=18, fontweight="bold")
    axes[1].set_xlabel("年份")
    axes[1].set_ylabel("净增长数量")
    axes[1].grid(axis="y")
    axes[1].spines[["top", "right"]].set_visible(False)
    max_idx = int(net.iloc[1:].idxmax())
    axes[1].annotate(fmt_plain(net.loc[max_idx]), (a.loc[max_idx, "year"], net.loc[max_idx]),
                     xytext=(0, 12), textcoords="offset points", ha="center", fontsize=14)
    axes[1].set_xticks(years)
    fig.suptitle("活跃企业数量与年度净增长", fontsize=23, y=1.01, fontweight="bold")
    savefig(DIRS["dynamic"] / "fig03_活跃企业数量与年度净增长")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    rate = a["growth_rate"] * 100
    ax.bar(years[1:], rate.iloc[1:], width=0.56, color="#80B1D3")
    ax.axhline(0, color="#333333", lw=1)
    ax.set_title("活跃企业数量同比增长率", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("同比增长率（%）")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    for x, y in zip(years[1:], rate.iloc[1:]):
        ax.annotate(f"{y:.1f}%", (x, y), xytext=(0, 8 if y >= 0 else -18),
                    textcoords="offset points", ha="center", fontsize=13)
    savefig(DIRS["dynamic"] / "fig04_活跃企业同比增长率")

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True)
    items = [
        ("entry_total", "新增企业", "#4C78A8"),
        ("persist_total", "持续企业", "#72B7B2"),
        ("renew_total", "续认定企业", "#59A14F"),
        ("exit_next_total", "下一年退出代理", "#E15759"),
    ]
    for ax, (col, title, color) in zip(axes.ravel(), items):
        ax.plot(years, a[col], marker="o", color=color)
        ax.set_title(title, fontsize=18, fontweight="bold")
        ax.grid(axis="y")
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xticks(years)
        ax.tick_params(axis="x", rotation=35)
        annotate_endpoints(ax, years, a[col], color=color)
        if col == "exit_next_total":
            ax.annotate("2024缺少下一年观测", (2024, a[col].iloc[-1]), xytext=(-95, 28),
                        textcoords="offset points", fontsize=13, color="#555555",
                        arrowprops=dict(arrowstyle="-", color="#999999", lw=1))
    fig.suptitle("企业动态变量年度变化", fontsize=23, y=1.02, fontweight="bold")
    savefig(DIRS["dynamic"] / "fig05_企业动态变量年度变化")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    stack_cols = ["entry_rate", "persist_rate", "renew_rate"]
    labels = ["新增占比", "持续占比", "续认定占比"]
    colors = ["#4C78A8", "#72B7B2", "#59A14F"]
    bottom = np.zeros(len(a))
    for col, lab, color in zip(stack_cols, labels, colors):
        vals = a[col].fillna(0).values * 100
        ax.bar(years, vals, bottom=bottom, width=0.58, label=lab, color=color)
        bottom += vals
    ax.set_title("企业动态变量年度占比结构", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("占比（%）")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    savefig(DIRS["dynamic"] / "fig06_企业动态变量年度占比结构")


def fig_grid_load(t: dict[str, pd.DataFrame]) -> None:
    a = t["annual"]
    c = t["concentration"]
    years = a["year"]

    fig, axes = plt.subplots(2, 1, figsize=(12, 8.2), sharex=True)
    axes[0].bar(years, a["active_grids"], color="#9CC3A5", width=0.58)
    axes[0].set_title("活跃格网数量变化", fontsize=18, fontweight="bold")
    axes[0].set_ylabel("活跃格网数量")
    axes[0].grid(axis="y")
    axes[0].spines[["top", "right"]].set_visible(False)
    axes[0].annotate(fmt_int(a["active_grids"].iloc[0]), (years.iloc[0], a["active_grids"].iloc[0]), xytext=(0, 8),
                     textcoords="offset points", ha="center", fontsize=13)
    axes[0].annotate(fmt_int(a["active_grids"].iloc[-1]), (years.iloc[-1], a["active_grids"].iloc[-1]), xytext=(0, 8),
                     textcoords="offset points", ha="center", fontsize=13)

    axes[1].plot(years, a["mean_active_per_active_grid"], marker="o", color="#B07AA1", label="活跃格网平均企业数")
    axes[1].plot(years, a["max_grid_active"], marker="s", color="#2E6F9E", label="单格网最大企业数")
    axes[1].set_title("格网承载强度变化", fontsize=18, fontweight="bold")
    axes[1].set_xlabel("年份")
    axes[1].set_ylabel("企业数")
    axes[1].grid(axis="y")
    axes[1].spines[["top", "right"]].set_visible(False)
    axes[1].legend(loc="upper left")
    fig.suptitle("格网覆盖范围与承载强度变化", fontsize=23, y=1.01, fontweight="bold")
    savefig(DIRS["grid_load"] / "fig07_格网覆盖范围与承载强度变化")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.plot(years, a["high_grid_5"], marker="o", label="active_cnt ≥ 5", color="#80B1D3")
    ax.plot(years, a["high_grid_10"], marker="s", label="active_cnt ≥ 10", color="#4C78A8")
    ax.plot(years, a["high_grid_20"], marker="^", label="active_cnt ≥ 20", color="#1F4E79")
    ax.set_title("高承载格网数量年度变化", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("格网数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend()
    savefig(DIRS["grid_load"] / "fig08_高承载格网数量年度变化")

    fig, axes = plt.subplots(3, 1, figsize=(12, 9.4), sharex=True)
    axes[0].plot(c["year"], c["gini"], marker="o", color="#E15759")
    axes[0].set_title("Gini系数", fontsize=18, fontweight="bold")
    axes[0].set_ylabel("Gini")
    axes[0].grid(axis="y")
    axes[0].spines[["top", "right"]].set_visible(False)

    axes[1].plot(c["year"], c["hhi"] * 1000, marker="s", color="#B07AA1")
    axes[1].set_title("HHI指数（×1000）", fontsize=18, fontweight="bold")
    axes[1].set_ylabel("HHI × 1000")
    axes[1].grid(axis="y")
    axes[1].spines[["top", "right"]].set_visible(False)

    axes[2].plot(c["year"], c["top_1_share"] * 100, marker="^", color="#4C78A8", label="前1%格网")
    axes[2].plot(c["year"], c["top_5_share"] * 100, marker="D", color="#59A14F", label="前5%格网")
    axes[2].plot(c["year"], c["top_10_share"] * 100, marker="o", color="#C49A52", label="前10%格网")
    axes[2].set_title("Top格网企业承载比例", fontsize=18, fontweight="bold")
    axes[2].set_xlabel("年份")
    axes[2].set_ylabel("承载比例（%）")
    axes[2].grid(axis="y")
    axes[2].spines[["top", "right"]].set_visible(False)
    axes[2].legend(ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.20))
    fig.suptitle("格网企业承载集中度变化", fontsize=23, y=1.01, fontweight="bold")
    savefig(DIRS["grid_load"] / "fig09_格网企业承载集中度变化")


def fig_attribute(df8: pd.DataFrame, t: dict[str, pd.DataFrame]) -> None:
    cat_year = t["cat_year"].set_index("year")
    cat_year.columns = [c.replace("n_cat_", "") for c in cat_year.columns]
    cat_pct = cat_year.div(cat_year.sum(axis=1), axis=0) * 100
    cat_order = cat_year.sum().sort_values(ascending=False).index.tolist()
    cat_pct = cat_pct[cat_order]
    colors = ["#4C78A8", "#72B7B2", "#59A14F", "#F28E2B", "#B07AA1", "#E15759", "#EDC948", "#9D755D"]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.stackplot(cat_pct.index, [cat_pct[c] for c in cat_pct.columns],
                 labels=cat_pct.columns, colors=colors[:len(cat_pct.columns)], alpha=0.94)
    ax.set_title("高新技术企业门类年度结构变化", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("占比（%）")
    ax.set_xlim(cat_pct.index.min(), cat_pct.index.max())
    ax.set_ylim(0, 100)
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=14)
    savefig(DIRS["attribute"] / "fig10_技术门类年度结构变化")

    major = cat_order[:5]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    for c, color in zip(major, colors):
        ax.plot(cat_year.index, cat_year[c], marker="o", label=c, color=color)
    ax.set_title("主要技术门类年度数量变化", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("企业年度记录数")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", ncol=2)
    savefig(DIRS["attribute"] / "fig11_主要技术门类年度数量变化")

    size_year = t["size_year"].set_index("year")
    size_year.columns = [c.replace("n_size_", "") for c in size_year.columns]
    order = [c for c in ["微型", "小型", "中型", "大型", "未知"] if c in size_year.columns]
    size_pct = size_year[order].div(size_year[order].sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(12, 6.4))
    bottom = np.zeros(len(size_pct))
    size_colors = {"微型": "#A6CEE3", "小型": "#74A9CF", "中型": "#FDBF6F", "大型": "#E6550D", "未知": "#BDBDBD"}
    for c in order:
        ax.bar(size_pct.index, size_pct[c], bottom=bottom, width=0.58, label=c, color=size_colors[c])
        bottom += size_pct[c].values
    ax.set_title("企业规模年度结构变化", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("占比（%）")
    ax.set_ylim(0, 100)
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    savefig(DIRS["attribute"] / "fig12_企业规模年度结构变化")

    cross = t["cross"].copy()
    row_sum = cross.sum(axis=1).replace(0, np.nan)
    cross_pct = cross.div(row_sum, axis=0) * 100
    cross_pct = cross_pct.loc[cat_order]
    fig, ax = plt.subplots(figsize=(12, 6.8))
    im = ax.imshow(cross_pct.values, cmap="YlGnBu", vmin=0, vmax=np.nanmax(cross_pct.values))
    ax.set_xticks(range(len(cross_pct.columns)))
    ax.set_xticklabels(cross_pct.columns)
    ax.set_yticks(range(len(cross_pct.index)))
    ax.set_yticklabels(cross_pct.index)
    ax.set_title("技术门类与企业规模结构交叉", pad=16)
    for i in range(cross_pct.shape[0]):
        for j in range(cross_pct.shape[1]):
            val = cross_pct.iloc[i, j]
            if np.isfinite(val) and val >= 3:
                txt_color = "white" if val >= 35 else "#1F1F1F"
                ax.text(j, i, f"{val:.0f}%", ha="center", va="center", fontsize=13, color=txt_color, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.02)
    cbar.set_label("门类内部占比（%）")
    savefig(DIRS["attribute"] / "fig13_技术门类与企业规模结构交叉")

    cap = df8[["year", "capital_wan"]].copy()
    cap["capital_wan"] = pd.to_numeric(cap["capital_wan"], errors="coerce")
    cap = cap[(cap["capital_wan"].notna()) & (cap["capital_wan"] >= 0)]
    cap["log_capital"] = np.log10(cap["capital_wan"] + 1)
    data = [cap.loc[cap["year"] == y, "log_capital"].values for y in sorted(cap["year"].unique())]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    bp = ax.boxplot(data, tick_labels=sorted(cap["year"].unique()), patch_artist=True, showfliers=False)
    for patch in bp["boxes"]:
        patch.set_facecolor("#D9E8F5")
        patch.set_edgecolor("#4C78A8")
        patch.set_linewidth(1.2)
    for obj in bp["whiskers"] + bp["caps"] + bp["medians"]:
        obj.set_color("#4C78A8")
        obj.set_linewidth(1.2)
    ax.set_title("企业注册资本年度分布（对数尺度）", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("log10(注册资本/万元 + 1)")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    savefig(DIRS["attribute"] / "fig14_注册资本年度分布_对数尺度")


def fig_lifecycle(t: dict[str, pd.DataFrame]) -> None:
    firm = t["firm_life"]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    counts = firm["active_years"].value_counts().sort_index()
    ax.bar(counts.index, counts.values, width=0.65, color="#80B1D3")
    ax.set_title("企业样本内活跃年限分布", pad=16)
    ax.set_xlabel("样本内活跃年数")
    ax.set_ylabel("企业数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    for x, y in zip(counts.index, counts.values):
        ax.annotate(fmt_int(y), (x, y), xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=13)
    savefig(DIRS["lifecycle"] / "fig15_企业样本内活跃年限分布")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    first = firm["first_year"].value_counts().sort_index()
    ax.bar(first.index, first.values, width=0.58, color="#9CC3A5")
    ax.set_title("企业首次进入年份分布", pad=16)
    ax.set_xlabel("首次进入年份")
    ax.set_ylabel("企业数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    savefig(DIRS["lifecycle"] / "fig16_企业首次进入年份分布")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    grid_counts = firm["grid_count"].clip(upper=6).value_counts().sort_index()
    labels = [str(i) if i < 6 else "6及以上" for i in grid_counts.index]
    ax.bar(labels, grid_counts.values, color="#C7A76C", width=0.58)
    ax.set_title("企业样本期内涉及格网数量分布", pad=16)
    ax.set_xlabel("企业涉及格网数量")
    ax.set_ylabel("企业数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    for x, y in zip(range(len(labels)), grid_counts.values):
        ax.annotate(fmt_int(y), (x, y), xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=13)
    savefig(DIRS["lifecycle"] / "fig17_企业涉及格网数量分布")


def fig_grid_structure(t: dict[str, pd.DataFrame]) -> None:
    grid = t["grid_life"]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    counts = grid["active_years"].value_counts().sort_index()
    ax.bar(counts.index, counts.values, width=0.65, color="#A6CEE3")
    ax.set_title("格网活跃年数分布", pad=16)
    ax.set_xlabel("2015-2024年中活跃年数")
    ax.set_ylabel("格网数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    savefig(DIRS["grid_structure"] / "fig18_格网活跃年数分布")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    order = ["从未活跃", "短期活跃", "间歇活跃", "长期活跃", "十年持续活跃"]
    type_counts = grid["type"].value_counts().reindex(order).fillna(0)
    ax.bar(order, type_counts.values, color=["#D9D9D9", "#BFD8B8", "#9CC3A5", "#5F9E6E", "#2F6B45"], width=0.58)
    ax.set_title("格网活跃稳定性类型", pad=16)
    ax.set_xlabel("格网类型")
    ax.set_ylabel("格网数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    for i, y in enumerate(type_counts.values):
        ax.annotate(fmt_int(y), (i, y), xytext=(0, 8), textcoords="offset points",
                    ha="center", fontsize=13)
    savefig(DIRS["grid_structure"] / "fig19_格网活跃稳定性类型")


def fig_dl(df9: pd.DataFrame, t: dict[str, pd.DataFrame]) -> None:
    annual = t["annual"]
    nrows = int(df9["row_id"].max())
    ncols = int(df9["col_id"].max())
    sample = df9[df9["year"].isin([2015, 2024])].copy()
    fig = plt.figure(figsize=(12.5, 6.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.035], wspace=0.18)
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1])]
    cax = fig.add_subplot(gs[0, 2])
    vmax = max(1, np.nanpercentile(sample.loc[sample["valid_mask"] == 1, "active_cnt"], 99.5))
    for ax, year in zip(axes, [2015, 2024]):
        g = sample[sample["year"] == year]
        arr = np.full((nrows, ncols), np.nan)
        rr = g["row_id"].astype(int).values - 1
        cc = g["col_id"].astype(int).values - 1
        vals = g["active_cnt"].astype(float).values
        valid = g["valid_mask"].astype(int).values
        arr[rr, cc] = np.where(valid == 1, vals, np.nan)
        im = ax.imshow(arr, cmap="YlGnBu", vmin=0, vmax=vmax, interpolation="nearest")
        ax.set_title(f"{year}年 active_cnt 矩阵", fontsize=19, fontweight="bold")
        ax.set_xlabel("列号")
        ax.set_ylabel("行号")
        ax.set_xticks([])
        ax.set_yticks([])
    cbar = fig.colorbar(im, cax=cax)
    cbar.set_label("企业数量")
    fig.suptitle("完整DL格网面板矩阵化展示", fontsize=24, y=0.99, fontweight="bold")
    savefig(DIRS["dl"] / "fig20_DL完整格网active_cnt矩阵_2015与2024")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.plot(annual["year"], annual["nonzero_ratio_valid"] * 100, marker="o", color="#4C78A8", label="有效格网非零比例")
    ax.plot(annual["year"], annual["nonzero_ratio_full"] * 100, marker="s", color="#E15759", label="完整矩阵非零比例")
    ax.set_title("DL格网面板非零格网比例变化", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("非零格网比例（%）")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left")
    savefig(DIRS["dl"] / "fig21_DL非零格网比例变化")

    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.axis("off")
    x0, y0 = 0.08, 0.45
    layers = [
        ("年份", "10年\n2015-2024"),
        ("行列", "305 × 226"),
        ("特征", "active/entry/persist\nrenew/capital/size/cat"),
        ("预测目标", "下一年企业数量\n或高增长格网"),
    ]
    for i, (title, text) in enumerate(layers):
        x = x0 + i * 0.23
        ax.add_patch(Rectangle((x, y0), 0.18, 0.24, lw=1.2, edgecolor="#555555", facecolor="#F7F7F7"))
        ax.text(x + 0.09, y0 + 0.17, title, ha="center", va="center", fontsize=17, fontweight="bold")
        ax.text(x + 0.09, y0 + 0.075, text, ha="center", va="center", fontsize=14, linespacing=1.35)
        if i < len(layers) - 1:
            ax.annotate("", xy=(x + 0.22, y0 + 0.12), xytext=(x + 0.18, y0 + 0.12),
                        arrowprops=dict(arrowstyle="->", lw=1.4, color="#555555"))
    ax.set_title("时空预测张量组织示意", fontsize=23, pad=12, fontweight="bold")
    ax.text(0.5, 0.25, "数据组织形式：year × row_id × col_id × feature",
            ha="center", va="center", fontsize=17, fontweight="bold")
    savefig(DIRS["dl"] / "fig22_时空预测张量组织示意")


def fig_validation(t: dict[str, pd.DataFrame]) -> None:
    a = t["annual"]
    v = t["validation"]
    fig, ax = plt.subplots(figsize=(12, 6.4))
    ax.plot(a["year"], a["point_records"], marker="o", color="#4C78A8", label="点位表年度记录数")
    ax.plot(a["year"], a["active_total"], marker="s", ls="--", color="#E15759", label="格网active_cnt年度总和")
    ax.set_title("点位表与格网面板年度数量一致性", pad=16)
    ax.set_xlabel("年份")
    ax.set_ylabel("企业数量")
    ax.grid(axis="y")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left")
    ax.text(0.02, 0.88, f"最大差值：{int(a['point_grid_diff'].abs().max())}",
            transform=ax.transAxes, fontsize=15)
    savefig(DIRS["validation"] / "fig23_点位与格网年度数量一致性")

    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.axis("off")
    ax.set_title("阶段一CSV数据一致性校验", fontsize=23, pad=12, fontweight="bold")
    y = 0.78
    for _, row in v.iterrows():
        color = "#2F7D4F" if row["result"] == "PASS" else "#B22222"
        ax.text(0.05, y, row["check_item"], fontsize=15, va="center")
        ax.text(0.75, y, row["result"], fontsize=15, va="center", color=color, fontweight="bold")
        ax.text(0.88, y, f"最大差值 {row['max_abs_diff']}", fontsize=15, va="center")
        y -= 0.17
    savefig(DIRS["validation"] / "fig24_CSV数据一致性校验")


def write_manifest() -> pd.DataFrame:
    rows = [
        ("01", "01_数据底板结构", "fig01_阶段一核心CSV数据底板规模", "展示三类核心CSV的数据规模。"),
        ("02", "01_数据底板结构", "fig02_阶段一CSV数据底板关系", "展示企业点位、有效格网面板、完整DL格网面板关系。"),
        ("03", "02_年度增长与动态变量", "fig03_活跃企业数量与年度净增长", "展示活跃企业数量及年度净增长。"),
        ("04", "02_年度增长与动态变量", "fig04_活跃企业同比增长率", "展示年度增长率。"),
        ("05", "02_年度增长与动态变量", "fig05_企业动态变量年度变化", "展示新增、持续、续认定和退出代理。"),
        ("06", "02_年度增长与动态变量", "fig06_企业动态变量年度占比结构", "展示动态变量结构比例。"),
        ("07", "03_格网扩展与承载", "fig07_格网覆盖范围与承载强度变化", "展示活跃格网数量和格网企业承载强度变化。"),
        ("08", "03_格网扩展与承载", "fig08_高承载格网数量年度变化", "展示高承载格网数量。"),
        ("09", "03_格网扩展与承载", "fig09_格网企业承载集中度变化", "展示Gini、HHI和Top格网承载比例。"),
        ("10", "04_企业属性结构", "fig10_技术门类年度结构变化", "展示技术门类年度占比。"),
        ("11", "04_企业属性结构", "fig11_主要技术门类年度数量变化", "展示主要技术门类数量变化。"),
        ("12", "04_企业属性结构", "fig12_企业规模年度结构变化", "展示企业规模结构。"),
        ("13", "04_企业属性结构", "fig13_技术门类与企业规模结构交叉", "展示门类与规模交叉结构。"),
        ("14", "04_企业属性结构", "fig14_注册资本年度分布_对数尺度", "展示注册资本长尾分布。"),
        ("15", "05_企业生命周期", "fig15_企业样本内活跃年限分布", "展示企业活跃年限。"),
        ("16", "05_企业生命周期", "fig16_企业首次进入年份分布", "展示企业首次进入年份。"),
        ("17", "05_企业生命周期", "fig17_企业涉及格网数量分布", "展示企业格网变化潜在情况。"),
        ("18", "06_格网结构特征", "fig18_格网活跃年数分布", "展示格网活跃年数。"),
        ("19", "06_格网结构特征", "fig19_格网活跃稳定性类型", "展示格网稳定性类型。"),
        ("20", "07_DL矩阵预测底板", "fig20_DL完整格网active_cnt矩阵_2015与2024", "展示矩阵化active_cnt对比。"),
        ("21", "07_DL矩阵预测底板", "fig21_DL非零格网比例变化", "展示DL面板零膨胀程度。"),
        ("22", "07_DL矩阵预测底板", "fig22_时空预测张量组织示意", "展示时空张量组织方式。"),
        ("23", "08_数据一致性校验", "fig23_点位与格网年度数量一致性", "展示点位与格网数量一致。"),
        ("24", "08_数据一致性校验", "fig24_CSV数据一致性校验", "展示四项校验结果。"),
    ]
    df = pd.DataFrame(rows, columns=["figure_id", "folder", "file_stem", "purpose"])
    df["png_path"] = df["folder"] + "/" + df["file_stem"] + ".png"
    df["pdf_path"] = df["folder"] + "/" + df["file_stem"] + ".pdf"
    df["svg_path"] = df["folder"] + "/" + df["file_stem"] + ".svg"
    df.to_csv(TABLE_DIR / "阶段一_增强版汇报图件清单.csv", index=False, encoding="utf-8-sig")
    return df


def write_readmes(t: dict[str, pd.DataFrame], manifest: pd.DataFrame) -> None:
    annual = t["annual"]
    validation = t["validation"]
    lines = [
        "# 阶段一增强版CSV汇报图件说明",
        "",
        "本批图件基于阶段一 7、8、9 三类最终CSV产出生成，用于中期答辩展示数据处理成果，不替代后续ArcGIS Pro空间集聚、影响因素和时空预测实验结果图。",
        "",
        "## 输出格式",
        "",
        "- 每张图均输出 PNG、PDF、SVG 三种格式。",
        "- PNG 为 600ppi；PDF/SVG 为矢量格式，适合放入PPT或后续排版。",
        "",
        "## 图件分组",
        "",
    ]
    for folder, g in manifest.groupby("folder", sort=False):
        lines.append(f"### {folder}")
        for _, r in g.iterrows():
            lines.append(f"- `{r['file_stem']}`：{r['purpose']}")
        lines.append("")
    lines += [
        "## 关键校验",
        "",
    ]
    for _, r in validation.iterrows():
        lines.append(f"- {r['check_item']}：{r['result']}，最大差值 {r['max_abs_diff']}")
    lines += [
        "",
        "## 核心统计口径",
        "",
        f"- 年份范围：{int(annual['year'].min())}-{int(annual['year'].max())}",
        f"- 企业年度点位记录数：{fmt_int(annual['point_records'].sum())}",
        f"- 有效格网年度面板记录数：{fmt_int(int(annual['valid_grids'].iloc[0]) * annual['year'].nunique())}",
        f"- 完整DL格网年度面板记录数：{fmt_int(int(annual['full_cells'].iloc[0]) * annual['year'].nunique())}",
        f"- 2015年活跃企业数：{fmt_int(annual.loc[annual['year'] == 2015, 'active_total'].iloc[0])}",
        f"- 2024年活跃企业数：{fmt_int(annual.loc[annual['year'] == 2024, 'active_total'].iloc[0])}",
    ]
    (FIG_DIR / "README_阶段一增强版CSV汇报图件说明.md").write_text("\n".join(lines), encoding="utf-8")

    meta_dir = REPORT_DIR / "00_汇报总览"
    meta_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "stage1_enhanced_csv_figures_v3",
        "figure_count": int(len(manifest)),
        "formats": ["png_600ppi", "pdf", "svg"],
        "source_csv": {
            "grid_panel": str(P7),
            "firm_points": str(P8),
            "full_grid_panel": str(P9),
        },
        "validation": validation.to_dict(orient="records"),
        "note": "Enhanced descriptive figures based only on stage-one CSV outputs 7, 8 and 9.",
    }
    (meta_dir / "generation_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    setup_dirs()
    setup_style()
    df7, df8, df9 = load_data()
    tables = build_tables(df7, df8, df9)
    fig_structure(df7, df8, df9)
    fig_dynamic(tables)
    fig_grid_load(tables)
    fig_attribute(df8, tables)
    fig_lifecycle(tables)
    fig_grid_structure(tables)
    fig_dl(df9, tables)
    fig_validation(tables)
    manifest = write_manifest()
    write_readmes(tables, manifest)

    if not (tables["validation"]["result"] == "PASS").all():
        raise RuntimeError("Validation failed. Inspect 阶段一_CSV数据一致性校验表.csv")

    pngs = sorted(FIG_DIR.rglob("*.png"))
    pdfs = sorted(FIG_DIR.rglob("*.pdf"))
    svgs = sorted(FIG_DIR.rglob("*.svg"))
    print(f"Generated PNG/PDF/SVG: {len(pngs)}/{len(pdfs)}/{len(svgs)}")
    print("Validation PASS")


if __name__ == "__main__":
    main()
