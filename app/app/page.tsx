"use client"

import { useEffect, useState } from "react"
import { DashboardMetrics } from "@/components/dashboard-metrics"
import { PerformanceChart } from "@/components/performance-chart"
import { TickerList } from "@/components/ticker-list"
import { Sidebar } from "@/components/sidebar"
import { Header } from "@/components/header"
import { supabase } from "@/lib/supabase"

export default function Dashboard() {
  const [botStatus, setBotStatus] = useState<"online" | "offline">("offline")
  const [lastScan, setLastScan] = useState<string | null>(null)
  const [activeZones, setActiveZones] = useState(0)
  const [signalsToday, setSignalsToday] = useState(0)

  useEffect(() => {
    const fetchInitialStatus = async () => {
      // 1. Busca Status e Zonas
      const { data: heartbeats } = await supabase
        .from('bot_heartbeats')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(1)

      if (heartbeats && heartbeats.length > 0) {
        const lastHeartbeat = new Date(heartbeats[0].created_at).getTime()
        const now = new Date().getTime()
        const diffMinutes = Math.floor((now - lastHeartbeat) / 60000)
        
        console.log(`[Status] Último sinal há ${diffMinutes} min. (${new Date(heartbeats[0].created_at).toLocaleString()})`)

        // Se o último sinal foi há menos de 10 minutos, marcar como online
        if (now - lastHeartbeat < 600000) {
          setBotStatus("online")
          setLastScan(new Date(heartbeats[0].created_at).toLocaleTimeString())
          setActiveZones(heartbeats[0].active_zones || 0)
        }
      }

      // 2. Busca Sinais de Hoje
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const { count } = await supabase
        .from('signals_liquidez')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', today.toISOString())
      
      setSignalsToday(count || 0)
    }

    fetchInitialStatus()

    // Escuta batimentos cardíacos
    const heartbeatSub = supabase
      .channel('heartbeats')
      .on('postgres_changes', { event: 'INSERT', table: 'bot_heartbeats' }, (payload) => {
        setBotStatus("online")
        setLastScan(new Date().toLocaleTimeString())
        setActiveZones(payload.new.active_zones || 0)
      })
      .subscribe()

    // Escuta novos sinais para atualizar contagem
    const signalsSub = supabase
      .channel('signals_count')
      .on('postgres_changes', { event: 'INSERT', table: 'signals_liquidez' }, () => {
        setSignalsToday(prev => prev + 1)
      })
      .subscribe()

    return () => {
      supabase.removeChannel(heartbeatSub)
      supabase.removeChannel(signalsSub)
    }
  }, [])

  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <DashboardMetrics 
        activeZones={activeZones} 
        signalsToday={signalsToday} 
        efficiency={0} 
        pnl="--"
        resultDay="$0.00"
      />
      <PerformanceChart />
      <TickerList />
      
      {/* Status Indicator */}
      <div className="flex items-center justify-end gap-4 mt-4">
          {lastScan && (
          <span className="text-xs text-gray-500 italic">Last Scan: {lastScan}</span>
        )}
        <div className="flex items-center gap-2">
          <div className={`w-[13px] h-[13px] rounded-full shadow-[0_0_8px] ${
            botStatus === "online" 
              ? "bg-[#0047AB] shadow-[#0047AB]/50 animate-pulse" 
              : "bg-red-500 shadow-red-500/50"
          }`} />
          <span className="text-sm text-[#919191]">
            Bot {botStatus === "online" ? "Operando" : "Offline"}
          </span>
        </div>
      </div>
    </div>
  )
}
