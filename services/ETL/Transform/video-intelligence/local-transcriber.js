const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

/**
 * Local Transcriber: Viral ETL (Hybrid Local Whisper + OpenRouter Vision)
 * 
 * ENHANCED: Audio segmentation for large files (>25MB or >10min)
 * Based on Bot_transcritor segmentation logic
 *
 * PRIORIDADES DEFINIDAS PELO USUÁRIO:
 * 1. Transcrição: Local Whisper (Grátis/Infinito)
 * 2. Visão/Inteligência: Qwen 3.6 Plus (Primário) -> Step 3.5 Flash (Secundário)
 */
class LocalTranscriber {
    constructor() {
        this.openRouterKey = "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";
        this.whisperExe = 'C:\\Users\\Pichau\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\whisper.exe';
        
        // Segmentação thresholds
        this.MAX_FILE_SIZE_MB = 25;     // Whisper local pode travar com arquivos grandes
        this.MAX_DURATION_SEC = 600;    // 10 minutos por segmento (sweet spot para Whisper)
        
        // Modelos de Visão — apenas openrouter/free (único free estável)
        this.visionModels = [
            "openrouter/free"
        ];
    }

    /**
     * Detecta o idioma do áudio usando Whisper tiny SEM flag --language.
     * Whisper detecta automaticamente o idioma quando --language não é fornecido.
     * O arquivo de output contém o idioma detectado no nome: <base>.<lang>.txt
     */
    async detectLanguage(mediaPath) {
        console.log(`[LocalTranscriber] Detectando idioma do áudio...`);
        const whisperExe = 'C:\\Users\\Pichau\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\whisper.exe';
        const baseName = path.basename(mediaPath, path.extname(mediaPath));
        const outputDir = path.dirname(mediaPath);

        // Estratégia 1: Whisper tiny SEM --language → ele detecta sozinho e salva como .<lang>.txt
        try {
            console.log(`[LocalTranscriber] Rodando Whisper tiny para detecção automática...`);
            execSync(`"${whisperExe}" "${mediaPath}" --model tiny --output_dir "${outputDir}" --output_format txt`, {
                stdio: ['pipe', 'pipe', 'pipe'],
                timeout: 120000
            });

            // Whisper cria arquivo: <base>.<detected_lang>.txt
            // Idiomas suportados: en, pt, es, fr, de, it, ja, zh, ko, ru, ar, hi, nl, tr, pl, sv, etc.
            const supportedLangs = [
                'en', 'pt', 'es', 'fr', 'de', 'it', 'ja', 'zh', 'ko', 'ru',
                'ar', 'hi', 'nl', 'tr', 'pl', 'sv', 'da', 'fi', 'no', 'cs',
                'ro', 'el', 'hu', 'th', 'uk', 'vi', 'id', 'ms', 'ca', 'hr'
            ];

            for (const lang of supportedLangs) {
                const langFile = path.join(outputDir, `${baseName}.${lang}.txt`);
                if (fs.existsSync(langFile)) {
                    console.log(`[LocalTranscriber] Idioma detectado pelo Whisper: ${lang}`);
                    // Cleanup imediato
                    try { fs.unlinkSync(langFile); } catch (_) {}
                    return lang;
                }
            }

            // Se chegou aqui, Whisper não criou arquivo .lang.txt — pode ter criado .txt genérico
            // Tenta ler o .txt genérico e analisar por heurística
            const genericFile = path.join(outputDir, `${baseName}.txt`);
            if (fs.existsSync(genericFile)) {
                const content = fs.readFileSync(genericFile, 'utf8');
                const detected = this.heuristicLanguageDetect(content);
                try { fs.unlinkSync(genericFile); } catch (_) {}
                console.log(`[LocalTranscriber] Idioma detectado por heurística: ${detected}`);
                return detected;
            }
        } catch (e) {
            console.warn(`[LocalTranscriber] Whisper tiny falhou na detecção: ${e.message}`);
        }

        // Estratégia 2: Fallback heurístico com transcrição forçada
        // Se Whisper não detectou, tenta transcrever sem flag e analisa o resultado
        console.log(`[LocalTranscriber] Fallback: transcrição sem flag de idioma...`);
        try {
            const tempFile = path.join(outputDir, `${baseName}_langtemp.txt`);
            execSync(`"${whisperExe}" "${mediaPath}" --model tiny --output_dir "${outputDir}" --output_format txt --task transcribe`, {
                stdio: ['pipe', 'pipe', 'pipe'],
                timeout: 120000
            });

            // Verifica se criou arquivo com idioma detectado
            const supportedLangs = ['en', 'pt', 'es', 'fr', 'de', 'it', 'ja', 'zh', 'ko', 'ru'];
            for (const lang of supportedLangs) {
                const langFile = path.join(outputDir, `${baseName}.${lang}.txt`);
                if (fs.existsSync(langFile)) {
                    console.log(`[LocalTranscriber] Idioma detectado no fallback: ${lang}`);
                    try { fs.unlinkSync(langFile); } catch (_) {}
                    try { fs.unlinkSync(tempFile); } catch (_) {}
                    return lang;
                }
            }

            // Lê o arquivo genérico e usa heurística
            if (fs.existsSync(tempFile)) {
                const content = fs.readFileSync(tempFile, 'utf8');
                const detected = this.heuristicLanguageDetect(content);
                try { fs.unlinkSync(tempFile); } catch (_) {}
                console.log(`[LocalTranscriber] Idioma detectado por heurística fallback: ${detected}`);
                return detected;
            }
        } catch (e) {
            console.warn(`[LocalTranscriber] Fallback falhou: ${e.message}`);
        }

        // Estratégia 3: Último recurso — analisa metadados do vídeo
        console.log(`[LocalTranscriber] Último recurso: inferindo por metadados/contexto...`);
        console.warn(`[LocalTranscriber] Não foi possível detectar idioma via Whisper. Padrão: pt (português).`);
        return 'pt'; // Padrão mais seguro para o contexto brasileiro do usuário
    }

