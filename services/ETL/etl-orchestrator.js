require('dotenv').config();
const Downloader = require('./Extract/downloader');
const VideoProcessor = require('./Transform/processors/video-processor');
const AgentHandoff = require('./Load/handoff/agent-context');
const fs = require('fs');
const path = require('path');

/**
 * Viral ETL: Full Pipeline Orchestrator (AIOX Integrated)
 */
async function orchestrate(url) {
    console.log(`\n🚀 Starting ETL (AIOX Mode) for: ${url}`);
    
    const downloader = new Downloader();
    const processor = new VideoProcessor();
    const handoff = new AgentHandoff();
    
    let videoPath, audioPath, screenshots;

    try {
        // 1. Extract: Download
        videoPath = await downloader.download(url);
        
        // 2. Transform: Audio/Frames extraction
        audioPath = await processor.extractAudio(videoPath);
        screenshots = await processor.extractScreenshots(videoPath, 5); // 1 frame every 5s

        // 3. Handoff: Create Agent-readable dossier
        const platform = url.includes('instagram') ? 'instagram' : 
                         url.includes('tiktok') ? 'tiktok' : 
                         url.includes('youtube') ? 'youtube' : 'linkedin';

        const dossierPath = await handoff.createDossier({
            url,
            platform,
            videoPath,
            audioPath,
            framesPath: path.dirname(screenshots[0]),
            framesCount: screenshots.length,
            metadata: {
                timestamp: new Date().toISOString()
            }
        });

        console.log(`\n✅ ETL COMPLETO: Ativos prontos para @virals-marketing-mrbeast-mk`);
        console.log(`💡 Para analisar, chame: *analyze-benchmark ${path.basename(dossierPath)}`);

        return { url, dossier: dossierPath, status: 'completed' };

    } catch (error) {
        console.error(`❌ ETL Failed for ${url}:`, error.message);
        return { url, error: error.message, status: 'error' };
    } finally {
        if (videoPath) downloader.cleanup(videoPath);
        processor.cleanup();
    }
}

async function main() {
    const link = "https://www.instagram.com/reel/DV14eBxESQG/";
    await orchestrate(link);
}

if (require.main === module) {
    main();
}

module.exports = { orchestrate };
