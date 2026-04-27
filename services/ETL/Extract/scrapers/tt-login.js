const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

/**
 * TikTok Stealth Login Utility - (Viral ETL) - v1.1.0
 * Finalidade: Permitir o login manual no TikTok sem detecção de bot ('Navegador Inseguro')
 */
async function ttLogin() {
    console.log('🚀 Iniciando TikTok em modo Stealth para Login...');
    
    const browser = await chromium.launch({ 
        headless: false,
        args: [
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox'
        ]
    });

    const context = await browser.newContext({
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        viewport: { width: 1440, height: 1200 },
        locale: 'pt-BR',
        timezoneId: 'America/Sao_Paulo'
    });

    // EVASÃO ADICIONAL (Injeta script para deletar navigator.webdriver)
    await context.addInitScript(() => {
        delete Object.getPrototypeOf(navigator).webdriver;
        window.chrome = { runtime: {} };
    });

    const page = await context.newPage();
    const savePath = path.resolve(__dirname, '..', 'auth', 'tiktok_session.json');

    console.log('\n--- AÇÕES REQUERIDAS ---');
    console.log('1. Realize o login no TikTok na janela que abriu.');
    console.log('2. Resolva os captchas normalmente.');
    console.log('3. Quando estiver logado no perfil correto:');
    console.log('   👉 VOLTE AQUI NO TERMINAL E APERTE [ENTER] PARA SALVAR A SESSÃO.');
    console.log('4. Somente após a confirmação de "Sessão salva", feche o navegador.');
    console.log('------------------------\n');

    await page.goto('https://www.tiktok.com/login', { waitUntil: 'networkidle' });

    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    const waitForEnter = () => new Promise(resolve => rl.question('Pressione [ENTER] para capturar os cookies e salvar a sessão...', () => resolve()));

    await waitForEnter();

    console.log('✅ Capturando cookies...');
    const cookies = await context.cookies();
    const sessionData = {
        cookies: cookies,
        timestamp: new Date().toISOString()
    };
    
    const dir = path.dirname(savePath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    
    fs.writeFileSync(savePath, JSON.stringify(sessionData, null, 2));
    console.log(`✨ SUCESSO: Sessão salva em: ${savePath}`);
    console.log('Agora você pode fechar o navegador e encerrar o script (Ctrl+C).');

    rl.close();
}

ttLogin().catch(err => console.error('❌ Erro no Login Stealth:', err));