    /**
     * Detecção heurística baseada em scoring de palavras-chave por idioma.
     * Usa palavras distintas (não artigos curtos) para evitar falsos positivos.
     */
    heuristicLanguageDetect(text) {
        const lower = text.toLowerCase();
        const words = lower.match(/[a-zà-ú]+/g) || [];

        // Palavras distintivas por idioma — escolho palavras que NÃO existem nos outros idiomas
        const ptDistinctive = [
            'não', 'muito', 'como', 'esse', 'essa', 'isso', 'isto', 'aquilo',
            'você', 'vocês', 'estou', 'está', 'estamos', 'estão', 'estava',
            'fazer', 'faz', 'fiz', 'feito', 'porque', 'quando', 'onde',
            'qual', 'quais', 'quem', 'cada', 'entre', 'sobre', 'após',
            'ainda', 'já', 'mais', 'menos', 'sempre', 'também', 'antes',
            'primeiro', 'depois', 'agora', 'hoje', 'dia', 'noite', 'bom',
            'coisa', 'coisas', 'pessoas', 'gente', 'mundo', 'vida', 'parte',
            'trabalho', 'empresa', 'negócio', 'resultado', 'vendas', 'marketing',
            'para', 'pelo', 'pela', 'pelos', 'pelas', 'num', 'numa', 'nuns',
            'tá', 'tô', 'né', 'então', 'assim', 'será', 'pode', 'posso',
            'temos', 'tem', 'tiver', 'tiveram', 'fosse', 'foram', 'eram',
            'querer', 'quer', 'quero', 'queremos', 'precisa', 'precisar',
            'importante', 'diferente', 'grande', 'pequeno', 'novo', 'velho'
        ];

        const enDistinctive = [
            'the', 'this', 'that', 'these', 'those', 'what', 'when', 'where',
            'which', 'who', 'why', 'how', 'with', 'from', 'into', 'through',
            'about', 'would', 'could', 'should', 'will', 'can', 'must',
            'have', 'has', 'had', 'been', 'being', 'were', 'was', 'are',
            'they', 'their', 'them', 'there', 'here', 'very', 'just', 'only',
            'other', 'another', 'some', 'such', 'than', 'then', 'too', 'also',
            'because', 'before', 'after', 'between', 'during', 'without',
            'people', 'thing', 'things', 'world', 'work', 'way', 'make',
            'made', 'need', 'want', 'know', 'think', 'see', 'look', 'come',
            'take', 'give', 'good', 'great', 'little', 'right', 'new', 'old',
            'really', 'much', 'many', 'most', 'more', 'even', 'back', 'well',
            'still', 'already', 'always', 'never', 'often', 'sometimes',
            'important', 'different', 'business', 'company', 'result', 'sales'
        ];

        const esDistinctive = [
            'pero', 'porque', 'cuando', 'donde', 'puede', 'puedo', 'hacer',
            'mucho', 'muy', 'siempre', 'nunca', 'también', 'ahora', 'hoy',
            'día', 'noche', 'bueno', 'mundo', 'vida', 'parte', 'trabajo',
            'empresa', 'gente', 'personas', 'cosas', 'importante', 'diferente',
            'grande', 'pequeño', 'nuevo', 'viejo', 'para', 'sobre', 'entre',
            'después', 'antes', 'primero', 'este', 'esta', 'eso', 'esto',
            'nada', 'nadie', 'todos', 'todas', 'cada', 'más', 'menos', 'muy'
        ];

        // Scoring: conta ocorrências de palavras distintivas
        let ptScore = 0;
        let enScore = 0;
        let esScore = 0;

        for (const word of words) {
            if (ptDistinctive.includes(word)) ptScore++;
            if (enDistinctive.includes(word)) enScore++;
            if (esDistinctive.includes(word)) esScore++;
        }

        // Log para debug
        console.log(`[LocalTranscriber] Scores heurísticos — PT: ${ptScore}, EN: ${enScore}, ES: ${esScore}`);

        // Se nenhum score > 0, tenta por proporção de caracteres
        if (ptScore === 0 && enScore === 0 && esScore === 0) {
            // Fallback: proporção de caracteres acentuados (português/espanhol usam mais)
            const accented = (text.match(/[àáâãéêíóôõúüçÀÁÂÃÉÊÍÓÔÕÚÜÇ]/g) || []).length;
            const totalLetters = words.length;
            const accentedRatio = totalLetters > 0 ? accented / totalLetters : 0;

            if (accentedRatio > 0.05) return 'pt'; // >5% acentuados = provável PT
            return 'en'; // Baixa acentuação = provável EN
        }

        // Retorna o idioma com maior score
        if (ptScore > enScore && ptScore > esScore) return 'pt';
        if (enScore > ptScore && enScore > esScore) return 'en';
        if (esScore > ptScore && esScore > enScore) return 'es';

        // Empate: PT vs EN — usa acentuação como desempate
        if (ptScore === enScore) {
            const accented = (text.match(/[àáâãéêíóôõúüçÀÁÂÃÉÊÍÓÔÕÚÜÇ]/g) || []).length;
            return accented > 2 ? 'pt' : 'en';
        }

        return 'pt'; // Fallback seguro
    }

