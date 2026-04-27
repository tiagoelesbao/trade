const { chromium } = require('playwright');

/**
 * YouTube Scraper Module
 * Focado em Vídeos e Shorts para o Viral ETL.
 */
class YouTubeScraper {
    constructor(options = {}) {
        this.options = { headless: true, ...options };
    }

    async init() {
        this.browser = await chromium.launch({ headless: this.options.headless });
        this.context = await this.browser.newContext({
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        });
    }

    async extract(url) {
        const page = await this.context.newPage();
        console.log(`[YouTubeScraper] Extracting: ${url}`);

        try {
            await page.goto(url, { waitUntil: 'networkidle' });
            
            // Aguarda o título do vídeo ou carregamento do shorts
            await page.waitForTimeout(2000); 

            const data = await page.evaluate(() => {
                const getMeta = (name) => document.querySelector(`meta[property="${name}"]`)?.content || document.querySelector(`meta[name="${name}"]`)?.content;
                
                return {
                    title: document.title,
                    description: getMeta('og:description') || getMeta('description'),
                    imageUrl: getMeta('og:image'),
                    author: document.querySelector('#upload-info #channel-name a')?.innerText || 'Unknown',
                    type: window.location.href.includes('/shorts/') ? 'shorts' : 'video'
                };
            });

            return { url, ...data, platform: 'youtube', timestamp: new Date().toISOString() };
        } catch (error) {
            console.error(`[YouTubeScraper] Error extracting ${url}:`, error.message);
            return { url, platform: 'youtube', error: error.message, status: 'error' };
        } finally {
            await page.close();
        }
    }

    async close() {
        if (this.browser) await this.browser.close();
    }
}

module.exports = YouTubeScraper;
