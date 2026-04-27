require('dotenv').config();
const Downloader = require('./Extract/downloader');
const VideoProcessor = require('./Transform/processors/video-processor');
const AgentHandoff = require('./Load/handoff/agent-context');
const GeminiAnalyzer = require('./Transform/video-intelligence/gemini-analyzer');
const fs = require('fs');
const path = require('path');

// Configuração
const OUTPUT_BASE = path.join(__dirname, 'outputs');
const LINKS_FILE = path.join(__dirname, 'Extract', 'Links', 'links-23.03.26.md');

/**
 * Viral ETL Pipeline: Content-by-Content Processing
 */
class ETLPipeline {
    constructor() {
        if (!fs.existsSync(OUTPUT_BASE)) fs.mkdirSync(OUTPUT_BASE, { recursive: true });
        
        // Verifica API Key
        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) throw new Error('GEMINI_API_KEY not found in .env');
        
        this.downloader = new Downloader();
        this.processor = new VideoProcessor();
        this.handoff = new AgentHandoff();
        this.analyzer = new GeminiAnalyzer(apiKey); // Para transcrição e análise preliminar
    }

    /**
     * Sanitiza strings para nomes de pasta seguros.
     */
    sanitizeName(name) {
        return name.replace(/[^a-zA-Z0-9]/g, '-').substring(0, 50);
    }

    /**
     * Processa um único link do início ao fim.
     */
    async processLink(link, index) {
        console.log(`\n🎬 [${index}] PROCESSING: ${link}`);
        
        const folderName = `Conteudo${index}-${Date.now()}`; // Nome temporário até termos o título
        const contentDir = path.join(OUTPUT_BASE, folderName);
        if (!fs.existsSync(contentDir)) fs.mkdirSync(contentDir);

        let videoPath, audioPath, screenshots;

        try {
            // 1. EXTRACTION
            videoPath = await this.downloader.download(link);
            
            // 2. TRANSFORMATION
            audioPath = await this.processor.extractAudio(videoPath);
            screenshots = await this.processor.extractScreenshots(videoPath, 5); // 1 frame/5s

            // 3. INTELLIGENCE (Gemini para Transcrição e Dados Brutos)
            console.log(`🧠 Generating raw intelligence...`);
            const intelligence = await this.analyzer.analyze(audioPath, screenshots);
            
            // Renomeia a pasta com o título real (se disponível) ou hook
            const safeTitle = this.sanitizeName(intelligence.hook || `Content-${index}`);
            const finalFolderName = `Conteudo${index}-${safeTitle}`;
            const finalDir = path.join(OUTPUT_BASE, finalFolderName);
            fs.renameSync(contentDir, finalDir);
            
            // 4. ORGANIZATION (Move Assets)
            // Salva Transcrição
            fs.writeFileSync(path.join(finalDir, 'transcription.txt'), intelligence.transcription || "No transcription available.");
            
            // Salva Dados Brutos (JSON)
            const benchData = {
                id: `bench-${index}`,
                url: link,
                title: safeTitle,
                intelligence: intelligence,
                processed_at: new Date().toISOString()
            };
            fs.writeFileSync(path.join(finalDir, 'bench-data.json'), JSON.stringify(benchData, null, 2));

            // Move Frames
            const framesDir = path.join(finalDir, 'frames');
            if (!fs.existsSync(framesDir)) fs.mkdirSync(framesDir);
            
            for (const shot of screenshots) {
                const dest = path.join(framesDir, path.basename(shot));
                fs.renameSync(shot, dest);
            }

            // 5. AGENT HANDOFF (Dossiê para Análise Profunda)
            const dossierPath = await this.handoff.createDossier({
                url: link,
                platform: 'detected', // TODO: Melhorar detecção
                videoPath: videoPath, // Ainda aponta para o temp se não movermos
                audioPath: audioPath,
                framesPath: framesDir,
                framesCount: screenshots.length,
                metadata: benchData
            });

            console.log(`✅ SUCCESS: ${finalFolderName}`);
            console.log(`📂 Output: ${finalDir}`);
            
            return { status: 'success', dir: finalDir, dossier: dossierPath };

        } catch (error) {
            console.error(`❌ FAILED: ${link}`, error.message);
            // Salva log de erro na pasta (mesmo com nome temporário)
            fs.writeFileSync(path.join(contentDir, 'error.log'), error.stack);
            return { status: 'error', error: error.message };
        } finally {
            // 6. CLEANUP (Deleta vídeo/áudio brutos do temp)
            // Se quisermos manter o áudio na pasta final, teríamos que ter movido antes.
            // Por enquanto, deletamos para economizar espaço conforme solicitado.
            if (videoPath) this.downloader.cleanup(videoPath);
            this.processor.cleanup(); // Limpa pasta temp do processador
        }
    }

    /**
     * Executa o loop sequencial.
     */
    async run() {
        if (!fs.existsSync(LINKS_FILE)) {
            console.error(`Error: Links file not found at ${LINKS_FILE}`);
            return;
        }

        const content = fs.readFileSync(LINKS_FILE, 'utf8');
        const links = content.match(/https?:\/\/[^\s)]+/g) || [];
        
        // Filtra links válidos
        const validLinks = links.filter(l => 
            l.includes('instagram.com/reel') || 
            l.includes('tiktok.com') || 
            l.includes('youtube.com/watch') || 
            l.includes('linkedin.com/posts')
        );

        console.log(`🚀 Starting ETL Pipeline for ${validLinks.length} links...`);

        for (let i = 0; i < validLinks.length; i++) {
            await this.processLink(validLinks[i], i + 1);
            
            // Pausa entre vídeos (segurança)
            if (i < validLinks.length - 1) {
                console.log(`⏳ Cooldown (2s)...`);
                await new Promise(r => setTimeout(r, 2000));
            }
        }

        console.log(`\n🏁 Pipeline Finished!`);
    }
}

// Execução
if (require.main === module) {
    const pipeline = new ETLPipeline();
    pipeline.run();
}

module.exports = ETLPipeline;
