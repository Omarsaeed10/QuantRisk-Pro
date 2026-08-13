// ==========================================================================
// MAT231 S&P 500 Continuous Random Variables Interactive Web Application
// Universal Dataset Analysis System
// ==========================================================================

let appData = null;
let currentTicker = "MARKET_AVG";
let activeTab = "histogram";
let mainChart = null;
let mcChart = null;

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
    fetchData();
    setupEventListeners();
});

// Fetch/Load statistical data
async function fetchData() {
    if (window.APP_DATA) {
        appData = window.APP_DATA;
        renderDashboard();
    } else {
        try {
            const response = await fetch("app_data.json");
            appData = await response.json();
            renderDashboard();
        } catch (error) {
            console.error("Error loading data:", error);
        }
    }
}

// Setup Interactive Controls
function setupEventListeners() {
    // Ticker Dropdown Change
    const tickerSelect = document.getElementById("tickerSelect");
    tickerSelect.addEventListener("change", (e) => {
        currentTicker = e.target.value;
        renderDashboard();
    });

    // Custom CSV File Upload Trigger
    const csvFileInput = document.getElementById("csvFileInput");
    if (csvFileInput) {
        csvFileInput.addEventListener("change", handleCustomCsvUpload);
    }

    // Tools & Simulators Dropdown Menu
    const toolsSelect = document.getElementById("toolsSelect");
    if (toolsSelect) {
        toolsSelect.addEventListener("change", (e) => {
            const val = e.target.value;
            if (val === "uploadCsv") {
                if (csvFileInput) csvFileInput.click();
            } else if (val === "monteCarlo") {
                const modal = document.getElementById("monteCarloModal");
                if (modal) { modal.classList.remove("hidden"); renderMonteCarloChart(); triggerMathJax(); }
            } else if (val === "models") {
                const modal = document.getElementById("modelsModal");
                if (modal) { modal.classList.remove("hidden"); renderModelsTable(); triggerMathJax(); }
            } else if (val === "matrix") {
                const modal = document.getElementById("matrixModal");
                if (modal) { modal.classList.remove("hidden"); renderMatrixTable(); triggerMathJax(); }
            } else if (val === "stress") {
                const modal = document.getElementById("stressModal");
                if (modal) { modal.classList.remove("hidden"); renderStressTable(); triggerMathJax(); }
            } else if (val === "formula") {
                const modal = document.getElementById("formulaModal");
                if (modal) { modal.classList.remove("hidden"); triggerMathJax(); }
            } else if (val === "downloadCsv") {
                downloadSummaryCsv();
            }
            toolsSelect.selectedIndex = 0; // Reset to default label
        });
    }

    // Tab Button Click
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            tabBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeTab = btn.dataset.tab;
            renderChart();
        });
    });

    // Modal Close Buttons Setup
    setupModalClose("monteCarloModal", "closeMonteCarloModal");
    setupModalClose("modelsModal", "closeModelsModal");
    setupModalClose("matrixModal", "closeMatrixModal");
    setupModalClose("stressModal", "closeStressModal");
    setupModalClose("formulaModal", "closeFormulaModal");

    // Probability Calculator Modal
    const modal = document.getElementById("calcModal");
    const calcBtn = document.getElementById("calculatorBtn");
    const closeBtn = document.getElementById("closeModal");
    const modalCalcBtn = document.getElementById("modalCalcBtn");
    const returnInput = document.getElementById("returnInput");

    if (calcBtn && modal) {
        calcBtn.addEventListener("click", () => {
            modal.classList.remove("hidden");
            calculateProbability();
            triggerMathJax();
        });
    }
    
    if (closeBtn && modal) {
        closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.add("hidden");
        });
    }

    if (returnInput) {
        returnInput.addEventListener("input", () => {
            calculateProbability();
        });
    }

    if (modalCalcBtn) {
        modalCalcBtn.addEventListener("click", () => {
            calculateProbability();
            triggerMathJax();
        });
    }

    // Print Report
    const printBtn = document.getElementById("printBtn");
    if (printBtn) {
        printBtn.addEventListener("click", () => {
            window.print();
        });
    }
}

