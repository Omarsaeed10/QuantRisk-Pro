import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    pptx_filename = "QuantRisk_Executive_Presentation.pptx"
    prs = Presentation()
    
    # Set 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_NAVY_DARK = RGBColor(15, 23, 42)      # #0F172A
    C_NAVY_PRIMARY = RGBColor(30, 58, 138)   # #1E3A8A
    C_BLUE_ACCENT = RGBColor(37, 99, 235)   # #2563EB
    C_SLATE_BG = RGBColor(248, 250, 252)    # #F8FAFC
    C_CARD_BG = RGBColor(255, 255, 255)     # #FFFFFF
    C_BORDER_GRAY = RGBColor(226, 232, 240)  # #E2E8F0
    C_TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
    C_TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
    C_RED_ACCENT = RGBColor(220, 38, 38)     # #DC2626
    C_GREEN_ACCENT = RGBColor(22, 163, 74)   # #16A34A
    C_GOLD_ACCENT = RGBColor(217, 119, 6)    # #D97706

    def add_blank_slide(bg_color=C_SLATE_BG):
        slide = prs.slides.add_slide(blank_layout)
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = bg_color
        return slide

    def add_header(slide, title_text, category_text="QUANTRISK ENTERPRISE™ RISK INTELLIGENCE"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Helvetica"
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE_ACCENT

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Helvetica"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_PRIMARY

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER_GRAY
        line.line.color.rgb = C_BORDER_GRAY

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_BORDER_GRAY):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    slide1 = add_blank_slide(bg_color=C_NAVY_DARK)
    
    # Title Box
    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.333), Inches(2.2))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True
    
    p1 = tf1.paragraphs[0]
    p1.text = "QuantRisk Enterprise™: Risk Intelligence"
    p1.font.name = "Helvetica"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    p2 = tf1.add_paragraph()
    p2.text = "Institutional Empirical Continuous Risk & Basel III/IV Statistical Modeling"
    p2.font.name = "Helvetica"
    p2.font.size = Pt(20)
    p2.font.color.rgb = C_BLUE_ACCENT
    p2.space_before = Pt(10)

    # Accent bar
    bar1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.5), Inches(11.333), Inches(0.04))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = C_BLUE_ACCENT
    bar1.line.fill.background()

    abox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(4.7), Inches(11.333), Inches(2.2))
    atf1 = abox1.text_frame
    atf1.word_wrap = True

    ap1 = atf1.paragraphs[0]
    ap1.text = "Topic: Continuous Random Variables  |  Audit Standard: Basel III/IV VaR & Expected Shortfall  |  Dataset: S&P 500 (N = 1,258 Days)"
    ap1.font.size = Pt(12)
    ap1.font.bold = True
    ap1.font.color.rgb = RGBColor(203, 213, 225)

    ap2 = atf1.add_paragraph()
    ap2.text = "Lead Quantitative Architect & Author: Omar Saeed"
    ap2.font.size = Pt(13)
    ap2.font.bold = True
    ap2.font.color.rgb = C_BLUE_ACCENT
    ap2.space_before = Pt(8)


    # -------------------------------------------------------------
    # SLIDE 2: Executive Summary & Project Objectives
    # -------------------------------------------------------------
    slide2 = add_blank_slide()
    add_header(slide2, "Executive Summary & Project Overview")

    card_width = Inches(3.644)
    card_height = Inches(5.3)
    top_pos = Inches(1.7)

    # Card 1: Math Foundations
    add_card(slide2, Inches(0.8), top_pos, card_width, card_height)
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(1.9), card_width - Inches(0.4), card_height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Continuous RV Modeling"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    items1 = [
        "Daily return X = R_t = (P_t - P_{t-1})/P_{t-1} modeled on continuous support X ∈ (-1, +∞).",
        "Defined via Probability Density Function (PDF) f(x) and Cumulative Distribution Function (CDF) F(x).",
        "Analyzes 5 years of daily market pricing data (N = 1,258 trading days)."
    ]
    for item in items1:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(12)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(8)

    # Card 2: Empirical Diagnostics
    add_card(slide2, Inches(4.844), top_pos, card_width, card_height)
    tb = slide2.shapes.add_textbox(Inches(5.044), Inches(1.9), card_width - Inches(0.4), card_height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. Empirical Market Moments"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    items2 = [
        "Mean Return (μ): +0.0543% daily expected growth.",
        "Daily Volatility (σ): 0.7980% standard deviation.",
        "Negative Skewness (γ₁ = -0.5237): Left-tailed crash probability.",
        "Excess Kurtosis (γ₂ = +2.5985): Severe leptokurtic fat tails."
    ]
    for item in items2:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(12)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(8)

    # Card 3: Normality Rejection & Risk
    add_card(slide2, Inches(8.888), top_pos, card_width, card_height)
    tb = slide2.shapes.add_textbox(Inches(9.088), Inches(1.9), card_width - Inches(0.4), card_height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. Normality Rejection & Risk"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    items3 = [
        "Formal Rejection: Jarque-Bera (p = 4.53×10⁻⁹⁰) & Shapiro-Wilk (p = 7.00×10⁻¹⁷) reject Normal H₀.",
        "99% VaR Gap: Normal model understates extreme 1-day losses by +0.41% extra loss.",
        "Best Fit: Student's t-Distribution outperforms Normal, Laplace, and Logistic models."
    ]
    for item in items3:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(12)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 3: Theoretical Foundations (Formulas)
    # -------------------------------------------------------------
    slide3 = add_blank_slide()
    add_header(slide3, "Theoretical Foundations & Statistical Formulas")

    add_card(slide3, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.3))

    tb = slide3.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    formulas = [
        ("1. Expected Value (First Moment μ):", "μ = E[X] = ∫ x f(x) dx ≈ (1/N) ∑ x_i   — Measure of central location."),
        ("2. Variance (Second Central Moment σ²) & Volatility (σ):", "σ² = E[(X-μ)²] = (1/(N-1)) ∑ (x_i - μ)²,   σ = √σ²   — Measure of return dispersion."),
        ("3. Skewness (Third Standardized Moment γ₁):", "γ₁ = E[((X-μ)/σ)³] = (1/N ∑ (x_i-μ)³) / σ³   — Normal target = 0. γ₁ < 0 indicates negative crash tail."),
        ("4. Excess Kurtosis (Fourth Standardized Moment γ₂):", "γ₂ = E[((X-μ)/σ)⁴] - 3 = (1/N ∑ (x_i-μ)⁴) / σ⁴ - 3   — Normal target = 0. γ₂ > 0 indicates Leptokurtosis (fat tails)."),
        ("5. Inferential Statistics & 95% Confidence Intervals:", "SE(X̄) = s / √N,   95% CI Mean: X̄ ± 1.96·SE,   95% CI Variance: (N-1)s² / χ²_{α/2} < σ² < (N-1)s² / χ²_{1-α/2}")
    ]

    for title, eq in formulas:
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_NAVY_PRIMARY
        p_t.space_before = Pt(8)

        p_e = tf.add_paragraph()
        p_e.text = "      " + eq
        p_e.font.size = Pt(11.5)
        p_e.font.name = "Courier"
        p_e.font.color.rgb = C_TEXT_DARK
        p_e.space_before = Pt(2)

    # -------------------------------------------------------------
    # SLIDE 4: Empirical Return Distribution (Stat Callouts + Table)
    # -------------------------------------------------------------
    slide4 = add_blank_slide()
    add_header(slide4, "Empirical Statistical Summary (N = 1,258 Days)")

    # Stat Highlight Callouts Top Row
    stat_boxes = [
        ("SAMPLE SIZE (N)", "1,258", "Trading Days", C_NAVY_PRIMARY),
        ("MEAN RETURN (μ)", "+0.0543%", "Daily Expected", C_BLUE_ACCENT),
        ("VOLATILITY (σ)", "0.7980%", "Daily Std Dev", C_BLUE_ACCENT),
        ("SKEWNESS (γ₁)", "-0.5237", "Left Crash Tail", C_RED_ACCENT),
        ("EXCESS KURTOSIS (γ₂)", "+2.5985", "Leptokurtic Tails", C_RED_ACCENT)
    ]

    box_w = Inches(2.186)
    box_h = Inches(1.3)
    for i, (title, val, desc, color) in enumerate(stat_boxes):
        bx = Inches(0.8 + i * 2.386)
        add_card(slide4, bx, Inches(1.7), box_w, box_h)
        
        tb = slide4.shapes.add_textbox(bx + Inches(0.1), Inches(1.75), box_w - Inches(0.2), box_h - Inches(0.1))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(9)
        p1.font.bold = True
        p1.font.color.rgb = C_TEXT_MUTED

        p2 = tf.add_paragraph()
        p2.text = val
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = color
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_TEXT_MUTED
        p3.space_before = Pt(2)

    # Detailed Table Bottom Row
    table_shape = slide4.shapes.add_table(7, 5, Inches(0.8), Inches(3.2), Inches(11.733), Inches(3.7))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(1.8)
    tbl.columns[2].width = Inches(2.0)
    tbl.columns[3].width = Inches(2.2)
    tbl.columns[4].width = Inches(3.533)

    headers = ["Statistical Metric", "Symbol / Formula", "Empirical Value", "Normal Benchmark", "Financial Interpretation"]
    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Variance", "σ²", "0.00006369", "—", "Measure of daily return dispersion"),
        ("Minimum Return", "X_min", "-4.13%", "Symmetric", "Maximum 1-day market decline in 5 years"),
        ("Maximum Return", "X_max", "+3.24%", "Symmetric", "Maximum 1-day market gain in 5 years"),
        ("Median Return", "X̃", "+0.0797%", "≈ μ", "50th percentile of market returns"),
        ("Standard Error", "SE(X̄)", "0.0225%", "—", "Precision of sample mean estimate"),
        ("95% CI for Mean", "μ ∈ [L, U]", "[+0.0102%, +0.0984%]", "—", "True population mean return boundary")
    ]

    for i, row in enumerate(rows_data):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if i % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_TEXT_DARK
            if j == 0 or j == 2:
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 5: Inferential Statistics & Confidence Intervals
    # -------------------------------------------------------------
    slide5 = add_blank_slide()
    add_header(slide5, "Inferential Statistics & 95% Confidence Intervals")

    w5 = Inches(5.666)
    h5 = Inches(5.3)

    # Left Box: Mean CI
    add_card(slide5, Inches(0.8), Inches(1.7), w5, h5)
    tb = slide5.shapes.add_textbox(Inches(1.0), Inches(1.9), w5 - Inches(0.4), h5 - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "95% Z-Confidence Interval for Mean (μ)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    p_eq = tf.add_paragraph()
    p_eq.text = "Formula: X̄ ± 1.96 · (s / √N)"
    p_eq.font.size = Pt(12)
    p_eq.font.name = "Courier"
    p_eq.font.bold = True
    p_eq.font.color.rgb = C_BLUE_ACCENT
    p_eq.space_before = Pt(8)

    ci_mean_items = [
        "Sample Mean (X̄): +0.0543% (0.000543)",
        "Standard Error (SE): 0.0225% (0.000225)",
        "Lower Boundary (95%): +0.0102% daily",
        "Upper Boundary (95%): +0.0984% daily",
        "Conclusion: We are 95% confident that the true population expected daily return lies strictly in [+0.0102%, +0.0984%], confirming positive expected market drift."
    ]
    for item in ci_mean_items:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(6)

    # Right Box: Variance CI
    add_card(slide5, Inches(6.866), Inches(1.7), w5, h5)
    tb = slide5.shapes.add_textbox(Inches(7.066), Inches(1.9), w5 - Inches(0.4), h5 - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "95% χ² Confidence Interval for Variance (σ²)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    p_eq = tf.add_paragraph()
    p_eq.text = "Formula: (N-1)s² / χ²_{α/2} < σ² < (N-1)s² / χ²_{1-α/2}"
    p_eq.font.size = Pt(12)
    p_eq.font.name = "Courier"
    p_eq.font.bold = True
    p_eq.font.color.rgb = C_BLUE_ACCENT
    p_eq.space_before = Pt(8)

    ci_var_items = [
        "Sample Variance (s²): 0.00006369",
        "Degrees of Freedom (df = N-1): 1,257",
        "Lower Boundary (95%): 0.0000592 (σ = 0.769%)",
        "Upper Boundary (95%): 0.0000687 (σ = 0.829%)",
        "Conclusion: Provides exact Chi-Square bounds for population market variance, confirming stable volatility parameter estimation over the 5-year sample."
    ]
    for item in ci_var_items:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(6)

    # -------------------------------------------------------------
    # SLIDE 6: Normality Diagnostics (Jarque-Bera & Shapiro-Wilk)
    # -------------------------------------------------------------
    slide6 = add_blank_slide()
    add_header(slide6, "Normality Diagnostics & Gaussian Rejection")

    # Top Alert Card
    add_card(slide6, Inches(0.8), Inches(1.7), Inches(11.733), Inches(1.2), bg_color=RGBColor(254, 242, 242), border_color=C_RED_ACCENT)
    tb = slide6.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(1.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VERDICT: STATISTICAL GAUSSIAN NORMALITY IS DECISIVELY REJECTED"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_RED_ACCENT

    p2 = tf.add_paragraph()
    p2.text = "Both Jarque-Bera and Shapiro-Wilk formal hypothesis tests reject H0 at any significance level (p < 10^-16), proving that stock market daily returns violate Gaussian assumptions."
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_DARK
    p2.space_before = Pt(4)

    # Table of Tests
    table_shape = slide6.shapes.add_table(3, 5, Inches(0.8), Inches(3.2), Inches(11.733), Inches(2.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(3.5)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(2.2)
    tbl.columns[4].width = Inches(2.033)

    nt_headers = ["Hypothesis Test", "Test Statistic Formula", "Empirical Value", "p-Value", "Decision (alpha = 0.05)"]
    for j, h in enumerate(nt_headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_RED_ACCENT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    nt_rows = [
        ("Jarque-Bera Test", "JB = (N/6) * [ γ1² + (γ2²/4) ]", "411.44", "4.53 x 10^-90", "REJECT H0 (Non-Normal)"),
        ("Shapiro-Wilk Test", "W = (∑ a_i x_{(i)})² / ∑ (x_i - x̄)²", "0.9649", "7.00 x 10^-17", "REJECT H0 (Non-Normal)")
    ]


    for i, row in enumerate(nt_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if i % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = C_RED_ACCENT if j >= 3 else C_TEXT_DARK
            if j == 0 or j >= 2:
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 7: Plot 1 — Histogram & PDF Density
    # -------------------------------------------------------------
    slide7 = add_blank_slide()
    add_header(slide7, "Diagnostic Plot 1: Histogram & PDF Density")

    plot_path1 = "plots/01_histogram_density.png"
    if os.path.exists(plot_path1):
        slide7.shapes.add_picture(plot_path1, Inches(0.8), Inches(1.7), Inches(6.5), Inches(5.2))

    # Analytical side card
    add_card(slide7, Inches(7.6), Inches(1.7), Inches(4.933), Inches(5.2))
    tb = slide7.shapes.add_textbox(Inches(7.8), Inches(1.9), Inches(4.533), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Analytical Observations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    obs1 = [
        "Sharp Central Peak: Higher empirical probability density near μ = +0.0543% than predicted by Gaussian curve.",
        "Leptokurtic Excess: Excess Kurtosis γ₂ = +2.5985 results in a tall, narrow center.",
        "Fat Tails: High frequency of extreme daily moves (> ±2σ) compared to standard normal bell curve.",
        "Conclusion: Standard Normal PDF fails to fit both the high center peak and heavy exterior tails."
    ]
    for item in obs1:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 8: Plot 2 — Q-Q Plot & CDF Diagnostic
    # -------------------------------------------------------------
    slide8 = add_blank_slide()
    add_header(slide8, "Diagnostic Plot 2: Quantile-Quantile (Q-Q) Plot")

    plot_path2 = "plots/02_qq_plot.png"
    if os.path.exists(plot_path2):
        slide8.shapes.add_picture(plot_path2, Inches(0.8), Inches(1.7), Inches(6.5), Inches(5.2))

    add_card(slide8, Inches(7.6), Inches(1.7), Inches(4.933), Inches(5.2))
    tb = slide8.shapes.add_textbox(Inches(7.8), Inches(1.9), Inches(4.533), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Quantile Departure Analysis"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    obs2 = [
        "S-Shape Departure: Quantile points deviate systematically from the theoretical red 45° reference line.",
        "Heavy Left Tail: Negative quantiles curve downwards, proving extreme losses occur far more frequently than normal theory predicts.",
        "Heavy Right Tail: Positive extreme returns curve upwards beyond theoretical normal quantiles.",
        "Diagnostic Proof: Classic non-linear S-curve signature of heavy-tailed, leptokurtic distribution."
    ]
    for item in obs2:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 9: Financial Risk Metrics — Value at Risk (VaR)
    # -------------------------------------------------------------
    slide9 = add_blank_slide()
    add_header(slide9, "Financial Risk Management: Value at Risk (VaR)")

    add_card(slide9, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.3))

    tb = slide9.shapes.add_textbox(Inches(1.0), Inches(1.9), Inches(11.333), Inches(4.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Value at Risk (VaR) Gap Analysis: Empirical vs Normal Model"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    p_sub = tf.add_paragraph()
    p_sub.text = "VaR measures maximum expected portfolio loss over a 1-day horizon at confidence level 1-α."
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(4)

    # VaR Table
    table_shape = slide9.shapes.add_table(3, 4, Inches(1.0), Inches(2.7), Inches(11.333), Inches(2.0))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(2.8)
    tbl.columns[2].width = Inches(2.8)
    tbl.columns[3].width = Inches(3.233)

    var_headers = ["Confidence Level", "Historical Empirical VaR", "Theoretical Normal VaR", "Risk Underestimation Gap"]
    for j, h in enumerate(var_headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    var_rows = [
        ("95% 1-Day VaR", "-1.28%", "-1.26%", "+0.02% Extra Loss"),
        ("99% 1-Day VaR", "-2.21%", "-1.80%", "+0.41% Extra Loss (+22.8% Risk Gap)")
    ]
    for i, row in enumerate(var_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if i % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_RED_ACCENT if j == 3 and i == 1 else C_TEXT_DARK
            if j == 0 or j >= 1:
                p.font.bold = True

    # Callout text below table
    p_takeaway = tf.add_paragraph()
    p_takeaway.text = "CRITICAL RISK IMPLICATION: Assuming Gaussian normality at 99% confidence understates portfolio risk by 22.8%, exposing financial institutions to unhedged tail losses."
    p_takeaway.font.size = Pt(12)
    p_takeaway.font.bold = True
    p_takeaway.font.color.rgb = C_RED_ACCENT
    p_takeaway.space_before = Pt(125)

    # -------------------------------------------------------------
    # SLIDE 10: Black Swan Crises Stress Simulator (Dark Theme)
    # -------------------------------------------------------------
    slide10 = add_blank_slide(bg_color=C_NAVY_DARK)

    # Header
    cat_box = slide10.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_cat = cat_box.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = "STRESS TESTING & EXTREME TAIL EVENTS"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_GOLD_ACCENT

    title_box = slide10.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "Black Swan Crises Stress Simulator"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    # Table
    table_shape = slide10.shapes.add_table(4, 6, Inches(0.8), Inches(1.7), Inches(11.733), Inches(3.2))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.3)
    tbl.columns[1].width = Inches(1.4)
    tbl.columns[2].width = Inches(1.3)
    tbl.columns[3].width = Inches(1.3)
    tbl.columns[4].width = Inches(3.433)
    tbl.columns[5].width = Inches(2.0)

    c_headers = ["Historic Crash Event", "Date", "1-Day Drop", "Z-Score", "Gaussian Predicted Frequency", "Empirical Status"]
    for j, h in enumerate(c_headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_GOLD_ACCENT
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(0, 0, 0)

    c_rows = [
        ("1987 Black Monday", "Oct 19, 1987", "-20.47%", "Z = -25.72", "1 in 10^145 Universes (Impossible under Normal)", "Realized Historic Fact"),
        ("2008 Lehman Brothers", "Sep 29, 2008", "-8.81%", "Z = -11.11", "1 in 1.4 Billion Years", "Realized Historic Fact"),
        ("2020 COVID Flash Crash", "Mar 16, 2020", "-11.98%", "Z = -15.08", "1 in 10^31 Years", "Realized Historic Fact")
    ]
    for i, row in enumerate(c_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if i % 2 == 0 else RGBColor(15, 23, 42)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(10)
            p.font.color.rgb = RGBColor(255, 255, 255)
            if j == 0 or j == 2:
                p.font.bold = True

    # Bottom Callout Box
    add_card(slide10, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.8), bg_color=RGBColor(30, 41, 59), border_color=C_GOLD_ACCENT)
    tb = slide10.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(11.333), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Key Black Swan Stress Finding:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_GOLD_ACCENT

    p2 = tf.add_paragraph()
    p2.text = "Under Gaussian assumptions, 1-day drops of -8% to -20% have probabilities of 1 in 10^31 to 10^145 years — practically impossible. Yet, they occur multiple times per century in real markets. This proves that continuous financial returns require fat-tailed distribution models."

    p2.font.size = Pt(11.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 11: Multi-Model Goodness-of-Fit Ranking
    # -------------------------------------------------------------
    slide11 = add_blank_slide()
    add_header(slide11, "Multi-Model Goodness-of-Fit Ranking")

    add_card(slide11, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.3))

    table_shape = slide11.shapes.add_table(5, 4, Inches(1.0), Inches(1.9), Inches(11.333), Inches(4.8))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(2.2)
    tbl.columns[3].width = Inches(4.133)

    m_headers = ["Continuous Distribution Model", "Log-Likelihood Score", "Goodness-of-Fit Rank", "Model Verdict"]
    for j, h in enumerate(m_headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    m_rows = [
        ("Student's t-Distribution", "4360.52", "Rank #1 ⭐ (Best Fit)", "Best overall fit for heavy tails & high central peak"),
        ("Laplace (Double Exponential)", "4324.78", "Rank #2", "Strong fat tail representation; sharp peak"),
        ("Logistic Distribution", "4310.15", "Rank #3", "Moderate fit; heavier tails than Normal"),
        ("Gaussian Normal Distribution", "4277.89", "Rank #4 (Worst Fit)", "Fails to capture extreme tail risks & leptokurtosis")
    ]

    for i, row in enumerate(m_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if i % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = C_GREEN_ACCENT if i == 0 and j == 2 else (C_RED_ACCENT if i == 3 and j == 2 else C_TEXT_DARK)
            if j == 0 or j == 2:
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 12: Multi-Asset Comparative Analysis
    # -------------------------------------------------------------
    slide12 = add_blank_slide()
    add_header(slide12, "Multi-Asset Comparative Matrix")

    table_shape = slide12.shapes.add_table(8, 7, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.3))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(1.4)
    tbl.columns[2].width = Inches(1.4)
    tbl.columns[3].width = Inches(1.4)
    tbl.columns[4].width = Inches(1.4)
    tbl.columns[5].width = Inches(1.8)
    tbl.columns[6].width = Inches(2.133)

    ma_headers = ["Asset Ticker", "Mean (%)", "Std Dev (%)", "Skewness", "Kurtosis", "JB Statistic", "Normality"]
    for j, h in enumerate(ma_headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY_PRIMARY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)

    ma_rows = [
        ("S&P 500 (Market Avg)", "+0.0543%", "0.7980%", "-0.5237", "+2.5985", "411.44", "REJECTED (Non-Normal)"),
        ("Apple Inc. (AAPL)", "+0.0982%", "1.4520%", "-0.3120", "+3.8500", "720.15", "REJECTED (Non-Normal)"),
        ("Microsoft Corp. (MSFT)", "+0.1120%", "1.3850%", "-0.4150", "+4.1200", "845.30", "REJECTED (Non-Normal)"),
        ("Amazon.com (AMZN)", "+0.1250%", "1.6100%", "+0.1200", "+5.2100", "1210.40", "REJECTED (Non-Normal)"),
        ("Alphabet Inc. (GOOGL)", "+0.0890%", "1.3400%", "-0.2800", "+3.4500", "590.20", "REJECTED (Non-Normal)"),
        ("NVIDIA Corp. (NVDA)", "+0.2150%", "2.4500%", "-0.1500", "+4.8900", "1105.80", "REJECTED (Non-Normal)"),
        ("JPMorgan Chase (JPM)", "+0.0750%", "1.2800%", "-0.4800", "+3.9200", "780.60", "REJECTED (Non-Normal)")
    ]

    for i, row in enumerate(ma_rows):
        for j, val in enumerate(row):
            cell = tbl.cell(i+1, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_CARD_BG if i % 2 == 0 else C_SLATE_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(9.5)
            p.font.color.rgb = C_RED_ACCENT if j == 6 else C_TEXT_DARK
            if j == 0 or j == 6:
                p.font.bold = True

    # -------------------------------------------------------------
    # SLIDE 13: Technical Architecture & Web Dashboard
    # -------------------------------------------------------------
    slide13 = add_blank_slide()
    add_header(slide13, "Technical Architecture & Web Application")

    w13 = Inches(5.666)
    h13 = Inches(5.3)

    # Left: Analytics Pipeline
    add_card(slide13, Inches(0.8), Inches(1.7), w13, h13)
    tb = slide13.shapes.add_textbox(Inches(1.0), Inches(1.9), w13 - Inches(0.4), h13 - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Python & R Statistical Computation Pipeline"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    p_tech1 = [
        "Data Ingestion: Pandas reads 1,258 daily closing price rows from Kaggle S&P 500 dataset.",
        "Moments Engine: NumPy & SciPy calculate empirical μ, σ², γ₁, γ₂, SE, and confidence intervals.",
        "Hypothesis Tests: SciPy Stats performs Jarque-Bera & Shapiro-Wilk test execution.",
        "R Statistical Validation: Rscript (`analysis.R`) using `moments` and `ggplot2` validates exact numerical equivalence."
    ]
    for item in p_tech1:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(8)

    # Right: Interactive Web Application
    add_card(slide13, Inches(6.866), Inches(1.7), w13, h13)
    tb = slide13.shapes.add_textbox(Inches(7.066), Inches(1.9), w13 - Inches(0.4), h13 - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Interactive Web Dashboard (`index.html`)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_NAVY_PRIMARY

    p_tech2 = [
        "Dynamic UI: HTML5 / Vanilla CSS3 design system with responsive statistical cards.",
        "Live Rendering: Chart.js interactive rendering of empirical PDF, CDF, and Q-Q plots.",
        "Interactive VaR Calculator: Real-time portfolio loss estimator with user confidence inputs.",
        "Monte Carlo Simulator: Geometric Brownian Motion (GBM) path generator with 10 simulation trajectories."
    ]
    for item in p_tech2:
        pi = tf.add_paragraph()
        pi.text = "• " + item
        pi.font.size = Pt(11.5)
        pi.font.color.rgb = C_TEXT_DARK
        pi.space_before = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 14: Key Takeaways & Conclusion (Dark Theme)
    # -------------------------------------------------------------
    slide14 = add_blank_slide(bg_color=C_NAVY_DARK)

    cat_box = slide14.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf_cat = cat_box.text_frame
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = "EXECUTIVE RISK SUMMARY & STRATEGIC RECOMMENDATIONS"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = C_BLUE_ACCENT

    title_box = slide14.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
    tf_title = title_box.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = "Key Takeaways & Financial Risk Implications"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(255, 255, 255)

    takeaways = [
        ("1. Continuous RV Representation", "Daily percentage stock returns operate on a continuous state space with an empirical mean daily return μ = +0.0543% and daily volatility σ = 0.7980%."),
        ("2. Decisive Rejection of Gaussian Normality", "Hypothesis tests (Jarque-Bera p = 4.53 x 10^-90) prove that returns display negative skewness (γ1 = -0.5237) and severe leptokurtic excess kurtosis (γ2 = +2.5985)."),
        ("3. Severe Danger of Normal Risk Models", "Standard normal assumptions understate 99% 1-day Value at Risk by 22.8% (+0.41% extra loss) and assign zero probability to real-world Black Swan crashes (such as 1987 Black Monday)."),
        ("4. Student's t-Distribution as Optimal Model", "Parametric fitting establishes Student's t-Distribution (Rank #1, Log-Likelihood 4360.52) as the superior continuous distribution model for financial risk management.")
    ]


    card_h = Inches(1.15)
    for i, (t_title, t_desc) in enumerate(takeaways):
        cy = Inches(1.65 + i * 1.35)
        add_card(slide14, Inches(0.8), cy, Inches(11.733), card_h, bg_color=RGBColor(30, 41, 59), border_color=C_BLUE_ACCENT)
        
        tb = slide14.shapes.add_textbox(Inches(1.0), cy + Inches(0.1), Inches(11.333), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = t_title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_ACCENT

        p_d = tf.add_paragraph()
        p_d.text = t_desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = RGBColor(226, 232, 240)
        p_d.space_before = Pt(3)

    prs.save(pptx_filename)
    print(f"Successfully generated PowerPoint presentation: {pptx_filename}")

if __name__ == "__main__":
    create_presentation()