    /**
     * Get audio duration in seconds using ffprobe
     * @param {string} audioPath 
     * @returns {number|null} Duration in seconds
     */
    getAudioDuration(audioPath) {
        try {
            const cmd = `ffprobe -v quiet -print_format json -show_format "${audioPath}"`;
            const output = execSync(cmd, { stdio: 'pipe', timeout: 10000 }).toString();
            const data = JSON.parse(output);
            return parseFloat(data.format.duration);
        } catch (e) {
            console.warn(`[LocalTranscriber] Duration check failed: ${e.message}`);
            return null;
        }
    }

    /**
     * Get file size in MB
     * @param {string} filePath 
     * @returns {number} Size in MB
     */
    getFileSizeMB(filePath) {
        try {
            return fs.statSync(filePath).size / (1024 * 1024);
        } catch (_) {
            return 0;
        }
    }

    /**
     * Split audio into segments using FFmpeg
     * @param {string} audioPath 
     * @param {string} outputDir 
     * @param {number} segmentDuration - Duration in seconds (default: 600 = 10min)
     * @returns {string[]} Array of segment paths
     */
    splitAudio(audioPath, outputDir, segmentDuration = 600) {
        try {
            const segmentsDir = path.join(outputDir, 'segments');
            if (!fs.existsSync(segmentsDir)) {
                fs.mkdirSync(segmentsDir, { recursive: true });
            }

            const baseName = path.basename(audioPath, path.extname(audioPath));
            const segmentTemplate = path.join(segmentsDir, `${baseName}_parte_%03d.mp3`);

            const cmd = `ffmpeg -i "${audioPath}" -f segment -segment_time ${segmentDuration} -c:a libmp3lame -q:a 4 -map a -y "${segmentTemplate}"`;
            
            console.log(`[LocalTranscriber] Dividindo áudio em segmentos de ${(segmentDuration/60).toFixed(1)}min...`);
            execSync(cmd, { stdio: 'pipe', timeout: 120000 });

            const segments = fs.readdirSync(segmentsDir)
                .filter(f => f.startsWith(`${baseName}_parte_`) && f.endsWith('.mp3'))
                .map(f => path.join(segmentsDir, f))
                .sort();

            console.log(`[LocalTranscriber] Áudio dividido em ${segments.length} segmentos`);
            return segments;
        } catch (e) {
            console.error(`[LocalTranscriber] Split failed: ${e.message}`);
            return [];
        }
    }

