const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * Instagram Scraper Module
 * Focado em Reels, Posts e Carrosséis para o Viral ETL.
 * Usa sessão autenticada se disponível.
 */
class InstagramScraper {
    constructor(options = {}) {
        this.options = {
            headless: true,
            ...options
        };
        this.sessionPath = path.resolve(__dirname, '..', 'auth', 'instagram_session.json');
    }

    async init() {
        let contextOptions = {
            userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        };

        // Load authenticated session if available
        if (fs.existsSync(this.sessionPath)) {
            console.log(`[InstagramScraper] Loading authenticated session from ${this.sessionPath}`);
            contextOptions.storageState = this.sessionPath;
        }

        this.browser = await chromium.launch({ headless: this.options.headless });
        this.context = await this.browser.newContext(contextOptions);
    }

    async extract(url, downloadDir = null) {
        const page = await this.context.newPage();
        console.log(`[InstagramScraper] Extracting: ${url}`);

        try {
            await page.goto(url, { waitUntil: 'networkidle' });
            await page.waitForTimeout(3000); 

            // Expanding caption and dismissing modals
            try {
                // Initial wait for any dynamic modals to settle
                await page.waitForTimeout(3000);
                await page.keyboard.press('Escape');

                // Absolute Isolation: Clone and Replace Body
                await page.evaluate(() => {
                    const article = document.querySelector('article') || document.querySelector('div[role="main"]');
                    if (!article) return;

                    // 1. Clone the content we want
                    const clone = article.cloneNode(true);
                    
                    // 2. Clear the entire document
                    document.body.innerHTML = '';
                    document.head.innerHTML = '<style>body { background: white !important; margin: 0; padding: 20px; display: flex; justify-content: center; }</style>';
                    
                    // 3. Re-insert ONLY the clone
                    document.body.appendChild(clone);

                    // 4. Force reset styles on the clone
                    clone.style.setProperty('filter', 'none', 'important');
                    clone.style.setProperty('opacity', '1', 'important');
                    clone.style.setProperty('background', 'none', 'important');
                    clone.style.setProperty('position', 'relative', 'important');
                    clone.style.setProperty('display', 'block', 'important');
                    clone.style.setProperty('visibility', 'visible', 'important');
                    
                    // Force white background everywhere
                    document.documentElement.style.setProperty('background-color', '#ffffff', 'important');
                    document.body.style.setProperty('background-color', '#ffffff', 'important');
                });

                // Stabilization Wait (to ensure images/fonts in the clone are ready)
                await page.waitForTimeout(5000);

                // Click "more" if it exists (now that overlays are nuked)
                const moreButton = await page.locator('div[role="button"]:has-text("mais")').or(page.locator('div[role="button"]:has-text("more")'));
                if (await moreButton.count() > 0 && await moreButton.first().isVisible()) {
                    await moreButton.first().click();
                    await page.waitForTimeout(500);
                }
            } catch (e) {}

            // Deep extraction of metadata via DOM
            const data = await page.evaluate(() => {
                const getMeta = (name) => document.querySelector(`meta[property="${name}"]`)?.content;
                
                // Robust caption extraction: find the post description
                // Usually it's a span inside an article, but we want to avoid the "Liked by" spans
                const allSpans = Array.from(document.querySelectorAll('article span[class*="x193iq5w"], div[class*="_a9zs"] span'));
                const captionSpan = allSpans.find(s => s.innerText.length > 20 && !s.innerText.includes('and others') && !s.innerText.includes('e outras pessoas'));
                
                const captionText = captionSpan ? captionSpan.innerText : (getMeta('og:description') || getMeta('description'));

                return {
                    title: document.title,
                    description: captionText,
                    imageUrl: getMeta('og:image'),
                    videoUrl: getMeta('og:video'),
                    type: window.location.href.includes('/reel/') ? 'video' : 'post',
                    author: document.querySelector('header a, span[class*="x1lliihq"] a')?.innerText || 'Unknown'
                };
            });

            // High-resolution harvesting via screenshot
            let localImagePath = null;
            if (downloadDir) {
                const imgPath = path.join(downloadDir, `ig_post_${Date.now()}.jpg`);
                console.log(`[InstagramScraper] Capturing high-res screenshot to: ${imgPath}`);
                
                try {
                    // Force a wider viewport to capture side-by-side layout properly
                    await page.setViewportSize({ width: 1280, height: 1000 });
                    
                    // Try to find the main post container
                    const postElement = await page.locator('article').first();
                    if (await postElement.isVisible()) {
                        await postElement.screenshot({ path: imgPath, quality: 90, type: 'jpeg' });
                    } else {
                        await page.screenshot({ path: imgPath, fullPage: false, quality: 90, type: 'jpeg' });
                    }
                    localImagePath = imgPath;
                } catch (ssErr) {
                    console.error(`[InstagramScraper] Screenshot failed:`, ssErr.message);
                }
            }

            // Lógica para detectar se é carrossel (múltiplas imagens)
            const isCarousel = await page.evaluate(() => document.querySelectorAll('ul li img').length > 1);
            if (isCarousel) data.type = 'carousel';

            return {
                url,
                ...data,
                images: localImagePath ? [localImagePath] : [],
                timestamp: new Date().toISOString(),
                status: localImagePath ? 'success' : 'metadata_only'
            };

        } catch (error) {
            console.error(`[InstagramScraper] Error extracting ${url}:`, error.message);
            return { url, error: error.message, status: 'error' };
        } finally {
            await page.close();
        }
    }

    async close() {
        if (this.browser) await this.browser.close();
    }
}

module.exports = InstagramScraper;
