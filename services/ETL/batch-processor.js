const fs = require('fs');
const path = require('path');
const { orchestrate } = require('./etl-orchestrator');

/**
 * Viral ETL: Batch Watcher
 * Processa a lista completa de 244 links para gerar dossiês para o MrBeast.
 */
async function runBatch() {
    const linksFile = path.join(__dirname, 'Extract', 'Links', 'links-23.03.26.md');
    
    if (!fs.existsSync(linksFile)) {
        console.error(`[BatchWatcher] Error: File not found ${linksFile}`);
        return;
    }

    const content = fs.readFileSync(linksFile, 'utf8');
    const allLinks = content.match(/https?:\/\/[^\s)]+/g) || [];
    
    // Filtra apenas links de vídeo suportados
    const validLinks = allLinks.filter(l => 
        l.includes('instagram.com/reel') || 
        l.includes('tiktok.com') || 
        l.includes('youtube.com/watch') ||
        l.includes('youtube.com/shorts')
    );

    console.log(`\n🚀 [BatchWatcher] Iniciando processamento de ${validLinks.length} links.`);
    
    const results = {
        total: validLinks.length,
        completed: 0,
        failed: 0,
        errors: []
    };

    // Processamento sequencial para evitar bloqueios de IP e sobrecarga do sistema
    for (let i = 0; i < validLinks.length; i++) {
        const link = validLinks[i];
        console.log(`\n[${i + 1}/${validLinks.length}] Processando: ${link}`);
        
        try {
            const report = await orchestrate(link);
            if (report.status === 'completed') {
                results.completed++;
            } else {
                results.failed++;
                results.errors.push({ link, error: report.error });
            }
        } catch (err) {
            results.failed++;
            results.errors.push({ link, error: err.message });
            console.error(`[BatchWatcher] Erro crítico no link ${link}:`, err.message);
        }

        // Pequeno intervalo entre downloads para ser "gentil" com as redes sociais
        if (i < validLinks.length - 1) {
            const delay = 2000; // 2 segundos
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    // Relatório Final
    const summaryPath = path.join(__dirname, '..', '..', '.aiox', 'logs', `batch-summary-${Date.now()}.json`);
    fs.writeFileSync(summaryPath, JSON.stringify(results, null, 2));

    console.log(`\n✅ [BatchWatcher] FINALIZADO!`);
    console.log(`📊 Total: ${results.total}`);
    console.log(`✨ Completos: ${results.completed}`);
    console.log(`❌ Falhas: ${results.failed}`);
    console.log(`📝 Sumário salvo em: ${summaryPath}`);
}

if (require.main === module) {
    runBatch();
}
