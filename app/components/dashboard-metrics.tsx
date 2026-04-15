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
    // 1. Zonas Ativas (Último Heartbeat)
    const { data: heartbeat } = await supabase
      .from('bot_heartbeats')
      .select('active_zones')
      .order('created_at', { ascending: false })
      .limit(1)
    
    // 2. Sinais e PNL
    const { data: signals } = await supabase
      .from('signals_liquidez')
      .select('pnl, wick_pct, created_at, status')

    if (signals) {
      const now = new Date()
      const last24h = new Date(now.getTime() - 24 * 60 * 60 * 1000)
      const startOfDay = new Date(now.setHours(0, 0, 0, 0))

      const signals24h = signals.filter(s => new Date(s.created_at) > last24h).length
      const wicks = signals.filter(s => new Date(s.created_at) > last24h).map(s => s.wick_pct || 0)
      const avgWick = wicks.length > 0 ? (wicks.reduce((a, b) => a + b, 0) / wicks.length) * 100 : 0
      
      const resultDay = signals
        .filter(s => s.status === 'closed' && new Date(s.created_at) > startOfDay)
        .reduce((acc, s) => acc + (s.pnl || 0), 0)
      
      const totalPnl = signals
        .filter(s => s.status === 'closed')
        .reduce((acc, s) => acc + (s.pnl || 0), 0)

      setMetrics({
        activeZones: heartbeat?.[0]?.active_zones || 0,
        signals24h,
        avgWick,
        resultDay,
        totalPnl
      })
    }
  }

  useEffect(() => {
    fetchMetrics()
    
    const channel = supabase.channel('metrics-db-changes')
      .on('postgres_changes', { event: '*', table: 'signals_liquidez' }, () => fetchMetrics())
      .on('postgres_changes', { event: 'INSERT', table: 'bot_heartbeats' }, () => fetchMetrics())
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [])

  return (
    <div className="flex flex-col xl:flex-row gap-8 xl:items-center justify-between p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2 text-gray-400">
          <Activity className="h-5 w-5 text-[#0047AB]" />
          <span className="text-lg">Zonas H1 Ativas</span>
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
            <span>Result (Day)</span>
          </div>
          <span className={`text-2xl md:text-xl lg:text-2xl font-semibold ${metrics.resultDay >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
            ${metrics.resultDay.toFixed(2)}
          </span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Wallet className="h-4 w-4" />
            <span>Total PNL</span>
          </div>
          <span className={`text-2xl md:text-xl lg:text-2xl font-semibold ${metrics.totalPnl >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
            ${metrics.totalPnl.toFixed(2)}
          </span>
        </div>
      </div>
    </div>
  )
}
