"use client"

import { useEffect, useState } from "react"
import { Wallet, Activity, Target, Zap } from 'lucide-react'
import { supabase } from "@/lib/supabase"

export function DashboardMetrics() {
  const [metrics, setMetrics] = useState({
    activeZones: 0,
    signals24h: 0,
    avgWick: 0,
    resultDay: 0,
    totalPnl: 0
  })

  const fetchMetrics = async () => {
    // 1. FONTE ÚNICA DE VERDADE: Pega métricas REAIS calculadas pelo robô no Heartbeat
    const { data: heartbeat } = await supabase
      .from('bot_heartbeats')
      .select('active_zones, pnl_today, pnl_total')
      .eq('symbol', 'GLOBAL')
      .order('created_at', { ascending: false })
      .limit(1)
    
    // 2. Estatísticas de Volume (Mantemos apenas para contagem de sinais)
    const { data: signals } = await supabase
      .from('signals_liquidez')
      .select('wick_pct, created_at')

    if (signals) {
      const now = new Date()
      const last24h = now.getTime() - (24 * 60 * 60 * 1000)
      const signals24h = signals.filter(s => new Date(s.created_at).getTime() > last24h).length
      const wicks = signals.filter(s => new Date(s.created_at).getTime() > last24h).map(s => s.wick_pct || 0)
      const avgWick = wicks.length > 0 ? (wicks.reduce((a, b) => a + b, 0) / wicks.length) * 100 : 0
      
      const hb = heartbeat?.[0]
      
      // ATUALIZAÇÃO: Agora usamos o valor que o robô enviou, sem cálculos no JS
      setMetrics({
        activeZones: hb?.active_zones || 0,
        signals24h,
        avgWick,
        resultDay: hb?.pnl_today || 0, 
        totalPnl: hb?.pnl_total || 0   
      })
    }
  }

  useEffect(() => {
    fetchMetrics()
    const channel = supabase.channel('metrics-integrity-v2')
      .on('postgres_changes', { event: '*', table: 'bot_heartbeats' }, () => fetchMetrics())
      .on('postgres_changes', { event: '*', table: 'signals_liquidez' }, () => fetchMetrics())
      .subscribe()
    return () => { supabase.removeChannel(channel) }
  }, [])

  return (
    <div className="flex flex-col xl:flex-row gap-8 xl:items-center justify-between p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2 text-gray-400">
          <Activity className="h-5 w-5 text-[#0047AB]" />
          <span className="text-lg">Zonas M15 Ativas</span>
        </div>
        <div className="text-5xl md:text-4xl lg:text-5xl font-bold text-white">{metrics.activeZones}</div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8 xl:gap-16">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Zap className="h-4 w-4" />
            <span>Sinais (24h)</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-white">{metrics.signals24h}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Target className="h-4 w-4" />
            <span>Pavio Médio %</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-[#0047AB]">{metrics.avgWick.toFixed(1)}%</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <span>P&amp;L Sessão (MT5)</span>
          </div>
          <span className={`text-2xl md:text-xl lg:text-2xl font-semibold ${metrics.resultDay >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
            ${metrics.resultDay.toFixed(2)}
          </span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Wallet className="h-4 w-4" />
            <span>Total PNL (MT5)</span>
          </div>
          <span className={`text-2xl md:text-xl lg:text-2xl font-semibold ${metrics.totalPnl >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
            ${metrics.totalPnl.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  )
}
