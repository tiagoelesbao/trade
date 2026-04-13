"use client"

import { useEffect, useState } from "react"
import { Shield, Brain, TrendingUp, AlertTriangle, CheckCircle2 } from 'lucide-react'
import { supabase } from "@/lib/supabase"

interface AgentComment {
  agent: string
  avatar: string
  comment: string
  sentiment: 'bullish' | 'bearish' | 'neutral'
  confidence: number
}

export function AgentWarRoom() {
  const [latestSignal, setLatestSignal] = useState<any>(null)
  const [analysis, setAnalysis] = useState<AgentComment[]>([])
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  useEffect(() => {
    const handleNewSignal = (signal: any) => {
      setLatestSignal(signal)
      setIsAnalyzing(true)
      
      // Simulação de análise agêntica (Teamwork)
      setTimeout(() => {
        const comments: AgentComment[] = [
          {
            agent: "Jim Simons",
            avatar: "JS",
            comment: `Anatomia quantitativa validada. Pavio de ${(signal.wick_pct * 100).toFixed(1)}% sugere exaustão de Delta.`,
            sentiment: signal.type === 'BUY' ? 'bullish' : 'bearish',
            confidence: 88
          },
          {
            agent: "Druckenmiller",
            avatar: "SD",
            comment: "Estrutura Macro em H1 corrobora a liquidez. O ponto de entrada é ótimo para o risco/retorno.",
            sentiment: signal.type === 'BUY' ? 'bullish' : 'bearish',
            confidence: 92
          },
          {
            agent: "Nassim Taleb",
            avatar: "NT",
            comment: "Risco de cauda controlado pelo SL curto. A convexidade desta entrada é aceitável.",
            sentiment: 'neutral',
            confidence: 75
          }
        ]
        setAnalysis(comments)
        setIsAnalyzing(false)
      }, 2000)
    }

    // Busca o último sinal ao carregar
    const fetchLast = async () => {
       const { data } = await supabase.from('signals_liquidez').select('*').order('created_at', { ascending: false }).limit(1)
       if (data?.[0]) handleNewSignal(data[0])
    }
    fetchLast()

    // Realtime para novos sinais
    const sub = supabase.channel('war-room')
      .on('postgres_changes', { event: 'INSERT', table: 'signals_liquidez' }, (p) => {
        handleNewSignal(p.new)
      })
      .subscribe()

    return () => { supabase.removeChannel(sub) }
  }, [])

  return (
    <div className="flex flex-col gap-6">
      <h3 className="text-white font-medium flex items-center gap-2 border-b border-[#1A1A1A] pb-4">
        <Brain className="h-5 w-5 text-[#0047AB]" />
        SALA DE GUERRA AGÊNTICA (AIA)
      </h3>

      {isAnalyzing ? (
        <div className="flex flex-col items-center justify-center py-12 gap-4">
           <div className="w-12 h-12 border-4 border-[#0047AB] border-t-transparent rounded-full animate-spin"></div>
           <p className="text-sm text-gray-500 animate-pulse">Agentes analisando fluxo de ordens...</p>
        </div>
      ) : latestSignal ? (
        <div className="flex flex-col gap-4">
           {analysis.map((item, idx) => (
             <div key={idx} className="p-4 bg-[#1A1A1A]/30 rounded-xl border border-[#1A1A1A] flex gap-4">
                <div className="w-10 h-10 rounded-full bg-[#0047AB] flex items-center justify-center text-xs font-bold text-white shrink-0 shadow-[0_0_10px_rgba(0,71,171,0.3)]">
                   {item.avatar}
                </div>
                <div className="flex flex-col gap-1">
                   <div className="flex items-center gap-2">
                      <span className="text-sm font-bold text-white">{item.agent}</span>
                      <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                         item.sentiment === 'bullish' ? 'bg-emerald-500/20 text-emerald-500' : 
                         item.sentiment === 'bearish' ? 'bg-red-500/20 text-red-500' : 'bg-gray-500/20 text-gray-500'
                      }`}>
                         {item.sentiment.toUpperCase()}
                      </span>
                      <span className="text-[10px] text-gray-500">{item.confidence}% Confiança</span>
                   </div>
                   <p className="text-xs text-gray-400 leading-relaxed italic">"{item.comment}"</p>
                </div>
             </div>
           ))}

           <div className="mt-4 p-4 rounded-xl bg-[#0047AB]/10 border border-[#0047AB]/30 flex items-center justify-between">
              <div className="flex items-center gap-2">
                 <CheckCircle2 className="h-5 w-5 text-[#0047AB]" />
                 <span className="text-sm font-medium text-white">Consenso: VALIDADO</span>
              </div>
              <button className="px-4 py-1.5 bg-[#0047AB] hover:bg-[#0056D2] text-white text-xs font-bold rounded-lg transition-colors">
                 EXECUTAR AGORA
              </button>
           </div>
        </div>
      ) : (
        <p className="text-sm text-gray-600 italic text-center py-20">Nenhum sinal ativo para análise.</p>
      )}
    </div>
  )
}
