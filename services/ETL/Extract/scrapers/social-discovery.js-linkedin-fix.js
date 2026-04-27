    async discoverLinkedIn(profileUrl, identifier) {
        const page = await this.context.newPage();
        const results = [];
        let postsUrl = profileUrl.replace(/\/$/, '');

        // Estrutura atualizada para LinkedIn 2026
        if (postsUrl.includes('/in/')) postsUrl += '/recent-activity/all/';
        else if (postsUrl.includes('/company/')) postsUrl += '/posts/';

        this.logDiagnostic(`   🔎 LinkedIn: Navegando para ${postsUrl}`);
        try {
            await page.goto(postsUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
            await page.waitForTimeout(8000);

            const currentUrl = page.url();
            if (currentUrl.includes('login') || currentUrl.includes('checkpoint')) {
                this.logDiagnostic(`   ❌ LinkedIn: Bloqueio de login detectado (URL: ${currentUrl}). Cookies expirados.`);
                return [];
            }

            // Scroll progressivo para carregar conteúdo dinâmico
            this.logDiagnostic(`   🔎 LinkedIn: Rolando a página para carregar mais posts...`);
            for (let s = 0; s < 5; s++) {
                await page.mouse.wheel(0, 3000);
                await page.waitForTimeout(3000);
            }

            // Seletores atualizados LinkedIn 2026
            const postSelector = 'div.feed-shared-update-v2, div.occludable-update, div.update-components-actor, div.scaffold-finite-post__content, article.feed-shared-update-v2';
            const count = await page.locator(postSelector).count();
            this.logDiagnostic(`   🔎 LinkedIn: Elementos de post carregados: ${count}`);

            if (count === 0) {
                // Fallback: tentar seletor mais genérico de feed ou atributos customizados
                const fallbackSelector = '[data-urn], article, div[class*="feed-shared-update"], div.update-components-text';
                const fallbackCount = await page.locator(fallbackSelector).count();
                if (fallbackCount === 0) {
                    this.logDiagnostic(`   ⚠️ LinkedIn: Nenhum post encontrado em ${postsUrl}. Verifique cookies ou permissões de visualização.`);
                    return [];
                }
            }

            const candidates = await page.evaluate(() => {
                const selectors = [
                    'div.feed-shared-update-v2',
                    'div.occludable-update',
                    'article[data-urn]',
                    'div[data-id*="urn:li:activity"]',
                    'div.scaffold-finite-post__content'
                ];

                let posts = [];
                for (const sel of selectors) {
                    const found = Array.from(document.querySelectorAll(sel));
                    if (found.length > 0) {
                        posts = found;
                        break;
                    }
                }

                return posts.slice(0, 15).map((p) => {
                    const urn = p.getAttribute('data-urn') || p.getAttribute('data-id');
                    let url = (urn && urn.includes('activity')) ? `https://www.linkedin.com/feed/update/${urn}/` : null;

                    if (!url) {
                        const linkEl = p.querySelector('a[href*="/feed/update/"], a[href*="/activity/"]');
                        url = linkEl?.href || null;
                    }

                    const allSpans = Array.from(p.querySelectorAll('span'));
                    const dateTextRaw = allSpans.find(s => /^(\d+)\s*(h|d|sem|dia|min|s)/.test(s.innerText.toLowerCase().trim()))?.innerText || '';
                    const dateText = dateTextRaw.split('\n')[0].trim();

                    const reactionsEl = p.querySelector('.social-details-social-counts__reactions-count, .social-details-social-counts__social-proof-fallback-number, [class*="reactions-count"]');
                    const commentsEl = p.querySelector('.social-details-social-counts__comments, [class*="comments-count"]');

                    return {
                        url,
                        dateText,
                        likes: reactionsEl?.innerText || '0',
                        comments: commentsEl?.innerText || '0'
                    };
                }).filter(c => !!c.url);
            });

            this.logDiagnostic(`   🔎 LinkedIn: Analisando ${candidates.length} candidatos da atividade...`);

            for (const item of candidates) {
                const pubDate = this.parseLinkedInDate(item.dateText);
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
