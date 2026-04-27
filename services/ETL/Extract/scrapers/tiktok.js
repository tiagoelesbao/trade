const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * TikTok Scraper Module with Authenticated Session
 * Uses stored session cookies to access restricted content.
 */
class TikTokScraper {
    constructor(options = {}) {
        this.options = { headless: true, ...options };
        this.sessionPath = path.resolve(__dirname, '..', 'auth', 'tiktok_session.json');
    }

    async init() {
        this.browser = await chromium.launch({
            headless: this.options.headless,
            args: ['--disable-blink-features=AutomationControlled']
        });

        // Load session if available
        if (fs.existsSync(this.sessionPath)) {
            console.log(`[TikTokScraper] Loading authenticated session...`);
            const sessionData = JSON.parse(fs.readFileSync(this.sessionPath, 'utf8'));
            this.context = await this.browser.newContext({
                userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                cookies: sessionData.cookies || []
            });
        } else {
            console.log(`[TikTokScraper] No session found, using unauthenticated mode.`);
            this.context = await this.browser.newContext({
                userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            });
        }
    }

    async extract(url) {
        const page = await this.context.newPage();
        console.log(`[TikTokScraper] Extracting: ${url}`);

        try {
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

            // Wait for video content to load
            await page.waitForTimeout(5000);

            // Dismiss any cookie banners
            try {
                const cookieBanner = page.locator('div[id*="cookie"], button:has-text("Accept all"), button:has-text("Accept cookies")').first();
                if (await cookieBanner.isVisible({ timeout: 2000 })) {
                    await cookieBanner.click({ force: true });
                    await page.waitForTimeout(1000);
                }
            } catch (_) {}

            const data = await page.evaluate(() => {
                const getMeta = (name) => document.querySelector(`meta[property="${name}"]`)?.content || document.querySelector(`meta[name="${name}"]`)?.content;

                // Try to get video description from various sources
                let description = getMeta('og:description') || getMeta('description') || '';

                // Try to extract from TikTok's structured data
                const videoEl = document.querySelector('video');
                const isVideoReady = videoEl && videoEl.readyState >= 2;

                // Try to get author from various selectors
                let author = 'Unknown';
                const authorSelectors = [
                    '[data-e2e="browse-user-node"]',
                    'a[href^="/@"]',
                    'h2[data-e2e="user-title"]',
                    'span[data-e2e="user-display-name"]'
                ];
                for (const sel of authorSelectors) {
                    const el = document.querySelector(sel);
                    if (el && el.innerText.trim()) {
                        author = el.innerText.trim();
                        break;
                    }
                }

                // Get engagement stats if visible
                let likes = null;
                let comments = null;
                const likesEl = document.querySelector('[data-e2e="like-count"], strong[data-e2e="like-count"]');
                const commentsEl = document.querySelector('[data-e2e="comment-count"], strong[data-e2e="comment-count"]');
                if (likesEl) likes = likesEl.innerText;
                if (commentsEl) comments = commentsEl.innerText;

                return {
                    title: document.title.replace('| TikTok', '').trim(),
                    description,
                    imageUrl: getMeta('og:image'),
                    videoUrl: getMeta('og:video:url') || getMeta('og:video'),
                    author,
                    likes,
                    comments,
                    type: 'video',
                    videoReady: isVideoReady
                };
            });

            console.log(`  📝 Description: ${data.description ? data.description.substring(0, 80).replace(/\n/g, ' ') : '(empty)'}...`);
            console.log(`  👤 Author: ${data.author}`);

            return { url, ...data, platform: 'tiktok', timestamp: new Date().toISOString(), status: data.description ? 'success' : 'metadata_only' };
        } catch (error) {
            console.error(`[TikTokScraper] Error extracting ${url}:`, error.message);
            return { url, platform: 'tiktok', error: error.message, status: 'error' };
        } finally {
            await page.close();
        }
    }

    async close() {
        if (this.browser) await this.browser.close();
    }
}

module.exports = TikTokScraper;
