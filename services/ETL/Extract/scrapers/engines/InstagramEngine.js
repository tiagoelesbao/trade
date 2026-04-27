const BaseEngine = require('./BaseEngine');

class InstagramEngine extends BaseEngine {
    async discover(profileUrl, identifier) {
        const page = await this.parent.context.newPage();
        const results = [];
        this.logDiagnostic(`   🧐 Buscando INSTAGRAM: ${identifier}`);

        try {
            await page.goto(profileUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
            await page.waitForTimeout(8000);
            
            // Scroll para carregar grade
            for (let i = 0; i < 3; i++) {
                await page.mouse.wheel(0, 1500);
                await page.waitForTimeout(2000);
            }

            const candidates = await page.evaluate(() => {
                const links = Array.from(document.querySelectorAll('a[href*="/p/"], a[href*="/reel/"]'));
                return [...new Set(links.map(a => a.href))].slice(0, 8);
            });

            this.logDiagnostic(`   🔎 Analisando ${candidates.length} posts do Instagram...`);

            for (const url of candidates) {
                const postPage = await this.parent.context.newPage();
                try {
                    await postPage.goto(url, { waitUntil: 'domcontentloaded', timeout: 40000 });
                    await postPage.waitForTimeout(6000);

                    const meta = await postPage.evaluate(() => {
                        const res = { dt: null, likes: 0, comments: 0, source: 'none' };
                        
                        // 1. ld+json
                        const ldScripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                        for (const script of ldScripts) {
                            try {
                                const data = JSON.parse(script.innerText);
                                if (data.uploadDate) res.dt = data.uploadDate;
                                res.source = 'ld+json';
                            } catch (e) {}
                        }

                        // 2. DOM
                        if (!res.dt) {
                            const timeEl = document.querySelector('time');
                            if (timeEl) res.dt = timeEl.getAttribute('datetime');
                        }

                        const text = document.body.innerText;
                        const likeMatch = text.match(/([\d\.,km]+)\s*(curtidas|likes)/i);
                        if (likeMatch) res.likes = likeMatch[1];

                        const commentMatch = text.match(/([\d\.,km]+)\s*(comentários|comments)/i);
                        if (commentMatch) res.comments = commentMatch[1];

                        return res;
                    });

                    const pubDate = meta.dt ? new Date(meta.dt) : null;
                    const isNew = this.isWithinWindow(pubDate);

                    this.logDiagnostic(`      📄 Post [${url.split('/').pop()}]: Data="${meta.dt}" -> ${pubDate ? pubDate.toLocaleString() : 'NULA'} (${isNew ? 'NOVO' : 'ANTIGO'})`);

                    if (isNew) {
                        const metrics = {
                            likes: this.parseViralMetric(meta.likes),
                            comments: this.parseViralMetric(meta.comments),
                            views: 0
                        };
                        const score = this.calculateScore(metrics);
                        results.push({ url, platform: 'instagram', identifier, metrics, score, pubDate });
                    }
                } catch (e) {
                    this.logDiagnostic(`      ❌ Instagram: Erro no post ${url}: ${e.message}`);
                } finally { await postPage.close(); }
            }
        } catch (e) {
            this.logDiagnostic(`   ❌ Instagram ERRO: ${e.message}`);
        } finally {
            await page.close();
        }
        return results;
    }
}

module.exports = InstagramEngine;