    /**
     * Combine transcribed segments into final output
     * @param {Array<{text: string, segmentNumber: number}>} transcriptions 
     * @param {string} outputDir 
     * @param {string} baseName 
     * @returns {{fullText: string, segments: Array, outputPath: string}}
     */
    combineTranscriptions(transcriptions, outputDir, baseName) {
        const fullText = [];
        const allSegments = [];

        for (const t of transcriptions) {
            const segNum = t.segmentNumber;
            const header = `\n\n--- SEGMENTO ${segNum} ---\n\n`;
            
            fullText.push((segNum === 1 ? '' : header) + t.text.trim());
        }

        const combinedText = fullText.join('');
        const outputPath = path.join(outputDir, `${baseName}_combined.txt`);
        fs.writeFileSync(outputPath, combinedText, 'utf8');

        console.log(`[LocalTranscriber] Transcrição combinada: ${transcriptions.length} segmentos → ${path.basename(outputPath)}`);
        return { fullText: combinedText, outputPath, segmentsCount: transcriptions.length };
    }

    /**
     * Cleanup segment files
     * @param {string[]} segments 
     */
    cleanupSegments(segments) {
        for (const seg of segments) {
            try {
                if (fs.existsSync(seg)) fs.unlinkSync(seg);
            } catch (_) {}
        }
        
        // Remove segments dir if empty
        if (segments.length > 0) {
            const segmentsDir = path.dirname(segments[0]);
            try {
                if (fs.existsSync(segmentsDir) && fs.readdirSync(segmentsDir).length === 0) {
                    fs.rmdirSync(segmentsDir);
                }
            } catch (_) {}
        }
    }

    async transcribeLocally(mediaPath, detectedLanguage = null) {
        console.log(`[LocalTranscriber] Transcrição Local (Whisper)...`);

        // Se nenhum idioma foi detectado, detecta primeiro
        if (!detectedLanguage) {
            detectedLanguage = await this.detectLanguage(mediaPath);
        }

        // CHECK: Precisa segmentar?
        const fileSizeMB = this.getFileSizeMB(mediaPath);
        const durationSec = this.getAudioDuration(mediaPath);
        const needsSegmentation = fileSizeMB > this.MAX_FILE_SIZE_MB || (durationSec && durationSec > this.MAX_DURATION_SEC * 1.5);

        if (needsSegmentation) {
            console.log(`[LocalTranscriber] Áudio grande detectado: ${fileSizeMB.toFixed(1)}MB, ${durationSec ? (durationSec/60).toFixed(1) + 'min' : 'unknown duration'}. Usando segmentação.`);
            return await this.transcribeWithSegmentation(mediaPath, detectedLanguage);
        }

        // Transcrição direta (arquivo pequeno)
        return await this.transcribeDirect(mediaPath, detectedLanguage);
    }

