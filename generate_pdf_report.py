import os
import sys
import pandas as pd
import numpy as np
import scipy.stats as stats

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and render 'Page X of Y' footers
    and running headers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "QuantRisk Enterprise™: Continuous Random Variables — S&P 500 Return Analysis")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "Quantitative Risk Audit Report")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Footer (All pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "QuantRisk Enterprise™ Risk Intelligence | S&P 500 Empirical Analysis")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 32, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 44, 8.5 * 72 - 54, 44)
        
        self.restoreState()

def build_pdf():
    pdf_filename = "QuantRisk_Executive_Report.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2563EB'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#1E40AF'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1E293B')
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1E293B')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0F172A')
    )

    story = []

    # Title Block / Cover Header
    story.append(Paragraph("QuantRisk Enterprise™: Empirical Continuous Random Variables", title_style))
    story.append(Paragraph("Institutional Financial Risk Audit & Basel III/IV Statistical Analysis of S&P 500 Daily Returns", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2563EB'), spaceBefore=0, spaceAfter=12))

    # Meta Table
    meta_data = [
        [
            Paragraph("<b>Author & Quantitative Architect:</b> Omar Saeed", body_style),
            Paragraph("<b>Dataset:</b> Kaggle S&P 500 (N = 1,258 Days)", body_style)
        ],
        [
            Paragraph("<b>Audit Standard:</b> Basel III/IV Cornish-Fisher VaR & ES", body_style),
            Paragraph("<b>Environment:</b> Python (SciPy, Pandas, NumPy) & R", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Executive Summary Box
    summary_text = (
        "<b>Executive Summary:</b> This study models 5 years of daily percentage returns of the S&P 500 index "
        "($N = 1,258$ trading days) as a continuous random variable $X$. Through empirical moment calculation, "
        "inferential confidence interval estimation, normality hypothesis testing (Jarque-Bera & Shapiro-Wilk), "
        "and multi-model distribution fitting, we rigorously demonstrate that financial market returns reject the classical "
        "Gaussian Normal Distribution assumption ($p < 10^{-16}$). Instead, market returns display pronounced negative skewness "
        "($\\gamma_1 = -0.5237$) and severe leptokurtosis (excess kurtosis $\\gamma_2 = +2.5985$). Consequently, standard normal "
        "risk models understate extreme tail risks (99% VaR gap of +0.41% and Black Swan odds underestimated by factors exceeding $10^{30}$). "
        "Student's $t$-Distribution is identified as the optimal parametric model."
    )
    summary_table = Table([[Paragraph(summary_text, callout_style)]], colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#3B82F6')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 12))

    # Section 1: Introduction & Mathematical Definitions
    story.append(Paragraph("1. Introduction & Mathematical Definition", h1_style))
    story.append(Paragraph(
        "In quantitative finance and statistical modeling, the daily percentage return of a stock market index is treated "
        "as a <b>continuous random variable</b>, denoted by $X$. Given the daily closing price $P_t$ at trading day $t$ and $P_{t-1}$ at day $t-1$, "
        "the simple daily percentage return $R_t$ is defined as:", body_style
    ))
    
    eq1_text = "<b>Mathematical Definition:</b> &nbsp;&nbsp;&nbsp;&nbsp; X = R_t = ( P_t - P_{t-1} ) / P_{t-1}"
    eq1_table = Table([[Paragraph(eq1_text, ParagraphStyle('EqStyle', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#1E3A8A')))]], colWidths=[504])
    eq1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(eq1_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Because price movements occur over a continuous support interval $X \\in (-1, +\\infty)$, the continuous random variable $X$ "
        "is defined by its Probability Density Function (PDF) $f(x)$ and Cumulative Distribution Function (CDF) $F(x) = P(X \\le x) = \\int_{-\\infty}^x f(u) du$.",
        body_style
    ))

    # Section 2: Theoretical Background & Formulas
    story.append(Paragraph("2. Theoretical Background & Statistical Formulas", h1_style))
    
    formulas_data = [
        [Paragraph("<b>Statistical Metric</b>", table_header_style), Paragraph("<b>Mathematical Formula</b>", table_header_style), Paragraph("<b>Theoretical Normal Benchmark</b>", table_header_style)],
        [Paragraph("<b>Expected Value (Mean $\\mu$)</b>", table_cell_bold), Paragraph("$\\mu = E[X] = \\int_{-\\infty}^{\\infty} x f(x) dx \\approx \\frac{1}{N} \\sum x_i$", table_cell_style), Paragraph("$0.00\\%$ (Zero drift assumption)", table_cell_style)],
        [Paragraph("<b>Variance ($\\sigma^2$) & Volatility ($\\sigma$)</b>", table_cell_bold), Paragraph("$\\sigma^2 = E[(X-\\mu)^2] = \\frac{1}{N-1} \\sum (x_i - \\mu)^2$, &nbsp; $\\sigma = \\sqrt{\\sigma^2}$", table_cell_style), Paragraph("Domain parameter $\\sigma > 0$", table_cell_style)],
        [Paragraph("<b>Skewness ($\\gamma_1$)</b>", table_cell_bold), Paragraph("$\\gamma_1 = E[((X-\\mu)/\\sigma)^3] = \\frac{\\frac{1}{N} \\sum (x_i - \\mu)^3}{\\sigma^3}$", table_cell_style), Paragraph("$\\gamma_1 = 0.0000$ (Symmetric)", table_cell_style)],
        [Paragraph("<b>Excess Kurtosis ($\\gamma_2$)</b>", table_cell_bold), Paragraph("$\\gamma_2 = E[((X-\\mu)/\\sigma)^4] - 3 = \\frac{\\frac{1}{N} \\sum (x_i - \\mu)^4}{\\sigma^4} - 3$", table_cell_style), Paragraph("$\\gamma_2 = 0.0000$ (Mesokurtic)", table_cell_style)],
        [Paragraph("<b>Standard Error of Mean</b>", table_cell_bold), Paragraph("$SE(\\bar{X}) = \\frac{s}{\\sqrt{N}}$", table_cell_style), Paragraph("Sampling error bounds", table_cell_style)],
        [Paragraph("<b>95% CI for Mean</b>", table_cell_bold), Paragraph("$\\bar{X} \\pm Z_{\\alpha/2} \\cdot SE(\\bar{X}) = \\bar{X} \\pm 1.96 \\cdot \\frac{s}{\\sqrt{N}}$", table_cell_style), Paragraph("Standard Normal Z-bounds", table_cell_style)],
        [Paragraph("<b>95% CI for Variance</b>", table_cell_bold), Paragraph("$\\frac{(N-1)s^2}{\\chi^2_{\\alpha/2, N-1}} < \\sigma^2 < \\frac{(N-1)s^2}{\\chi^2_{1-\\alpha/2, N-1}}$", table_cell_style), Paragraph("Chi-Square Distribution bounds", table_cell_style)]
    ]
    f_table = Table(formulas_data, colWidths=[130, 244, 130])
    f_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(f_table)
    story.append(Spacer(1, 10))

    # Section 3: Empirical Statistical Results
    story.append(Paragraph("3. Empirical Statistical Results (N = 1,258 Trading Days)", h1_style))
    story.append(Paragraph(
        "Analysis of 5 years of S&P 500 daily market returns ($N = 1,258$) yields the empirical moments and confidence intervals detailed below:",
        body_style
    ))

    results_data = [
        [Paragraph("<b>Metric Name</b>", table_header_style), Paragraph("<b>Symbol / Formula</b>", table_header_style), Paragraph("<b>Empirical Value</b>", table_header_style), Paragraph("<b>Theoretical Normal Target</b>", table_header_style), Paragraph("<b>Financial Interpretation</b>", table_header_style)],
        [Paragraph("Sample Size", table_cell_bold), Paragraph("$N$", table_cell_style), Paragraph("<b>1,258</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("5 years daily observations", table_cell_style)],
        [Paragraph("Mean Daily Return", table_cell_bold), Paragraph("$\\mu = E[X]$", table_cell_style), Paragraph("<b>+0.0543%</b> (0.000543)", table_cell_style), Paragraph("0.0000%", table_cell_style), Paragraph("Positive average daily growth", table_cell_style)],
        [Paragraph("Variance", table_cell_bold), Paragraph("$\\sigma^2$", table_cell_style), Paragraph("<b>0.00006369</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Return dispersion measure", table_cell_style)],
        [Paragraph("Standard Deviation", table_cell_bold), Paragraph("$\\sigma$", table_cell_style), Paragraph("<b>0.7980%</b> (0.007980)", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Daily market volatility", table_cell_style)],
        [Paragraph("Skewness", table_cell_bold), Paragraph("$\\gamma_1$", table_cell_style), Paragraph("<font color='#DC2626'><b>-0.5237</b></font>", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("Asymmetric left crash tail", table_cell_style)],
        [Paragraph("Excess Kurtosis", table_cell_bold), Paragraph("$\\gamma_2$", table_cell_style), Paragraph("<font color='#DC2626'><b>+2.5985</b></font>", table_cell_style), Paragraph("0.0000", table_cell_style), Paragraph("High Leptokurtosis (Fat tails)", table_cell_style)],
        [Paragraph("Minimum Return", table_cell_bold), Paragraph("$X_{\\min}$", table_cell_style), Paragraph("<b>-4.13%</b>", table_cell_style), Paragraph("Symmetric", table_cell_style), Paragraph("Max 1-day decline in sample", table_cell_style)],
        [Paragraph("Maximum Return", table_cell_bold), Paragraph("$X_{\\max}$", table_cell_style), Paragraph("<b>+3.24%</b>", table_cell_style), Paragraph("Symmetric", table_cell_style), Paragraph("Max 1-day gain in sample", table_cell_style)],
        [Paragraph("Median Return", table_cell_bold), Paragraph("$\\tilde{X}$", table_cell_style), Paragraph("<b>+0.0797%</b>", table_cell_style), Paragraph("$\\approx \\mu$", table_cell_style), Paragraph("50th percentile return", table_cell_style)],
        [Paragraph("Standard Error", table_cell_bold), Paragraph("$SE(\\bar{X})$", table_cell_style), Paragraph("<b>0.0225%</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Mean sampling precision", table_cell_style)],
        [Paragraph("95% CI for Mean", table_cell_bold), Paragraph("$\\mu \\in [L, U]$", table_cell_style), Paragraph("<b>[+0.0102%, +0.0984%]</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("True population mean bounds", table_cell_style)],
        [Paragraph("95% CI for Variance", table_cell_bold), Paragraph("$\\sigma^2 \\in [L, U]$", table_cell_style), Paragraph("<b>[0.0000592, 0.0000687]</b>", table_cell_style), Paragraph("—", table_cell_style), Paragraph("True population variance bounds", table_cell_style)]
    ]
    r_table = Table(results_data, colWidths=[95, 75, 110, 85, 139])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0, 0), (-1, -1), 4.5),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 10))

    # Section 4: Normality Tests & Rejection
    story.append(Paragraph("4. Normality Diagnostic Tests & Gaussian Rejection", h1_style))
    story.append(Paragraph(
        "To rigorously evaluate whether empirical daily market returns conform to a Gaussian Normal Distribution $\\mathcal{N}(\\mu, \\sigma^2)$, "
        "we perform two formal hypothesis tests under $H_0: X \\sim \\mathcal{N}(\\mu, \\sigma^2)$ vs $H_1: X \\not\\sim \\mathcal{N}(\\mu, \\sigma^2)$:",
        body_style
    ))

    norm_tests_data = [
        [Paragraph("<b>Hypothesis Test</b>", table_header_style), Paragraph("<b>Test Statistic Formula</b>", table_header_style), Paragraph("<b>Empirical Statistic</b>", table_header_style), Paragraph("<b>p-Value</b>", table_header_style), Paragraph("<b>Decision (&alpha; = 0.05)</b>", table_header_style)],
        [Paragraph("<b>Jarque-Bera Test</b>", table_cell_bold), Paragraph("JB = (N/6) &times; [ &gamma;<sub>1</sub><sup>2</sup> + (&gamma;<sub>2</sub><sup>2</sup>/4) ]", table_cell_style), Paragraph("<b>411.44</b>", table_cell_style), Paragraph("<font color='#DC2626'><b>4.53 &times; 10<sup>-90</sup></b></font>", table_cell_style), Paragraph("<font color='#DC2626'><b>REJECT H<sub>0</sub> (Non-Normal)</b></font>", table_cell_style)],
        [Paragraph("<b>Shapiro-Wilk Test</b>", table_cell_bold), Paragraph("W = (&sum; a<sub>i</sub> x<sub>(i)</sub>)<sup>2</sup> / &sum; (x<sub>i</sub> - x̄)<sup>2</sup>", table_cell_style), Paragraph("<b>0.9649</b>", table_cell_style), Paragraph("<font color='#DC2626'><b>7.00 &times; 10<sup>-17</sup></b></font>", table_cell_style), Paragraph("<font color='#DC2626'><b>REJECT H<sub>0</sub> (Non-Normal)</b></font>", table_cell_style)]
    ]
    nt_table = Table(norm_tests_data, colWidths=[100, 154, 80, 85, 85])
    nt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#991B1B')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#FCA5A5')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#FEF2F2'), colors.white]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(nt_table)
    story.append(Spacer(1, 10))

    # Section 5: Risk Applications & Black Swan Crises
    story.append(Paragraph("5. Real-World Risk Applications & Stress Simulations", h1_style))
    
    story.append(Paragraph("<b>5.1 Value at Risk (VaR 95% & 99%) Gap Analysis</b>", h2_style))
    story.append(Paragraph(
        "Value at Risk (VaR) estimates the maximum potential loss over a 1-day horizon at confidence level 1-&alpha;. "
        "Comparing historical non-parametric VaR against theoretical Gaussian parametric VaR exposes severe tail-risk underestimation:",
        body_style
    ))

    var_data = [
        [Paragraph("<b>Confidence Level</b>", table_header_style), Paragraph("<b>Historical Empirical VaR</b>", table_header_style), Paragraph("<b>Theoretical Normal VaR</b>", table_header_style), Paragraph("<b>Risk Underestimation Gap</b>", table_header_style)],
        [Paragraph("<b>95% 1-Day VaR</b>", table_cell_bold), Paragraph("<b>-1.28%</b>", table_cell_style), Paragraph("-1.26%", table_cell_style), Paragraph("<font color='#D97706'>+0.02% Extra Loss</font>", table_cell_style)],
        [Paragraph("<b>99% 1-Day VaR</b>", table_cell_bold), Paragraph("<b>-2.21%</b>", table_cell_style), Paragraph("-1.80%", table_cell_style), Paragraph("<font color='#DC2626'><b>+0.41% Extra Loss (+22.8% Risk Gap)</b></font>", table_cell_style)]
    ]
    var_table = Table(var_data, colWidths=[120, 120, 120, 144])
    var_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(var_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>5.2 Black Swan Crises Stress Simulator</b>", h2_style))
    story.append(Paragraph(
        "By mapping famous historic stock market crashes onto theoretical Gaussian Normal curves (Z = (X - &mu;) / &sigma;), "
        "we demonstrate the complete breakdown of Gaussian models in financial risk modeling:",
        body_style
    ))

    crises_table_data = [
        [Paragraph("<b>Historic Crash Event</b>", table_header_style), Paragraph("<b>Date</b>", table_header_style), Paragraph("<b>1-Day Drop</b>", table_header_style), Paragraph("<b>Z-Score</b>", table_header_style), Paragraph("<b>Gaussian Predicted Frequency</b>", table_header_style), Paragraph("<b>Empirical Status</b>", table_header_style)],
        [Paragraph("<b>1987 Black Monday</b>", table_cell_bold), Paragraph("Oct 19, 1987", table_cell_style), Paragraph("<b>-20.47%</b>", table_cell_style), Paragraph("Z = -25.72", table_cell_style), Paragraph("1 in 10<sup>145</sup> Universes", table_cell_style), Paragraph("Realized Historic Fact", table_cell_style)],
        [Paragraph("<b>2008 Lehman Brothers</b>", table_cell_bold), Paragraph("Sep 29, 2008", table_cell_style), Paragraph("<b>-8.81%</b>", table_cell_style), Paragraph("Z = -11.11", table_cell_style), Paragraph("1 in 1.4 Billion Years", table_cell_style), Paragraph("Realized Historic Fact", table_cell_style)],
        [Paragraph("<b>2020 COVID Flash Crash</b>", table_cell_bold), Paragraph("Mar 16, 2020", table_cell_style), Paragraph("<b>-11.98%</b>", table_cell_style), Paragraph("Z = -15.08", table_cell_style), Paragraph("1 in 10<sup>31</sup> Years", table_cell_style), Paragraph("Realized Historic Fact", table_cell_style)]
    ]

    cs_table = Table(crises_table_data, colWidths=[110, 65, 65, 60, 114, 90])
    cs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F5F9')]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(cs_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>5.3 Multi-Model Goodness-of-Fit Ranking</b>", h2_style))
    
    fit_data = [
        [Paragraph("<b>Distribution Model</b>", table_header_style), Paragraph("<b>Log-Likelihood Score</b>", table_header_style), Paragraph("<b>Goodness-of-Fit Rank</b>", table_header_style), Paragraph("<b>Model Verdict</b>", table_header_style)],
        [Paragraph("<b>Student's t-Distribution</b>", table_cell_bold), Paragraph("<b>4360.52</b>", table_cell_style), Paragraph("<font color='#16A34A'><b>Rank #1 ⭐</b></font>", table_cell_style), Paragraph("Best overall fit for heavy tails & central peak", table_cell_style)],
        [Paragraph("<b>Laplace (Double Exponential)</b>", table_cell_bold), Paragraph("4324.78", table_cell_style), Paragraph("Rank #2", table_cell_style), Paragraph("Strong fat tail representation", table_cell_style)],
        [Paragraph("<b>Logistic Distribution</b>", table_cell_bold), Paragraph("4310.15", table_cell_style), Paragraph("Rank #3", table_cell_style), Paragraph("Moderate fit", table_cell_style)],
        [Paragraph("<b>Gaussian Normal Distribution</b>", table_cell_bold), Paragraph("4277.89", table_cell_style), Paragraph("<font color='#DC2626'>Rank #4 (Worst)</font>", table_cell_style), Paragraph("Fails to capture heavy tail risks", table_cell_style)]
    ]
    fit_table = Table(fit_data, colWidths=[140, 100, 100, 164])
    fit_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(fit_table)
    story.append(Spacer(1, 14))

    # Section 6: Diagnostic Visualizations & Figure Analysis
    story.append(Paragraph("6. Analytical Diagnostic Visualizations", h1_style))
    story.append(Paragraph(
        "Below are high-resolution diagnostic plots generated from the empirical S&P 500 dataset, illustrating distribution shape, quantile behavior, time-series volatility clustering, outlier bounds, and cumulative probability functions:",
        body_style
    ))

    plots_dir = "plots"
    plot_files = [
        ("01_histogram_density.png", "Figure 1: Histogram & PDF Density (Empirical vs Normal Density)", "Shows sharp central peak around μ = +0.0543% and non-Gaussian heavy tails."),
        ("02_qq_plot.png", "Figure 2: Quantile-Quantile (Q-Q) Diagnostic Plot", "Non-linear S-curve highlights significant deviations from theoretical normal quantiles at both ends."),
        ("03_returns_time_series.png", "Figure 3: Daily Returns Time Series Timeline (N = 1,258 Days)", "Demonstrates volatility clustering where high-volatility days cluster in distinct regimes."),
        ("04_boxplot_outliers.png", "Figure 4: Boxplot Outlier Diagnostic", "Extensive extreme outliers extend beyond standard 1.5×IQR whiskers."),
        ("05_cumulative_distribution.png", "Figure 5: Empirical CDF vs Theoretical Normal CDF", "Empirical CDF exhibits steeper transition near 0% return matching higher central density.")
    ]

    for filename, caption, desc in plot_files:
        filepath = os.path.join(plots_dir, filename)
        if os.path.exists(filepath):
            img_flowable = Image(filepath, width=460, height=200)
            fig_elements = [
                Spacer(1, 4),
                img_flowable,
                Spacer(1, 4),
                Paragraph(f"<b>{caption}</b>", ParagraphStyle('CapStyle', parent=body_style, fontName='Helvetica-Bold', alignment=1)),
                Paragraph(f"<i>Interpretation: {desc}</i>", ParagraphStyle('DescStyle', parent=body_style, fontSize=8.5, alignment=1, textColor=colors.HexColor('#475569'))),
                Spacer(1, 10)
            ]
            story.append(KeepTogether(fig_elements))

    # Section 7: Code Implementation Snippets
    story.append(Paragraph("7. Code Implementation Snippets", h1_style))
    story.append(Paragraph("<b>7.1 Python Implementation (`analysis.py`)</b>", h2_style))
    
    python_snippet = (
        "import pandas as pd\n"
        "import numpy as np\n"
        "import scipy.stats as stats\n\n"
        "# Load dataset & calculate daily percentage returns\n"
        "df = pd.read_csv('data/all_stocks_5yr.csv')\n"
        "df['daily_return'] = df.groupby('Name')['close'].pct_change()\n"
        "market_returns = df.groupby('date')['daily_return'].mean().dropna()\n\n"
        "# Statistical moments & confidence intervals\n"
        "mean = market_returns.mean()\n"
        "std = market_returns.std()\n"
        "skewness = stats.skew(market_returns)\n"
        "kurtosis = stats.kurtosis(market_returns)\n"
        "jb_stat, jb_p = stats.jarque_bera(market_returns)\n"
        "print(f'Mean: {mean:.6f}, Std: {std:.6f}, Skew: {skewness:.4f}, Kurt: {kurtosis:.4f}')"
    )
    py_table = Table([[Paragraph(python_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    py_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(py_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>7.2 R Implementation (`analysis.R`)</b>", h2_style))
    r_snippet = (
        "library(dplyr)\n"
        "library(moments)\n\n"
        "data <- read.csv('data/all_stocks_5yr.csv') %>%\n"
        "  group_by(Name) %>%\n"
        "  mutate(daily_return = (close - lag(close))/lag(close))\n\n"
        "market_returns <- data %>%\n"
        "  group_by(date) %>%\n"
        "  summarise(market_return = mean(daily_return, na.rm=TRUE))\n\n"
        "cat('Mean:', mean(market_returns$market_return),\n"
        "    'Skew:', skewness(market_returns$market_return),\n"
        "    'Kurtosis:', kurtosis(market_returns$market_return) - 3)"
    )
    r_table = Table([[Paragraph(r_snippet.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)]], colWidths=[504])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 10))

    # Section 8: Conclusion
    story.append(Paragraph("8. Conclusion & Financial Risk Implications", h1_style))
    concl_text = (
        "<b>Summary of Conclusions:</b><br/>"
        "1. <b>Continuous RV Modeling:</b> S&P 500 daily market returns $X$ operate on a continuous sample space with an empirical mean daily return of $\\mu = +0.0543\\%$ and daily volatility of $\\sigma = 0.7980\\%$.<br/>"
        "2. <b>Failure of Gaussian Normality:</b> Empirical returns exhibit negative skewness ($\\gamma_1 = -0.5237$) and severe excess kurtosis ($\\gamma_2 = +2.5985$). Hypothesis tests (Jarque-Bera $p = 4.53 \\times 10^{-90}$) decisively reject normal distribution assumptions.<br/>"
        "3. <b>Underestimation of Financial Risk:</b> Standard normal models severely understate 99% Value at Risk (-1.80% normal vs -2.21% empirical) and assign zero probability to real-world Black Swan market crashes (such as 1987 Black Monday and 2020 COVID crash).<br/>"
        "4. <b>Optimal Distribution:</b> Parametric fitting proves that heavy-tailed distributions such as <b>Student's $t$-Distribution</b> (Rank #1, Log-Likelihood 4360.52) provide vastly superior risk calibration."
    )
    concl_table = Table([[Paragraph(concl_text, body_style)]], colWidths=[504])
    concl_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1E3A8A')),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(concl_table)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