// Modal Close Helper
function setupModalClose(modalId, closeBtnId) {
    const modal = document.getElementById(modalId);
    const closeBtn = document.getElementById(closeBtnId);
    if (closeBtn && modal) {
        closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
        modal.addEventListener("click", (e) => {
            if (e.target === modal) modal.classList.add("hidden");
        });
    }
}

function triggerMathJax() {
    if (window.MathJax && window.MathJax.typesetPromise) {
        window.MathJax.typesetPromise();
    }
}

// Custom CSV File Processing Engine
function handleCustomCsvUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (window.Papa) {
        Papa.parse(file, {
            header: true,
            dynamicTyping: true,
            skipEmptyLines: true,
            complete: function(results) {
                parseAndProcessCsvData(file.name, results.data);
            }
        });
    }
}

function parseAndProcessCsvData(fileName, rows) {
    if (!rows || rows.length < 5) return;

    // Detect columns
    const firstRow = rows[0];
    const keys = Object.keys(firstRow);
    
    let priceCol = keys.find(k => /close|price|value|val|return|ret/i.test(k));
    if (!priceCol) {
        priceCol = keys.find(k => typeof firstRow[k] === 'number');
    }
    if (!priceCol) priceCol = keys[1] || keys[0];

    let dateCol = keys.find(k => /date|time|day/i.test(k));

    const numbers = [];
    const datesList = [];

    rows.forEach(r => {
        const val = parseFloat(r[priceCol]);
        if (!isNaN(val)) {
            numbers.push(val);
            if (dateCol && r[dateCol]) datesList.push(String(r[dateCol]));
        }
    });

    if (numbers.length < 5) return;

    // Process Statistical Engine for Custom CSV
    let rets = [];
    if (numbers.length > 5 && numbers.every(n => n > 0) && (Math.max(...numbers) > 1.0)) {
        for (let i = 1; i < numbers.length; i++) {
            rets.push((numbers[i] - numbers[i-1]) / numbers[i-1]);
        }
    } else {
        rets = numbers;
    }

    const n = rets.length;
    const mean = rets.reduce((a, b) => a + b, 0) / n;
    const varVal = rets.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / (n - 1);
    const stdVal = Math.sqrt(varVal);

    const skewVal = stdVal > 0 ? rets.reduce((a, b) => a + Math.pow((b - mean) / stdVal, 3), 0) / n : 0;
    const kurtVal = stdVal > 0 ? (rets.reduce((a, b) => a + Math.pow((b - mean) / stdVal, 4), 0) / n) - 3 : 0;

    const jbStat = (n / 6) * (Math.pow(skewVal, 2) + Math.pow(kurtVal, 2) / 4);
    const jbP = Math.exp(-0.5 * jbStat);

    const sorted = [...rets].sort((a, b) => a - b);
    const minVal = sorted[0];
    const maxVal = sorted[sorted.length - 1];
    const median = sorted[Math.floor(n / 2)];
    const q25 = sorted[Math.floor(n * 0.25)];
    const q75 = sorted[Math.floor(n * 0.75)];
    const iqr = q75 - q25;

    const seMean = stdVal / Math.sqrt(n);
    const ciMeanLower = mean - 1.96 * seMean;
    const ciMeanUpper = mean + 1.96 * seMean;

    const sortedPct = sorted.map(r => r * 100);
    const var95Hist = sortedPct[Math.floor(n * 0.05)];
    const var99Hist = sortedPct[Math.floor(n * 0.01)];
    const var95Norm = (mean * 100) - 1.645 * (stdVal * 100);
    const var99Norm = (mean * 100) - 2.326 * (stdVal * 100);

    const minPct = sortedPct[0];
    const maxPct = sortedPct[sortedPct.length - 1];
    const binWidth = (maxPct - minPct) / 40 || 0.1;

    const counts = new Array(40).fill(0);
    const binCenters = [];
    for (let i = 0; i < 40; i++) {
        binCenters.push(minPct + (i + 0.5) * binWidth);
    }

    sortedPct.forEach(val => {
        let binIdx = Math.floor((val - minPct) / binWidth);
        if (binIdx >= 40) binIdx = 39;
        counts[binIdx]++;
    });

    const totalCount = sortedPct.length;
    const densityCounts = counts.map(c => (c / (totalCount * binWidth)));
    const normPdf = binCenters.map(x => stdVal > 0 ? (1 / (stdVal * 100 * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * Math.pow((x - mean * 100) / (stdVal * 100), 2)) : 0);

    const qqTheoretical = [];
    const qqSample = [];
    const stepQQ = Math.max(1, Math.floor(n / 100));
    for (let i = 0; i < n; i += stepQQ) {
        const p = (i + 0.5) / n;
        const z = invNormCdf(p);
        qqTheoretical.push(z);
        qqSample.push(sortedPct[i]);
    }

    const cdfX = [];
    const cdfEmp = [];
    const cdfNorm = [];
    for (let i = 0; i < n; i += stepQQ) {
        cdfX.push(sortedPct[i]);
        cdfEmp.push((i + 1) / n);
        const z = stdVal > 0 ? (sortedPct[i] - mean * 100) / (stdVal * 100) : 0;
        cdfNorm.push(0.5 * (1 + erf(z / Math.SQRT2)));
    }

    const dates = datesList && datesList.length === numbers.length ? datesList.slice(1) : rets.map((_, i) => `Day ${i+1}`);

    const customKey = "CUSTOM_" + Date.now();
    appData[customKey] = {
        "n": n,
        "mean": mean,
        "variance": varVal,
        "std": stdVal,
        "skewness": skewVal,
        "kurtosis": kurtVal,
        "min": minVal,
        "max": maxVal,
        "median": median,
        "q25": q25,
        "q75": q75,
        "iqr": iqr,
        "jb_stat": jbStat,
        "jb_p": jbP,
        "var_metrics": {
            "hist_95": var95Hist,
            "hist_99": var99Hist,
            "norm_95": var95Norm,
            "norm_99": var99Norm
        },
        "lecture_metrics": {
            "se_mean": seMean,
            "ci_mean": [ciMeanLower, ciMeanUpper],
            "ci_var": [varVal * 0.9, varVal * 1.1],
            "degrees_of_freedom": n - 1
        },
        "sorted_returns_pct": sortedPct.map(v => parseFloat(v.toFixed(4))),
        "histogram": {
            "counts": densityCounts,
            "bin_centers": binCenters.map(b => parseFloat(b.toFixed(3))),
            "norm_pdf": normPdf.map(p => parseFloat(p.toFixed(4)))
        },
        "qq_plot": {
            "theoretical": qqTheoretical.map(t => parseFloat(t.toFixed(3))),
            "sample": qqSample.map(s => parseFloat(s.toFixed(3)))
        },
        "cdf": {
            "x": cdfX.map(x => parseFloat(x.toFixed(3))),
            "empirical": cdfEmp.map(e => parseFloat(e.toFixed(4))),
            "normal": cdfNorm.map(n => parseFloat(n.toFixed(4)))
        },
        "time_series": {
            "dates": dates.slice(0, 500),
            "returns": rets.slice(0, 500).map(r => parseFloat((r * 100).toFixed(3)))
        }
    };

    const tickerSelect = document.getElementById("tickerSelect");
    const option = document.createElement("option");
    option.value = customKey;
    option.textContent = `📂 Custom: ${fileName}`;
    option.selected = true;
    tickerSelect.appendChild(option);

    currentTicker = customKey;
    renderDashboard();
}

// Rational Approximation for Inverse Normal CDF
function invNormCdf(p) {
    if (p <= 0) return -3.5;
    if (p >= 1) return 3.5;
    if (p < 0.5) return -invNormCdf(1 - p);
    const t = Math.sqrt(-2 * Math.log(1 - p));
    const c0 = 2.515517, c1 = 0.802853, c2 = 0.010328;
    const d1 = 1.432788, d2 = 0.189269, d3 = 0.001308;
    return t - ((c2 * t + c1) * t + c0) / (((d3 * t + d2) * t + d1) * t + 1);
}

// Download Summary Metrics CSV
function downloadSummaryCsv() {
    if (!appData || !appData[currentTicker]) return;

    const data = appData[currentTicker];
    const lm = data.lecture_metrics;
    const vm = data.var_metrics;

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Parameter,Symbol,Value\n";
    csvContent += `Ticker,,${currentTicker}\n`;
    csvContent += `Sample Size,N,${data.n}\n`;
    csvContent += `Mean Daily Return,mu,${(data.mean * 100).toFixed(6)}%\n`;
    csvContent += `Variance,sigma^2,${data.variance.toFixed(8)}\n`;
    csvContent += `Standard Deviation,sigma,${(data.std * 100).toFixed(6)}%\n`;
    csvContent += `Skewness,gamma_1,${data.skewness.toFixed(4)}\n`;
    csvContent += `Excess Kurtosis,gamma_2,${data.kurtosis.toFixed(4)}\n`;
    csvContent += `Min Daily Return,X_min,${(data.min * 100).toFixed(2)}%\n`;
    csvContent += `Max Daily Return,X_max,${(data.max * 100).toFixed(2)}%\n`;
    csvContent += `Median Daily Return,X_median,${(data.median * 100).toFixed(4)}%\n`;
    csvContent += `Standard Error,SE,${(lm.se_mean * 100).toFixed(4)}%\n`;
    csvContent += `95% CI Mean Lower,,${(lm.ci_mean[0] * 100).toFixed(4)}%\n`;
    csvContent += `95% CI Mean Upper,,${(lm.ci_mean[1] * 100).toFixed(4)}%\n`;
    csvContent += `95% VaR Historical,,${vm.hist_95.toFixed(2)}%\n`;
    csvContent += `99% VaR Historical,,${vm.hist_99.toFixed(2)}%\n`;
    csvContent += `Jarque-Bera Stat,,${data.jb_stat.toFixed(2)}\n`;

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${currentTicker}_mat231_summary.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Render Monte Carlo Simulation Chart
function renderMonteCarloChart() {
    if (!appData || !appData.ADVANCED || !appData.ADVANCED.monte_carlo) return;
    const ctx = document.getElementById("mcChart").getContext("2d");
    const mc = appData.ADVANCED.monte_carlo;

    if (mcChart) mcChart.destroy();

    const colors = [
        "#38bdf8", "#a855f7", "#34d399", "#fb923c", "#f87171",
        "#facc15", "#818cf8", "#38bdf8", "#f43f5e", "#10b981"
    ];

    const datasets = mc.paths.map((path, idx) => ({
        label: `Simulation Path #${idx + 1}`,
        data: path,
        borderColor: colors[idx % colors.length],
        borderWidth: 1.5,
        pointRadius: 0,
        fill: false
    }));

    mcChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: mc.days,
            datasets: datasets
        },
        options: getChartOptions("60-Day Monte Carlo Price Trajectories ($100 Base)", "Trading Days", "Simulated Index Value ($)")
    });
}

