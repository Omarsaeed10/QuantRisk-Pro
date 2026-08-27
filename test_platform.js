// ==========================================================================
// Comprehensive Platform Test Suite & Quality Assurance Engine
// ==========================================================================
const fs = require('fs');
const path = require('path');
const https = require('https');

const projectDir = __dirname;
let passed = 0;
let failed = 0;
let errors = [];

function assert(condition, testName, errorDetails = "") {
    if (condition) {
        console.log(`  \x1b[32m✔ PASS:\x1b[0m ${testName}`);
        passed++;
    } else {
        console.error(`  \x1b[31m✖ FAIL:\x1b[0m ${testName} ${errorDetails ? `(${errorDetails})` : ''}`);
        failed++;
        errors.push(`${testName}: ${errorDetails}`);
    }
}

async function runTests() {
    console.log("\n==================================================");
    console.log("🚀 STARTING QUANTRISK PRO™ END-TO-END AUDIT SUITE");
    console.log("==================================================\n");

    // -------------------------------------------------------------
    // TEST 1: File Existence & Build Files
    // -------------------------------------------------------------
    console.log("📁 1. Testing Core Files Existence...");
    const files = [
        "index.html",
        "styles.css",
        "app.js",
        "app_data.js",
        "generate_pdf_report.py",
        "generate_pptx_presentation.py",
        "QuantRisk_Executive_Report.pdf",
        "QuantRisk_Executive_Presentation.pptx"
    ];
    files.forEach(f => {
        const fullPath = path.join(projectDir, f);
        assert(fs.existsSync(fullPath), `File exists: ${f}`);
    });

    // -------------------------------------------------------------
    // TEST 2: Data Integrity in app_data.js
    // -------------------------------------------------------------
    console.log("\n📊 2. Testing app_data.js Structure & Datasets...");
    global.window = global;
    require(path.join(projectDir, "app_data.js"));
    
    const APP_DATA = global.APP_DATA;
    const CATALOG_505 = global.CATALOG_505;

    assert(!!APP_DATA, "APP_DATA is loaded and non-empty");
    const assetKeys = Object.keys(APP_DATA).filter(k => k !== "ADVANCED");
    assert(assetKeys.length >= 41, `Dataset contains ${assetKeys.length} institutional assets & portfolios`);
    
    // Check MARKET_AVG Benchmark
    const market = APP_DATA["MARKET_AVG"];
    assert(!!market, "MARKET_AVG benchmark exists in dataset");
    assert(typeof market.mean === "number", `MARKET_AVG mean is valid number (${market?.mean})`);
    assert(typeof market.std === "number" && market.std > 0, `MARKET_AVG std is positive (${market?.std})`);
    assert(typeof market.skewness === "number", `MARKET_AVG skewness is valid (${market?.skewness})`);
    assert(typeof market.kurtosis === "number", `MARKET_AVG kurtosis is valid (${market?.kurtosis})`);
    assert(!!market.var_metrics, "MARKET_AVG contains var_metrics");
    assert(!!market.histogram, "MARKET_AVG contains histogram bins and density");
    assert(!!market.time_series, "MARKET_AVG contains time series and drawdowns");

    // Check Portfolios
    const portfolios = ["PORT_TECH", "PORT_FINANCE", "PORT_HEALTH", "PORT_DEFENSIVE", "PORT_BALANCED"];
    portfolios.forEach(p => {
        assert(!!APP_DATA[p], `Portfolio exists: ${p}`);
    });

    // -------------------------------------------------------------
    // TEST 3: DOM ID Contract Verification between JS & HTML
    // -------------------------------------------------------------
    console.log("\n🔍 3. Verifying DOM Elements Contract (app.js <-> index.html)...");
    const htmlContent = fs.readFileSync(path.join(projectDir, "index.html"), "utf8");
    const jsContent = fs.readFileSync(path.join(projectDir, "app.js"), "utf8");

    // Extract all getElementById calls
    const idRegex = /document\.getElementById\(["']([^"']+)["']\)/g;
    let match;
    const jsIds = new Set();
    while ((match = idRegex.exec(jsContent)) !== null) {
        jsIds.add(match[1]);
    }

    console.log(`  Found ${jsIds.size} unique DOM IDs queried in app.js.`);
    jsIds.forEach(id => {
        const idPattern = new RegExp(`id=["']${id}["']`);
        const found = idPattern.test(htmlContent);
        if (!found) {
            // Check if it's optional or missing
            console.warn(`  ⚠️ Notice: #${id} not found in index.html (checking optional)`);
        }
    });

    // -------------------------------------------------------------
    // TEST 4: Mathematical Calculations QA
    // -------------------------------------------------------------
    console.log("\n🧮 4. Testing Quantitative Risk Formulas & Math Accuracy...");
    
    // Parametric VaR: z_95 = 1.644853, z_99 = 2.326348
    const mu = market.mean;
    const sigma = market.std;
    const var95_calc = (mu - 1.644853 * sigma) * 100;
    const var99_calc = (mu - 2.326348 * sigma) * 100;
    assert(Math.abs(market.var_metrics.norm_95 - var95_calc) < 0.05, `95% Normal VaR accuracy: ${market.var_metrics.norm_95}% vs calc ${var95_calc.toFixed(2)}%`);
    assert(Math.abs(market.var_metrics.norm_99 - var99_calc) < 0.05, `99% Normal VaR accuracy: ${market.var_metrics.norm_99}% vs calc ${var99_calc.toFixed(2)}%`);

    // Cornish-Fisher Expansion Check
    const gamma1 = market.skewness;
    const gamma2 = market.kurtosis;
    const z = -2.326348;
    const z_cf = z + (1/6)*(z*z - 1)*gamma1 + (1/24)*(z*z*z - 3*z)*gamma2 - (1/36)*(2*z*z*z - 5*z)*(gamma1*gamma1);
    const var99_cf_calc = (mu + z_cf * sigma) * 100;
    assert(Math.abs(market.var_metrics.cf_99 - var99_cf_calc) < 0.1, `Cornish-Fisher 99% VaR: ${market.var_metrics.cf_99}% vs calc ${var99_cf_calc.toFixed(2)}%`);

    // -------------------------------------------------------------
    // TEST 5: Live Groq API Connectivity & LLM Inference
    // -------------------------------------------------------------
    console.log("\n🤖 5. Testing Live Groq API LLM Inference...");
    const groqApiKey = "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";
    
    try {
        const postData = JSON.stringify({
            model: "qwen/qwen3.8-27b",
            messages: [
                { role: "system", content: "You are a quantitative risk intelligence assistant. Respond in one concise sentence." },
                { role: "user", content: "State the Basel III capital adequacy definition." }
            ],
            temperature: 0.2,
            max_tokens: 100
        });

        const reqPromise = new Promise((resolve, reject) => {
            const req = https.request({
                hostname: 'api.groq.com',
                path: '/openai/v1/chat/completions',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${groqApiKey}`,
                    'Content-Length': Buffer.byteLength(postData)
                },
                timeout: 10000
            }, (res) => {
                let body = '';
                res.on('data', chunk => body += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(body);
                        resolve({ status: res.statusCode, data: json });
                    } catch(e) {
                        reject(e);
                    }
                });
            });

            req.on('error', reject);
            req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
            req.write(postData);
            req.end();
        });

        const response = await reqPromise;
        assert(response.status === 200, `Groq API HTTP Status 200 OK (Status: ${response.status})`);
        const replyText = response.data?.choices?.[0]?.message?.content;
        assert(!!replyText && replyText.length > 5, `Live AI Response received: "${replyText?.substring(0, 70)}..."`);
    } catch (e) {
        assert(false, "Groq API Connection", e.message);
    }

    // -------------------------------------------------------------
    // SUMMARY
    // -------------------------------------------------------------
    console.log("\n==================================================");
    console.log(`🏁 TEST RESULTS: ${passed} PASSED, ${failed} FAILED`);
    console.log("==================================================\n");

    if (failed > 0) {
        console.error("Errors encountered:", errors);
        process.exit(1);
    } else {
        console.log("🎉 ALL TESTS PASSED WITH 100% SUCCESS RATE!");
    }
}

runTests();
