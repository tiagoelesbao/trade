    async discoverTikTok(profileUrl, identifier) {
        const results = [];
        this.logDiagnostic(`   🚀 TikTok: Iniciando Discovery via Metadata (yt-dlp)...`);
        
        try {
            const ytDlpPath = this.binPath;
            const command = `"${ytDlpPath}" --flat-playlist --print-json --playlist-items 1-10 ${profileUrl}`;
            const output = execSync(command, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] });
            
            const lines = output.trim().split('\n');
            for (const line of lines) {
                try {
                    const data = JSON.parse(line);
                    const pubDate = data.timestamp ? new Date(data.timestamp * 1000) : null;
                    const isNew = this.isWithinWindow(pubDate);
                    
                    this.logDiagnostic(`      📄 Post [${data.id}]: Data="${pubDate ? pubDate.toISOString() : 'NULA'}" -> (${isNew ? 'NOVO' : 'ANTIGO'})`);
                    
                    if (isNew) {
                        const metrics = {
                            likes: data.like_count || 0,
                            comments: data.comment_count || 0,
                            views: data.view_count || 0
                        };
                        const score = this.calculateScore(metrics);
                        results.push({ 
                            url: data.webpage_url || data.url, 
                            platform: 'tiktok', 
                            identifier, 
                            metrics, 
                            score, 
                            pubDate,
                            title: data.title
                        });
                    }
                } catch (e) {
                    this.logDiagnostic(`      ❌ TikTok: Erro ao processar linha de metadados: ${e.message}`);
                }
            }
        } catch (e) {
            this.logDiagnostic(`   ❌ TikTok: Erro no Discovery via yt-dlp: ${e.message}`);
        }
        
        this.logDiagnostic(`   ✨ TikTok: ${results.length} posts qualificados via Metadata.`);
        return results;
    }
