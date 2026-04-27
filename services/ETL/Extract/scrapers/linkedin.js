const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

/**
 * LinkedIn Scraper Module with Authenticated Session
 * Uses stored session cookies to access posts that require login.
 */
class LinkedInScraper {
    constructor(options = {}) {
        this.options = { headless: true, ...options };
        this.sessionPath = path.resolve(__dirname, '..', 'auth', 'linkedin_session.json');
    }

    async init() {
        this.browser = await chromium.launch({
            headless: this.options.headless,
            args: ['--disable-blink-features=AutomationControlled']
        });

        // Load session if available
        if (fs.existsSync(this.sessionPath)) {
            console.log(`[LinkedInScraper] Loading authenticated session...`);
            const sessionData = JSON.parse(fs.readFileSync(this.sessionPath, 'utf8'));
            this.context = await this.browser.newContext({
                userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                cookies: sessionData.cookies || [],
                storageState: this.sessionPath
            });
        } else {
            console.log(`[LinkedInScraper] No session found, using unauthenticated mode.`);
            this.context = await this.browser.newContext({
                userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
            });
        }
    }

    async extract(url) {
        const page = await this.context.newPage();
        console.log(`[LinkedInScraper] Extracting: ${url}`);

        try {
            // Navigate with longer timeout for authenticated content
            await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

            // Wait for feed content to load
            await page.waitForTimeout(5000);

            // Try to expand "see more" button
            try {
                const seeMoreBtn = page.locator('button:has-text("see more"), button:has-text("ver mais"), button[aria-label*="see more"], button[aria-label*="ver mais"]').first();
                if (await seeMoreBtn.isVisible({ timeout: 2000 })) {
                    await seeMoreBtn.click({ force: true });
                    await page.waitForTimeout(1000);
                }
            } catch (_) {}

            // Multi-strategy extraction
            const data = await page.evaluate(() => {
                const getMeta = (name) => {
                    const el = document.querySelector(`meta[property="${name}"]`) || document.querySelector(`meta[name="${name}"]`);
                    return el ? el.content : '';
                };

                // Strategy 1: Extract from the post article
                let postContent = '';
                let author = 'Unknown';
                let likes = null;
                let comments = null;

                // Try to find the main post content
                const postArticle = document.querySelector('article.feed-shared-update-v2, div.feed-shared-update-v2, div.update-components-text');
                if (postArticle) {
                    // Author name
                    const authorEl = postArticle.querySelector('.update-components-actor__name, .update-components-actor__description, a[data-test-app-aware-link]');
                    if (authorEl) author = authorEl.innerText.trim();

                    // Post text - find the longest text block
                    const textElements = postArticle.querySelectorAll('span, p, div[aria-hidden="false"]');
                    let longestText = '';
                    textElements.forEach(el => {
                        const text = el.innerText.trim();
                        if (text.length > longestText.length && text.length > 20) {
                            longestText = text;
                        }
                    });
                    postContent = longestText;

                    // Engagement numbers
                    const socialBar = document.querySelector('.social-details-social-count, .update-components-social-activity');
                    if (socialBar) {
                        const likesEl = socialBar.querySelector('.social-details-social-count__likes-count, button:has-text("likes")');
                        const commentsEl = socialBar.querySelector('.social-details-social-count__comments-count, button:has-text("comments")');
                        if (likesEl) {
                            const match = likesEl.innerText.match(/([\d,.]+)/);
                            if (match) likes = match[1];
                        }
                        if (commentsEl) {
                            const match = commentsEl.innerText.match(/([\d,.]+)/);
                            if (match) comments = match[1];
                        }
                    }
                }

                // Strategy 2: Fallback to OG tags if post content not found
                if (!postContent || postContent.length < 30) {
                    postContent = getMeta('og:description') || getMeta('description') || '';
                }

                // Strategy 3: Extract from specific LinkedIn selectors
                if (!postContent || postContent.length < 30) {
                    const allSpans = Array.from(document.querySelectorAll('span[aria-hidden="false"]'));
                    const longTexts = allSpans
                        .map(s => s.innerText.trim())
                        .filter(t => t.length > 30 && !t.includes('Sign in') && !t.includes('Join now'))
                        .sort((a, b) => b.length - a.length);
                    if (longTexts.length > 0) postContent = longTexts[0];
                }

                // Image/video
                let mediaUrl = getMeta('og:image');
                const imgEl = document.querySelector('img.feed-shared-image__image, img.update-components-image__image');
                if (imgEl) mediaUrl = imgEl.src;

                // Video
                const videoEl = document.querySelector('video');
                const currentUrl = window.location.href;
                const isVideo = !!videoEl || currentUrl.includes('/video/');

                return {
                    title: document.title.replace(' | LinkedIn', '').trim(),
                    description: postContent,
                    imageUrl: mediaUrl,
                    author: author || 'Unknown',
                    likes: likes,
                    comments: comments,
                    type: isVideo ? 'video' : 'post'
                };
            });

            console.log(`  📝 Content: ${data.description ? data.description.substring(0, 80).replace(/\n/g, ' ') : '(empty)'}...`);
            console.log(`  👤 Author: ${data.author}`);
            console.log(`  ❤️ Likes: ${data.likes || 'N/A'}`);
            console.log(`  💬 Comments: ${data.comments || 'N/A'}`);

            return { url, ...data, platform: 'linkedin', timestamp: new Date().toISOString(), status: data.description ? 'success' : 'metadata_only' };
        } catch (error) {
            console.error(`[LinkedInScraper] Error extracting ${url}:`, error.message);

            // Fallback to metadata even on error
            try {
                const fallbackData = await page.evaluate(() => {
                    const getMeta = (name) => document.querySelector(`meta[property="${name}"]`)?.content || document.querySelector(`meta[name="${name}"]`)?.content;
                    return {
                        title: document.title,
                        description: getMeta('og:description') || getMeta('description'),
                        imageUrl: getMeta('og:image'),
                        author: 'Unknown',
                        type: 'post'
                    };
                });
                return { url, ...fallbackData, platform: 'linkedin', status: 'metadata_only', error: error.message };
            } catch (e) {
                return { url, platform: 'linkedin', error: error.message, status: 'error' };
            }
        } finally {
            await page.close();
        }
    }

    async close() {
        if (this.browser) await this.browser.close();
    }
}

module.exports = LinkedInScraper;
