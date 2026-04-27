const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function debugSession() {
    const authPath = path.resolve(__dirname, '..', 'auth', 'instagram_session.json');
    const debugDir = path.resolve(__dirname, '..', '..', 'outputs', 'debug_session');
    if (!fs.existsSync(debugDir)) fs.mkdirSync(debugDir, { recursive: true });

    console.log(`🔍 Verificando sessão em: ${authPath}`);
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
        storageState: fs.existsSync(authPath) ? authPath : undefined,
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    });

    const page = await context.newPage();
    await page.goto('https://www.instagram.com/');
    await page.waitForTimeout(5000);

    const screenshotPath = path.join(debugDir, `session_check_${Date.now()}.png`);
    await page.screenshot({ path: screenshotPath });
    
    const isLoggedIn = await page.evaluate(() => {
        return !!document.querySelector('svg[aria-label="Home"], svg[aria-label="Página inicial"]');
    });

    console.log(`📸 Screenshot de verificação salvo em: ${screenshotPath}`);
    console.log(`👤 Estado detectado: ${isLoggedIn ? 'LOGADO' : 'DESLOGADO'}`);

    await browser.close();
}

debugSession();
