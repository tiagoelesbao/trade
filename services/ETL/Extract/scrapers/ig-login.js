const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function runLogin() {
    const authDir = path.resolve(__dirname, '..', 'auth');
    if (!fs.existsSync(authDir)) fs.mkdirSync(authDir, { recursive: true });
    const statePath = path.join(authDir, 'instagram_session.json');

    console.log('🚀 [Instagram Login] Abrindo navegador para login manual...');
    console.log('👉 AÇÃO: Faça login no Instagram na janela que abrir.');
    console.log('👉 Após logar e ver seu feed, digite qualquer coisa aqui e pressione ENTER.');

    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 900 },
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });
    const page = await context.newPage();

    await page.goto('https://www.instagram.com/', { waitUntil: 'domcontentloaded' });

    console.log('\n⏳ Aguardando login... (você tem 5 minutos)');

    // Aguardar input do usuário enquanto monitora a URL
    const readline = require('readline');
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });

    const urlCheck = setInterval(async () => {
        const url = page.url();
        if (!url.includes('/accounts/login') && !url.includes('/accounts/signup') && url.includes('instagram.com')) {
            console.log('\n🎉 Instagram feed detectado! Login confirmado.');
            clearInterval(urlCheck);
            await saveSession(context, statePath, browser, rl);
        }
    }, 3000);

    rl.question('Pressione ENTER para salvar a sessão agora...\n', async () => {
        clearInterval(urlCheck);
        await saveSession(context, statePath, browser, rl);
    });

    // Timeout de 5 minutos
    setTimeout(async () => {
        clearInterval(urlCheck);
        console.log('\n⏱️ Timeout! Salvando sessão atual...');
        await saveSession(context, statePath, browser, rl);
    }, 300000);
}

async function saveSession(context, statePath, browser, rl) {
    try {
        await context.storageState({ path: statePath });
        const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
        const cookieCount = state.cookies?.length || 0;
        console.log(`\n✅ Sessão salva com sucesso em: ${statePath}`);
        console.log(`🍪 Cookies capturados: ${cookieCount}`);
    } catch (e) {
        console.error(`❌ Erro ao salvar sessão: ${e.message}`);
    }
    rl.close();
    await browser.close();
    process.exit(0);
}

runLogin().catch(err => {
    console.error(`❌ Erro fatal: ${err.message}`);
    process.exit(1);
});