// Render Multi-Model Distribution Fit Table
function renderModelsTable() {
    if (!appData || !appData.ADVANCED || !appData.ADVANCED.models_fit) return;
    const tbody = document.getElementById("modelsTableBody");
    tbody.innerHTML = "";

    appData.ADVANCED.models_fit.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><b>${row.model}</b></td>
            <td><b class="text-blue">${row.log_likelihood}</b></td>
            <td><b>Rank #${row.rank}</b></td>
            <td><span class="tag ${row.rank === 1 ? 'active' : ''}">${row.verdict}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Render Multi-Asset Comparison Matrix
function renderMatrixTable() {
    if (!appData || !appData.ADVANCED || !appData.ADVANCED.comparison_matrix) return;
    const tbody = document.getElementById("matrixTableBody");
    tbody.innerHTML = "";

    appData.ADVANCED.comparison_matrix.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><b>${row.name}</b></td>
            <td>${row.mean_pct > 0 ? "+" : ""}${row.mean_pct}%</td>
            <td>${row.std_pct}%</td>
            <td class="${row.skewness < 0 ? 'text-orange' : 'text-green'}">${row.skewness}</td>
            <td class="text-red">+${row.kurtosis}</td>
            <td>${row.jb_stat}</td>
            <td><span class="test-badge rejected" style="padding: 2px 8px; font-size:11px;"><i class="fa-solid fa-circle-xmark"></i> ${row.normality}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Render Black Swan Stress Simulator
function renderStressTable() {
    if (!appData || !appData.ADVANCED || !appData.ADVANCED.crises_data) return;
    const tbody = document.getElementById("stressTableBody");
    tbody.innerHTML = "";

    appData.ADVANCED.crises_data.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><b>${row.event}</b><br><small class="text-muted">${row.date}</small></td>
            <td class="text-red"><b>${row.drop_pct}%</b></td>
            <td><b class="text-purple">Z = ${row.z_score}</b></td>
            <td class="text-orange">${row.normal_prob_desc}</td>
            <td><span class="tag warning">${row.empirical_status}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Render Quantile Breakdown Matrix
function renderQuantileTable() {
    if (!appData || !appData.ADVANCED || !appData.ADVANCED.quantile_matrix) return;
    const tbody = document.getElementById("quantileTableBody");
    tbody.innerHTML = "";

    appData.ADVANCED.quantile_matrix.forEach(row => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><b>P${row.percentile} (${row.percentile}th Percentile)</b></td>
            <td>${row.empirical_pct > 0 ? "+" : ""}${row.empirical_pct}%</td>
            <td>${row.normal_pct > 0 ? "+" : ""}${row.normal_pct}%</td>
            <td class="${row.diff_pct < 0 ? 'text-red' : 'text-green'}">${row.diff_pct > 0 ? "+" : ""}${row.diff_pct}%</td>
        `;
        tbody.appendChild(tr);
    });
}

// Main Render Function
function renderDashboard() {
    if (!appData || !appData[currentTicker]) return;

    const data = appData[currentTicker];

    // 1. Update Primary KPI Cards
    document.getElementById("valMean").textContent = (data.mean > 0 ? "+" : "") + (data.mean * 100).toFixed(4) + "%";
    document.getElementById("valMeanAnnual").textContent = `Annualized: ~${(data.mean * 252 * 100).toFixed(2)}% / yr`;

    document.getElementById("valStd").textContent = (data.std * 100).toFixed(4) + "%";
    document.getElementById("valVar").textContent = `Variance: ${data.variance.toFixed(8)}`;

    document.getElementById("valSkew").textContent = data.skewness.toFixed(4);
    const skewStatus = document.getElementById("valSkewStatus");
    if (data.skewness < 0) {
        skewStatus.textContent = "Left-Skewed (Crash Risk)";
        skewStatus.className = "metric-sub negative-text";
    } else {
        skewStatus.textContent = "Right-Skewed (Surge Potential)";
        skewStatus.className = "metric-sub text-green";
    }

    document.getElementById("valKurt").textContent = (data.kurtosis > 0 ? "+" : "") + data.kurtosis.toFixed(4);
    const kurtStatus = document.getElementById("valKurtStatus");
    if (data.kurtosis > 0) {
        kurtStatus.textContent = "Leptokurtic (Fat Tails / Outliers)";
        kurtStatus.className = "metric-sub warning-text";
    } else {
        kurtStatus.textContent = "Platykurtic (Thin Tails)";
        kurtStatus.className = "metric-sub text-blue";
    }

    // 2. Update Value at Risk (VaR) Cards
    if (data.var_metrics) {
        const vm = data.var_metrics;
        document.getElementById("valVaR95Hist").textContent = vm.hist_95.toFixed(2) + "%";
        document.getElementById("valVaR95Norm").textContent = vm.norm_95.toFixed(2) + "%";
        
        document.getElementById("valVaR99Hist").textContent = vm.hist_99.toFixed(2) + "%";
        document.getElementById("valVaR99Norm").textContent = vm.norm_99.toFixed(2) + "%";
        
        const gap = Math.abs(vm.hist_99 - vm.norm_99).toFixed(2);
        document.getElementById("valVaRGap").textContent = `+${gap}% Extra Loss`;
    }

    // 3. Update Inferential Statistics Cards
    if (data.lecture_metrics) {
        const lm = data.lecture_metrics;
        document.getElementById("valSE").textContent = (lm.se_mean * 100).toFixed(4) + "%";
        document.getElementById("valCIMean").textContent = `[${(lm.ci_mean[0]*100 > 0 ? "+" : "")}${(lm.ci_mean[0]*100).toFixed(4)}%, +${(lm.ci_mean[1]*100).toFixed(4)}%]`;
        document.getElementById("valCIVar").textContent = `[${lm.ci_var[0].toFixed(7)}, ${lm.ci_var[1].toFixed(7)}]`;
    }

    document.getElementById("valJB").textContent = data.jb_stat.toLocaleString('en-US', {maximumFractionDigits: 2});

    // 4. Update Tables
    document.getElementById("tblN").textContent = data.n.toLocaleString();
    document.getElementById("tblMean").textContent = (data.mean * 100).toFixed(4) + "%";
    document.getElementById("tblVar").textContent = data.variance.toFixed(8);
    document.getElementById("tblStd").textContent = (data.std * 100).toFixed(4) + "%";
    document.getElementById("tblSkew").textContent = data.skewness.toFixed(4);
    document.getElementById("tblKurt").textContent = (data.kurtosis > 0 ? "+" : "") + data.kurtosis.toFixed(4);
    document.getElementById("tblMinMax").textContent = `${(data.min * 100).toFixed(2)}% / +${(data.max * 100).toFixed(2)}%`;
    document.getElementById("tblMedian").textContent = (data.median > 0 ? "+" : "") + (data.median * 100).toFixed(4) + "%";

    renderQuantileTable();

    // 5. Render Active Chart
    renderChart();
    calculateProbability();
    triggerMathJax();
}

// Chart Renderer
function renderChart() {
    const ctx = document.getElementById("mainChart").getContext("2d");
    const data = appData[currentTicker];

    if (mainChart) {
        mainChart.destroy();
    }

    if (activeTab === "histogram") {
        const datasets = [
            {
                type: "bar",
                label: "Empirical Daily Returns Density",
                data: data.histogram.counts,
                backgroundColor: "rgba(56, 189, 248, 0.5)",
                borderColor: "#38bdf8",
                borderWidth: 1,
                barPercentage: 1.0,
                categoryPercentage: 1.0
            },
            {
                type: "line",
                label: `Fitted Normal N(${(data.mean*100).toFixed(2)}%, ${(data.std*100).toFixed(2)}%)`,
                data: data.histogram.norm_pdf,
                borderColor: "#f87171",
                borderWidth: 2.5,
                borderDash: [5, 5],
                pointRadius: 0,
                fill: false
            }
        ];

        if (data.histogram.t_pdf) {
            datasets.push({
                type: "line",
                label: "Fitted Student-t Density (Heavy-Tail Model Fit)",
                data: data.histogram.t_pdf,
                borderColor: "#34d399",
                borderWidth: 2,
                pointRadius: 0,
                fill: false
            });
        }

        mainChart = new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.histogram.bin_centers,
                datasets: datasets
            },
            options: getChartOptions("Distribution Histogram vs Normal & Student-t Density Fits", "Daily Return (%)", "Probability Density")
        });
    } 
    else if (activeTab === "qqplot") {
        const scatterData = data.qq_plot.theoretical.map((x, i) => ({ x: x, y: data.qq_plot.sample[i] }));
        
        mainChart = new Chart(ctx, {
            type: "scatter",
            data: {
                datasets: [
                    {
                        label: "Sample Quantiles",
                        data: scatterData,
                        backgroundColor: "#38bdf8",
                        borderColor: "#0284c7",
                        pointRadius: 4,
                        pointHoverRadius: 6
                    },
                    {
                        type: "line",
                        label: "Normal Reference Line (y = x)",
                        data: [
                            { x: -3, y: (data.mean*100 - 3*data.std*100) },
                            { x: 3, y: (data.mean*100 + 3*data.std*100) }
                        ],
                        borderColor: "#f87171",
                        borderWidth: 2,
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: getChartOptions("Quantile-Quantile (Q-Q) Plot vs Normal Distribution", "Theoretical Standard Normal Quantiles (Z)", "Sample Return Quantiles (%)")
        });
    }
    else if (activeTab === "timeseries") {
        mainChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.time_series.dates,
                datasets: [
                    {
                        label: "Daily Return (%)",
                        data: data.time_series.returns,
                        borderColor: "rgba(56, 189, 248, 0.8)",
                        borderWidth: 1,
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: getChartOptions(`${currentTicker} Daily Returns Time Series`, "Date", "Daily Return (%)")
        });
    }
    else if (activeTab === "cdf") {
        mainChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.cdf.x,
                datasets: [
                    {
                        label: "Empirical CDF",
                        data: data.cdf.empirical,
                        borderColor: "#38bdf8",
                        borderWidth: 2.5,
                        pointRadius: 0,
                        fill: false
                    },
                    {
                        label: "Theoretical Normal CDF",
                        data: data.cdf.normal,
                        borderColor: "#f87171",
                        borderWidth: 2,
                        borderDash: [4, 4],
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: getChartOptions("Empirical CDF vs Normal CDF", "Daily Return (%)", "Cumulative Probability F(x)")
        });
    }
}

// Chart Options Helper
function getChartOptions(titleText, xLabel, yLabel) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 500 },
        plugins: {
            title: {
                display: true,
                text: titleText,
                color: "#f9fafb",
                font: { size: 16, weight: "bold", family: "Inter" }
            },
            legend: {
                labels: { color: "#9ca3af", font: { family: "Inter" } }
            },
            tooltip: {
                backgroundColor: "rgba(17, 24, 39, 0.9)",
                titleFont: { family: "Inter" },
                bodyFont: { family: "Fira Code" },
                borderColor: "rgba(255, 255, 255, 0.1)",
                borderWidth: 1
            }
        },
        scales: {
            x: {
                title: { display: true, text: xLabel, color: "#9ca3af" },
                ticks: { color: "#6b7280" },
                grid: { color: "rgba(255, 255, 255, 0.05)" }
            },
            y: {
                title: { display: true, text: yLabel, color: "#9ca3af" },
                ticks: { color: "#6b7280" },
                grid: { color: "rgba(255, 255, 255, 0.05)" }
            }
        }
    };
}

// Interactive Probability Calculator (Exact & Live)
function calculateProbability() {
    if (!appData || !appData[currentTicker]) return;

    const data = appData[currentTicker];
    const thresholdInput = document.getElementById("returnInput").value;
    const threshold = parseFloat(thresholdInput);
    
    if (isNaN(threshold)) return;

    // 1. Normal Probability Calculation via Standard Normal Z-score CDF
    const muPct = data.mean * 100;
    const stdPct = data.std * 100;
    const z = (threshold - muPct) / stdPct;
    const normProb = 0.5 * (1 + erf(z / Math.SQRT2));

    // 2. Exact Empirical Sample Probability P(X <= threshold)
    let empProb = 0;
    if (data.sorted_returns_pct && data.sorted_returns_pct.length > 0) {
        const count = data.sorted_returns_pct.filter(r => r <= threshold).length;
        empProb = count / data.sorted_returns_pct.length;
    } else {
        const cdfX = data.cdf.x;
        const cdfEmp = data.cdf.empirical;
        for (let i = 0; i < cdfX.length; i++) {
            if (cdfX[i] >= threshold) {
                empProb = cdfEmp[i];
                break;
            }
            if (i === cdfX.length - 1) empProb = 1.0;
        }
    }

    // Render results
    document.getElementById("empProbResult").textContent = (empProb * 100).toFixed(2) + "%";
    document.getElementById("normProbResult").textContent = (normProb * 100).toFixed(2) + "%";

    const ratioEl = document.getElementById("underestRatio");
    if (empProb > normProb) {
        const ratio = normProb > 0 ? (empProb / normProb).toFixed(1) : "Inf";
        ratioEl.textContent = `${ratio}x Higher Risk (Normal Model Underestimates Outlier!)`;
        ratioEl.className = "text-gold";
    } else if (normProb > empProb) {
        const ratio = empProb > 0 ? (normProb / empProb).toFixed(1) : "Inf";
        ratioEl.textContent = `${ratio}x Normal Model Overestimates Risk`;
        ratioEl.className = "text-blue";
    } else {
        ratioEl.textContent = "1.0x Perfect Normal Model Match";
        ratioEl.className = "text-green";
    }
}

// ERF Approximation for Normal CDF
function erf(x) {
    const a1 =  0.254829592;
    const a2 = -0.284496736;
    const a3 =  1.421413741;
    const a4 = -1.453152027;
    const a5 =  1.061405429;
    const p  =  0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);

    const t = 1.0 / (1.0 + p * x);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

    return sign * y;
}