    /**
     * Transcribe large audio by splitting into segments
     */
    async transcribeWithSegmentation(mediaPath, detectedLanguage) {
        const outputDir = path.dirname(mediaPath);
        const baseName = path.basename(mediaPath, path.extname(mediaPath));
        
        // Split audio
        const segments = this.splitAudio(mediaPath, outputDir, this.MAX_DURATION_SEC);
        if (segments.length === 0) {
            console.warn(`[LocalTranscriber] Falha ao segmentar. Tentando transcrição direta...`);
            return await this.transcribeDirect(mediaPath, detectedLanguage);
        }

        // Transcribe each segment
        const transcriptions = [];
        for (let i = 0; i < segments.length; i++) {
            const originalSegment = segments[i];
            const segNum = i + 1;
            
            // Renomear para nome simples (evita problemas com espaços no Windows)
            const simpleName = `segment_${String(segNum).padStart(3, '0')}.mp3`;
            const simplePath = path.join(outputDir, 'segments', simpleName);
            
            try {
                fs.copyFileSync(originalSegment, simplePath);
            } catch (e) {
                console.warn(`[LocalTranscriber] Falha ao copiar segmento ${segNum}: ${e.message}`);
                continue;
            }
            
            console.log(`[LocalTranscriber] Transcrevendo segmento ${segNum}/${segments.length}...`);
            const text = await this.transcribeDirect(simplePath, detectedLanguage);
            
            // Cleanup copied file
            try { fs.unlinkSync(simplePath); } catch (_) {}
            
            if (text && text.length > 10) {
                transcriptions.push({ text, segmentNumber: segNum });
                console.log(`[LocalTranscriber] Segmento ${segNum}: ${text.length} caracteres`);
            } else {
                console.warn(`[LocalTranscriber] Segmento ${segNum} falhou ou vazio.`);
            }
        }

        // Cleanup segment audio files
        this.cleanupSegments(segments);

        // Combine transcriptions
        if (transcriptions.length > 0) {
            const combined = this.combineTranscriptions(transcriptions, outputDir, baseName);
            console.log(`[LocalTranscriber] Transcrição segmentada concluída: ${combined.segmentsCount} segmentos, ${combined.fullText.length} chars`);
            return combined.fullText;
        }

        console.error(`[LocalTranscriber] Todos os segmentos falharam.`);
        return null;
    }

