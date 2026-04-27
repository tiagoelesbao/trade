const fs = require('fs');
const path = require('path');
const InstagramScraper = require('./scrapers/instagram');
const TikTokScraper = require('./scrapers/tiktok');
const YouTubeScraper = require('./scrapers/youtube');
const LinkedInScraper = require('./scrapers/linkedin');

/**
 * Extract Runner: Viral ETL
 * Lê arquivos de links e orquestra os scrapers multicanal.
 */
async function run() {
    const linksFile = path.join(__dirname, 'Links', 'links-23.03.26.md');
    
    if (!fs.existsSync(linksFile)) {
        console.error(`[ExtractRunner] Error: File not found ${linksFile}`);
        return;
    }

    const content = fs.readFileSync(linksFile, 'utf8');
    
    // Regex para capturar links por plataforma
    const links = {
        instagram: content.match(/https:\/\/www\.instagram\.com\/(p|reel)\/[a-zA-Z0-9_-]+\//g) || [],
        tiktok: content.match(/https:\/\/www\.tiktok\.com\/@[a-zA-Z0-9._-]+\/video\/[0-9]+/g) || [],
        youtube: content.match(/https:\/\/www\.youtube\.com\/(watch\?v=|shorts\/)[a-zA-Z0-9_-]+/g) || [],
        linkedin: content.match(/https:\/\/www\.linkedin\.com\/posts\/[a-zA-Z0-9_-]+/g) || []
    };

    console.log(`[ExtractRunner] Found: 
    - IG: ${links.instagram.length} 
    - TT: ${links.tiktok.length} 
    - YT: ${links.youtube.length} 
    - LI: ${links.linkedin.length}`);

    const results = [];

    // Mapeamento de Scrapers
    const scrapers = {
        instagram: new InstagramScraper(),
        tiktok: new TikTokScraper(),
        youtube: new YouTubeScraper(),
        linkedin: new LinkedInScraper()
    };

    // Inicializa todos
    for (const s of Object.values(scrapers)) await s.init();

    // Processamento sequencial por plataforma (amostragem para PoC)
    for (const [platform, urls] of Object.entries(links)) {
        console.log(`[ExtractRunner] Processing ${platform}...`);
        for (const url of urls.slice(0, 2)) { // Limite de 2 links por plataforma para o teste
            try {
                const data = await scrapers[platform].extract(url);
                results.push({ ...data, platform });
            } catch (err) {
                console.error(`[ExtractRunner] Error on ${platform} (${url}):`, err.message);
            }
        }
    }

    // Fecha todos
    for (const s of Object.values(scrapers)) await s.close();

    // Salvar resultados
    const outputPath = path.join(__dirname, '..', '..', '..', '.aiox', 'logs', `extract-results-multichannel-${Date.now()}.json`);
    if (!fs.existsSync(path.dirname(outputPath))) fs.mkdirSync(path.dirname(outputPath), { recursive: true });
    
    fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
    
    console.log(`[ExtractRunner] Finished! Results saved to ${outputPath}`);
}

run();
