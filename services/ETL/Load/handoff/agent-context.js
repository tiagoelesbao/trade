const fs = require('fs');
const path = require('path');

/**
 * Agent Handoff: Viral ETL
 * Prepara o dossiê de benchmark para análise de agentes especializados.
 * Configurável — target_agent e workflow_ref podem ser passados via data.
 */
class AgentHandoff {
    constructor(handoffDir = '.aiox/handoffs') {
        this.handoffDir = path.resolve(handoffDir);
        if (!fs.existsSync(this.handoffDir)) fs.mkdirSync(this.handoffDir, { recursive: true });
    }

    /**
     * Gera um arquivo JSON que o AIOS e seus agentes conseguem "ler" como contexto.
     * @param {Object} data - Dados do conteúdo processado
     * @param {string} data.url - URL do conteúdo original
     * @param {string} data.platform - Plataforma detectada
     * @param {string} data.videoPath - Caminho do vídeo
     * @param {string} data.audioPath - Caminho do áudio
     * @param {string} data.framesPath - Caminho da pasta de frames
     * @param {number} data.framesCount - Número de frames capturados
     * @param {string} [data.outputDir] - Caminho da pasta de output do conteúdo
     * @param {string} [data.targetAgent] - Agente alvo (default: workflow orchestrator)
     * @param {Object} [data.metadata] - Metadata adicional
     */
    async createDossier(data) {
        const dossierId = `benchmark_${Date.now()}`;
        const dossierPath = path.join(this.handoffDir, `${dossierId}.json`);
        
        const dossier = {
            id: dossierId,
            origin: 'Viral-ETL-Engine',
            target_agent: data.targetAgent || 'marketing-chief',
            workflow_ref: 'benchmark-creative-analysis.yaml',
            content: {
                url: data.url,
                platform: data.platform,
                assets: {
                    video: data.videoPath,
                    audio: data.audioPath,
                    frames_path: data.framesPath,
                    frames_count: data.framesCount
                },
                output_dir: data.outputDir || null,
                metadata: data.metadata || {}
            },
            status: 'ready_for_analysis',
            consumed: false
        };

        fs.writeFileSync(dossierPath, JSON.stringify(dossier, null, 2));
        
        console.log(`\n📋 DOSSIÊ DE BENCHMARK CRIADO!`);
        console.log(`📍 Local: ${dossierPath}`);
        console.log(`🎯 Workflow: benchmark-creative-analysis.yaml`);
        console.log(`🏗️ Agente Orquestrador: @${dossier.target_agent}`);
        
        return dossierPath;
    }
}

module.exports = AgentHandoff;