    /**
     * Direct transcription of a single audio file
     */
    async transcribeDirect(mediaPath, detectedLanguage) {
        const baseName = path.basename(mediaPath, path.extname(mediaPath));
        const outputDir = path.dirname(mediaPath);
        const expectedTxt = path.join(outputDir, `${baseName}.txt`);
        const expectedTxtLang = path.join(outputDir, `${baseName}.${detectedLanguage}.txt`);

        // Clean previous outputs
        try { if (fs.existsSync(expectedTxt)) fs.unlinkSync(expectedTxt); } catch (_) {}
        try { if (fs.existsSync(expectedTxtLang)) fs.unlinkSync(expectedTxtLang); } catch (_) {}

        try {
            // Usar aspas duplas e escape para caminhos com espaços
            const cmd = `"${this.whisperExe}" "${mediaPath}" --model base --language ${detectedLanguage} --output_dir "${outputDir}" --output_format txt`;
            execSync(cmd, {
                stdio: 'pipe',
                timeout: 600000,
                maxBuffer: 50 * 1024 * 1024 // 50MB buffer
            });

            // Find output file
            if (fs.existsSync(expectedTxtLang)) {
                const content = fs.readFileSync(expectedTxtLang, 'utf8').trim();
                try { fs.unlinkSync(expectedTxtLang); } catch (_) {}
                return content;
            }
            if (fs.existsSync(expectedTxt)) {
                const content = fs.readFileSync(expectedTxt, 'utf8').trim();
                try { fs.unlinkSync(expectedTxt); } catch (_) {}
                return content;
            }
        } catch (e) {
            console.warn(`[LocalTranscriber] Whisper base falhou: ${e.message.substring(0, 150)}`);
        }

        // Fallback: tiny model
        try {
            const cmd = `"${this.whisperExe}" "${mediaPath}" --model tiny --language ${detectedLanguage} --output_dir "${outputDir}" --output_format txt`;
            execSync(cmd, {
                stdio: 'pipe',
                timeout: 600000,
                maxBuffer: 50 * 1024 * 1024
            });

            if (fs.existsSync(expectedTxtLang)) {
                const content = fs.readFileSync(expectedTxtLang, 'utf8').trim();
                try { fs.unlinkSync(expectedTxtLang); } catch (_) {}
                return content;
            }
            if (fs.existsSync(expectedTxt)) {
                const content = fs.readFileSync(expectedTxt, 'utf8').trim();
                try { fs.unlinkSync(expectedTxt); } catch (_) {}
                return content;
            }
        } catch (e2) {
            console.warn(`[LocalTranscriber] Whisper tiny também falhou: ${e2.message.substring(0, 150)}`);
        }

        return null;
    }

    async analyze(mediaPath, mediaType = 'audio') {
        const isImage = mediaType === 'image';
        console.log(`[LocalTranscriber] Analisando ${isImage ? 'Visual' : 'Áudio'}...`);

        if (!fs.existsSync(mediaPath)) return `_Arquivo ausente._`;

        // LÓGICA DE ÁUDIO (Local Whisper)
        if (!isImage) {
            const localText = await this.transcribeLocally(mediaPath);
            if (localText) return localText;
            
            // Fallback para Visão se Áudio falhar totalmente
            console.log(`[LocalTranscriber] Áudio falhou. Recorrendo à análise visual de frames via OpenRouter...`);
            const screenshotsDir = path.join(path.dirname(mediaPath), 'Screenshots');
            if (fs.existsSync(screenshotsDir)) {
                const files = fs.readdirSync(screenshotsDir).filter(f => f.endsWith('.jpg')).sort();
                if (files.length > 0) return await this.analyze(path.join(screenshotsDir, files[0]), 'image');
            }
            return `_Erro: Falha na transcrição e no fallback visual._`;
        }

        // LÓGICA VISUAL (OpenRouter Prioritário)
        const base64Data = fs.readFileSync(mediaPath).toString('base64');
        const prompt = "Analise esta imagem de marketing: 1. Transcreva o texto visível. 2. Descreva elementos visuais, cores e mood. 3. Identifique gatilhos de design.";
        
        let lastError = null;

        for (const model of this.visionModels) {
            try {
                console.log(`[LocalTranscriber] OpenRouter Vision: Tentando ${model}...`);
                const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
                    method: "POST",
                    headers: {
                        "Authorization": `Bearer ${this.openRouterKey}`,
                        "HTTP-Referer": "https://github.com/google/gemini-cli",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "model": model,
                        "messages": [{
                            "role": "user",
                            "content": [
                                { "type": "text", "text": prompt },
                                { "type": "image_url", "image_url": { "url": `data:image/jpeg;base64,${base64Data}` } }
                            ]
                        }]
                    })
                });

                const data = await response.json();
                if (response.ok && data.choices && data.choices[0]) {
                    console.log(`[LocalTranscriber] Sucesso visual com ${model}!`);
                    return data.choices[0].message.content.trim();
                }
                lastError = new Error(data.error?.message || response.statusText);
                console.warn(`[LocalTranscriber] Modelo ${model} falhou: ${lastError.message}`);
            } catch (e) {
                lastError = e;
            }
        }

        return `_Erro Final na Visão: ${lastError ? lastError.message : 'Falha total de modelos'}_`;
    }
}

module.exports = LocalTranscriber;
