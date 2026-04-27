const BaseEngine = require('./BaseEngine');
const { execSync } = require('child_process');

class YouTubeEngine extends BaseEngine {
    async discover(profileUrl, identifier) {
        const results = [];
        this.logDiagnostic(`   🚀 YouTube: Iniciando Discovery via Metadata Sniper (yt-dlp)...`);

        try {
            // Normalizar URL para garantir que pegamos os vídeos mais recentes
            const targetUrl = profileUrl.includes('/videos') ? profileUrl : profileUrl.replace(/\/$/, '') + '/videos';
            const command = `"${this.parent.binPath}" --flat-playlist --print-json --playlist-items 1-15 ${targetUrl}`;
            
            const output = execSync(command, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
            const lines = output.trim().split('\n');

            for (const line of lines) {
                try {
                    const data = JSON.parse(line);
                    let pubDate = data.timestamp ? new Date(data.timestamp * 1000) : null;
                    
                    if (!pubDate && data.upload_date) {
                        const y = data.upload_date.substring(0, 4);
                        const m = data.upload_date.substring(4, 6);
                        const d = data.upload_date.substring(6, 8);
                        pubDate = new Date(y, parseInt(m) - 1, d);
                    }

                    // DEEP DISCOVERY FALLBACK: Se data ainda for NULA, faz inspeção profunda
                    if (!pubDate) {
                        this.logDiagnostic(`      🔍 YouTube: Data NULA para [${data.id}]. Iniciando Inspeção Profunda...`);
                        try {
                            const deepCmd = `"${this.parent.binPath}" --print upload_date --playlist-items 1 https://www.youtube.com/watch?v=${data.id}`;
                            const deepDateRaw = execSync(deepCmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
                            if (deepDateRaw && deepDateRaw.length === 8) {
                                const y = deepDateRaw.substring(0, 4);
                                const m = deepDateRaw.substring(4, 6);
                                const d = deepDateRaw.substring(6, 8);
                                pubDate = new Date(y, parseInt(m) - 1, d);
                            }
                        } catch (e) {
                            this.logDiagnostic(`         ❌ Falha na inspeção profunda: ${e.message}`);
                        }
                    }

                    const isNew = this.isWithinWindow(pubDate);
                    const dateLog = pubDate ? pubDate.toISOString().split('T')[0] : 'NULA';
                    this.logDiagnostic(`      📄 Vídeo [${data.id}]: Data="${dateLog}" -> (${isNew ? 'NOVO' : 'ANTIGO'})`);

                    if (isNew) {
                        const metrics = {
                            likes: data.like_count || 0,
                            comments: data.comment_count || 0,
                            views: data.view_count || 0
                        };
                        const score = this.calculateScore(metrics);
                        results.push({
                            url: `https://www.youtube.com/watch?v=${data.id}`,
                            platform: 'youtube',
                            identifier,
                            metrics,
                            score,
                            pubDate,
                            title: data.title
                        });
                    }
                } catch (e) {
                    this.logDiagnostic(`      ❌ YouTube: Erro ao processar linha de metadados: ${e.message}`);
                }
            }
        } catch (e) {
            this.logDiagnostic(`   ❌ YouTube ERRO no Discovery: ${e.message}`);
        }

        this.logDiagnostic(`   ✨ YouTube: ${results.length} vídeos qualificados via Metadata Sniper.`);
        return results;
    }
}

module.exports = YouTubeEngine;
