const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * LinkedIn Login Utility - Viral ETL
 * Use this to generate linkedin_session.json manually.
 */
async function runLogin() {
    const authDir = path.resolve(__dirname, '..', 'auth');
    if (!fs.existsSync(authDir)) fs.mkdirSync(authDir, { recursive: true });
    
    const statePath = path.join(authDir, 'linkedin_session.json');

    console.log('\n' + '═'.repeat(60));
    console.log('🚀 [LinkedIn Login] Abrindo navegador para login manual...');
    console.log('👉 AÇÃO REQUERIDA: Faça login no LinkedIn na janela que abrir.');
    console.log('👉 Vá até sua página inicial ou perfil após logar.');
    console.log('👉 O script detectará o login e salvará a sessão automaticamente.');
    console.log('═'.repeat(60) + '\n');

    const browser = await chromium.launch({ headless: false });
    const context = await browser.newContext({
        viewport: { width: 1280, height: 900 }
    });

    const page = await context.newPage();
    await page.goto('https://www.linkedin.com/login');

    try {
        // Aguarda até que a URL não contenha mais 'login' ou 'checkpoint' (2FA) e mostre o feed
        await page.waitForURL((url) => {
            return url.hostname.includes('linkedin.com') && 
                   !url.pathname.includes('/login') && 
                   !url.pathname.includes('/checkpoint');
        }, { timeout: 300000 }); // 5 minutos para login e 2FA

        console.log('\n🎉 Login detector! Aguardando 5 segundos para estabilizar cookies...');
        await page.waitForTimeout(5000);

        await context.storageState({ path: statePath });
        console.log(`\n✅ Sessão salva com sucesso em: ${statePath}`);
        console.log('Você já pode fechar o navegador e voltar para a automação.\n');

    } catch (e) {
        console.log('\n⚠️ Timeout ou erro durante o login. Tentando salvar estado atual mesmo assim.');
        await context.storageState({ path: statePath });
        console.log(`Sessão (parcial?) salva em: ${statePath}`);
    }

    await browser.close();
}

runLogin();
