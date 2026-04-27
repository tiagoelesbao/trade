const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

/**
 * Video Processor: Viral ETL
 * Usa FFmpeg para otimizar análise (extração de áudio e visual strip).
 * 0-cost, local-first.
 */
class VideoProcessor {
    constructor(tempDir = '.aiox/tmp/etl') {
        this.tempDir = path.resolve(tempDir);
        if (!fs.existsSync(this.tempDir)) fs.mkdirSync(this.tempDir, { recursive: true });
    }

    /**
     * Extrai áudio acelerado para transcrição se desejado (sugerido manter 1x para precisão).
     * Otimiza para Gemini que aceita áudio direto.
     */
    async extractAudio(videoPath) {
        const audioPath = path.join(this.tempDir, `${path.basename(videoPath, path.extname(videoPath))}.mp3`);
        console.log(`[VideoProcessor] Extracting audio to ${audioPath}`);
        
        // Extrai áudio em 128k mono para economizar espaço e manter fidelidade
        const cmd = `ffmpeg -i "${videoPath}" -b:a 32k -map a -ar 16000 -ac 1 "${audioPath}" -y`;
        execSync(cmd, { stdio: 'ignore' });
        
        return audioPath;
    }

    /**
     * Tira screenshots em intervalos regulares para contexto visual.
     * Gera uma colagem (filmstrip) para análise de IA de baixo custo.
     */
    async extractScreenshots(videoPath, intervalSeconds = 5) {
        const outputPattern = path.join(this.tempDir, `${path.basename(videoPath, path.extname(videoPath))}_thumb_%03d.jpg`);
        console.log(`[VideoProcessor] Extracting frames every ${intervalSeconds}s`);
        
        const cmd = `ffmpeg -i "${videoPath}" -vf "fps=1/${intervalSeconds},scale=640:-1" "${outputPattern}" -y`;
        execSync(cmd, { stdio: 'ignore' });

        return fs.readdirSync(this.tempDir)
                 .filter(f => f.includes('_thumb_'))
                 .map(f => path.join(this.tempDir, f));
    }

    /**
     * Limpa arquivos temporários.
     */
    cleanup() {
        if (fs.existsSync(this.tempDir)) {
            const files = fs.readdirSync(this.tempDir);
            for (const file of files) fs.unlinkSync(path.join(this.tempDir, file));
        }
    }
}

module.exports = VideoProcessor;
