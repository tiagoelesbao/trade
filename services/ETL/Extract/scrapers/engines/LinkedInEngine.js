const BaseEngine = require('./BaseEngine');

class LinkedInEngine extends BaseEngine {
    async discover(profileUrl, identifier) {
        const page = await this.parent.context.newPage();
        const results = [];
        let postsUrl = profileUrl.replace(/\/$/, '');

        if (postsUrl.includes('/in/')) postsUrl += '/recent-activity/all/';
        else if (postsUrl.includes('/company/')) postsUrl += '/posts/';

        this.logDiagnostic(`   🧐 Buscando LINKEDIN: ${identifier}`);
        try {
            await page.goto(postsUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
            await page.waitForTimeout(10000); // Aumentar espera inicial

            let currentUrl = page.url();
            this.logDiagnostic(`      🔗 LinkedIn URL Atual: ${currentUrl}`);

            // DETECTION: "Olá novamente" / Account Chooser (Intermediate login screen)
            const isWelcomeBack = await page.evaluate(() => {
                return document.body.innerText.includes('Olá novamente') || !!document.querySelector('section.profile-card');
            });

            if (isWelcomeBack) {
                this.logDiagnostic(`   🎯 LinkedIn: Tela "Olá novamente" detectada. Tentando clique de entrada automática...`);
                try {
                    // Tentar clicar no card do perfil ou no nome do usuário
                    const profileCard = page.locator('section.profile-card, .profile-card, div[data-test-id="profile-card"], .remembered-account').first();
                    if (await profileCard.isVisible()) {
                        await profileCard.click();
                        this.logDiagnostic(`      ✅ Clique no card de perfil executado.`);
                    } else {
                        // Fallback: clicar no texto do nome se visível
                        await page.click('text="Tiago Nunes"', { timeout: 5000 });
                        this.logDiagnostic(`      ✅ Clique via texto de nome executado.`);
                    }
                    await page.waitForTimeout(10000);
                    currentUrl = page.url();
                    this.logDiagnostic(`      🔗 URL após clique de entrada: ${currentUrl}`);
                } catch (e) {
                    this.logDiagnostic(`      ⚠️ Falha ao clicar no card: ${e.message}`);
                }
            }

            if (currentUrl.includes('login') || currentUrl.includes('checkpoint') || currentUrl.includes('authwall')) {
                this.logDiagnostic(`   ❌ LinkedIn: Bloqueio de Login/Authwall detectado. Tentando bypass via reload...`);
                await page.reload({ waitUntil: 'domcontentloaded' });
                await page.waitForTimeout(10000);
                currentUrl = page.url();
                if (currentUrl.includes('login')) {
                    this.logDiagnostic(`      ❌ Bypass falhou. Cookies podem estar corrompidos ou mal injetados.`);
                    return [];
                }
            }

            // Scroll agressivo e lento para LinkedIn com pausas randômicas
            this.logDiagnostic(`   🔎 LinkedIn: Carregando feed de atividades...`);
            for (let s = 0; s < 5; s++) {
                await page.mouse.wheel(0, 2500);
                await page.waitForTimeout(3000 + (Math.random() * 2000));
            }

            const candidates = await page.evaluate(() => {
                // Seletores ultra-resilientes 2026
                const selectors = [
                    'div.feed-shared-update-v2',
                    'article[data-urn]',
                    'div[data-id*="urn:li:activity"]',
                    '.scaffold-finite-post__content',
                    'div.update-components-actor',
                    '.feed-shared-update-v2__control-menu'
                ];

                let posts = [];
                for (const sel of selectors) {
                    const found = Array.from(document.querySelectorAll(sel));
                    if (found.length > 0) {
                        posts = found;
                        break;
                    }
                }

                // Se não encontrar elementos de post, tenta buscar por blocos de texto grandes
                if (posts.length === 0) {
                    const allDivs = Array.from(document.querySelectorAll('div'));
                    posts = allDivs.filter(d => d.innerText && d.innerText.length > 100 && /curtidas|likes|comentários|comments/i.test(d.innerText)).slice(0, 10);
                }

                return posts.slice(0, 15).map((p) => {
                    const urn = p.getAttribute('data-urn') || p.getAttribute('data-id');
                    let url = (urn && urn.includes('activity')) ? `https://www.linkedin.com/feed/update/${urn}/` : null;

                    if (!url) {
                        const linkEl = p.querySelector('a[href*="/feed/update/"], a[href*="/activity/"]');
                        url = linkEl?.href || null;
                    }

                    const allSpans = Array.from(p.querySelectorAll('span, time'));
                    const dateTextRaw = allSpans.find(s => /^(\d+)\s*(h|d|sem|dia|min|s|w)/.test(s.innerText.toLowerCase().trim()))?.innerText || '';
                    
                    const reactionsEl = p.querySelector('.social-details-social-counts__reactions-count, [class*="reactions-count"], .v-align-middle');
                    const commentsEl = p.querySelector('.social-details-social-counts__comments, [class*="comments-count"]');

                    return {
                        url,
                        dateText: dateTextRaw.split('\n')[0].trim(),
                        likes: reactionsEl?.innerText || '0',
                        comments: commentsEl?.innerText || '0'
                    };
                }).filter(c => !!c.url);
            });

            this.logDiagnostic(`   🔎 LinkedIn: Analisando ${candidates.length} posts da atividade...`);

            for (const item of candidates) {
                const pubDate = this.parseSmartDate(item.dateText);
                const isNew = this.isWithinWindow(pubDate);

                this.logDiagnostic(`      📄 Post [${item.url.split('/').pop()}]: Data="${item.dateText}" -> ${pubDate ? pubDate.toLocaleString() : 'NULA'} (${isNew ? 'NOVO' : 'ANTIGO'})`);

                if (isNew) {
                    const metrics = {
                        likes: this.parseViralMetric(item.likes),
                        comments: this.parseViralMetric(item.comments),
                        views: 0
                    };
                    const score = this.calculateScore(metrics);
                    results.push({ url: item.url, platform: 'linkedin', identifier, metrics, score, pubDate });
                }
            }
        } catch (e) {
            this.logDiagnostic(`   ❌ LinkedIn ERRO: ${e.message}`);
        } finally {
            await page.close();
        }
        return results;
    }
}

module.exports = LinkedInEngine;
