const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const { execSync } = require('child_process');

// Engines Especializadas (v3.2)
const InstagramEngine = require('./engines/InstagramEngine');
const TikTokEngine = require('./engines/TikTokEngine');
const YouTubeEngine = require('./engines/YouTubeEngine');
const LinkedInEngine = require('./engines/LinkedInEngine');

/**
 * Social Discovery Engine (Viral ETL) - v3.2 (Modular Sniper Architecture)
 * Orquestrador Chief da Máquina de Viralidade.
 */
class SocialDiscovery {
    constructor(options = {}) {
        this.options = {
            headless: options.headless !== undefined ? options.headless : true,
            profilesPath: options.profilesPath,
            outputPath: options.outputPath,
            lookbackHours: options.lookbackHours || 36,
            ...options
        };
        this.binPath = path.resolve(__dirname, '..', '..', 'bin', 'yt-dlp.exe');
        this.now = new Date();
        this.lookbackLimit = new Date(this.now.getTime() - (this.options.lookbackHours * 60 * 60 * 1000));
        this.debugDir = path.resolve(__dirname, '..', '..', 'outputs', 'discovery_debug');
        if (!fs.existsSync(this.debugDir)) fs.mkdirSync(this.debugDir, { recursive: true });
        
        this.diagnosticLogPath = path.join(this.debugDir, 'run_log.txt');
        fs.writeFileSync(this.diagnosticLogPath, `--- Sniper Run (v3.2): ${this.now.toLocaleString()} ---\n`);

        this.logDiagnostic(`[Config] Now: ${this.now.toISOString()}`);
        this.logDiagnostic(`[Config] Lookback Limit: ${this.lookbackLimit.toISOString()} (${this.options.lookbackHours}h)`);

        // Instanciar Engines
        this.engines = {
            instagram: new InstagramEngine(this),
            tiktok: new TikTokEngine(this),
            youtube: new YouTubeEngine(this),
            linkedin: new LinkedInEngine(this)
        };
    }

    logDiagnostic(msg) {
        console.log(msg);
        fs.appendFileSync(this.diagnosticLogPath, msg + '\n');
    }

    async init() {
        this.browser = await chromium.launch({ 
            headless: this.options.headless,
            args: [
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        });

        this.context = await this.browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            viewport: { width: 1440, height: 1200 },
            locale: 'pt-BR',
            timezoneId: 'America/Sao_Paulo'
        });

        // Injetar cookies de sessão
        const authFiles = {
            tiktok: 'tiktok_session.json',
            instagram: 'instagram_session.json',
            linkedin: 'linkedin_session.json'
        };

        for (const [plat, file] of Object.entries(authFiles)) {
            const authPath = path.resolve(__dirname, '..', 'auth', file);
            if (fs.existsSync(authPath)) {
                try {
                    const state = JSON.parse(fs.readFileSync(authPath, 'utf8'));
                    if (state.cookies) await this.context.addCookies(state.cookies);
                    this.logDiagnostic(`[Init] Cookies de ${plat} injetados.`);
                } catch(e) { this.logDiagnostic(`[Init] Erro cookies ${plat}: ${e.message}`); }
            }
        }
    }

    async run() {
        const absProfilesPath = path.resolve(process.cwd(), this.options.profilesPath);
        const absOutputPath = path.resolve(process.cwd(), this.options.outputPath);
        
        this.logDiagnostic(`🚀 [Discovery] Lendo perfis de: ${absProfilesPath}`);
        const profilesData = yaml.load(fs.readFileSync(absProfilesPath, 'utf8'));
        
        const allPosts = [];
        const platforms = Object.keys(profilesData.profiles);

        for (const platform of platforms) {
            const engine = this.engines[platform];
            if (!engine) {
                this.logDiagnostic(`⚠️ [Skip] Engine não encontrada para plataforma: ${platform}`);
                continue;
            }

            const profiles = profilesData.profiles[platform];
            for (const profile of profiles) {
                const identifier = profile.handle || profile.channel_id || profile.url;
                try {
                    const posts = await engine.discover(profile.url, identifier);
                    allPosts.push(...posts);
                } catch (e) {
                    this.logDiagnostic(`❌ [Error] Falha ao processar ${identifier} (${platform}): ${e.message}`);
                }
            }
        }

        // Gerar Relatório Final
        this.generateReport(allPosts, absOutputPath);
        return allPosts;
    }

    generateReport(allPosts, absOutputPath) {
        const sorted = allPosts.sort((a, b) => b.score - a.score);
        const platformsInReport = [...new Set(sorted.map(p => p.platform))];

        let mdReport = `# Daily Viral Ranking - ${this.now.toISOString().split('T')[0]}\n\n`;
        mdReport += `Posts publicados nas últimas ${this.options.lookbackHours}h com score mínimo de 10, ordenados pelo Viral Score.\n\n`;
        mdReport += `> Score = (Views * 0.1) + (Likes * 1) + (Comments * 5)\n\n---\n\n`;

        for (const plat of platformsInReport) {
            const platPosts = sorted.filter(p => p.platform === plat);
            mdReport += `## 🏆 Ranking ${plat.toUpperCase()}\n\n`;
            mdReport += `| Criador | Viral Score | Likes | Comentários | Views | Link |\n`;
            mdReport += `| :--- | :--- | :--- | :--- | :--- | :--- |\n`;

            platPosts.forEach(p => {
                mdReport += `| ${p.identifier} | **${p.score.toLocaleString()}** | ${p.metrics.likes.toLocaleString()} | ${p.metrics.comments.toLocaleString()} | ${p.metrics.views.toLocaleString()} | [Ver Post](${p.url}) |\n`;
            });
            mdReport += `\n`;
        }

        fs.writeFileSync(absOutputPath, mdReport);
        this.logDiagnostic(`\n🏁 [Concluido] Relatório de Ranking salvo em: ${absOutputPath}`);
    }

    async close() {
        if (this.browser) await this.browser.close();
    }
}

module.exports = SocialDiscovery;

if (require.main === module) {
    const profilesPath = process.argv[2];
    const outputPath = process.argv[3];
    const lookbackHours = parseInt(process.argv[4]) || 48;
    
    const discovery = new SocialDiscovery({ 
        profilesPath, 
        outputPath, 
        lookbackHours,
        headless: true 
    });
    (async () => {
        await discovery.init();
        await discovery.run();
        await discovery.close();
    })();
}
