"use client"

import { useEffect, useState } from "react"
import { DashboardMetrics } from "@/components/dashboard-metrics"
import { PerformanceChart } from "@/components/performance-chart"
import { TickerList } from "@/components/ticker-list"
import { supabase } from "@/lib/supabase"

export default function Dashboard() {
  const [botStatus, setBotStatus] = useState<"online" | "offline">("offline")
  const [lastScan, setLastScan] = useState<string | null>(null)

  useEffect(() => {
    const fetchInitialStatus = async () => {
      const { data: heartbeats } = await supabase
        .from('bot_heartbeats')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(1)

      if (heartbeats && heartbeats.length > 0) {
        const lastHeartbeat = new Date(heartbeats[0].created_at).getTime()
        const now = new Date().getTime()
        
        // Se o último sinal foi há menos de 10 minutos, marcar como online
        if (now - lastHeartbeat < 600000) {
          setBotStatus("online")
          setLastScan(new Date(heartbeats[0].created_at).toLocaleTimeString())
        }
      }
    }

    fetchInitialStatus()

    const heartbeatSub = supabase
      .channel('heartbeats')
      .on('postgres_changes', { event: 'INSERT', table: 'bot_heartbeats' }, () => {
        setBotStatus("online")
        setLastScan(new Date().toLocaleTimeString())
      })
      .subscribe()

    return () => {
      supabase.removeChannel(heartbeatSub)
    }
  }, [])

  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <DashboardMetrics />
      <PerformanceChart />
      <TickerList />
      
      {/* Status Indicator */}
      <div className="flex items-center justify-end gap-4 mt-4">
        {lastScan && (
          <span className="text-xs text-gray-500 italic uppercase tracking-widest">
            Última Varredura: {lastScan}
          </span>
        )}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-[#0D0D0D] border border-[#1A1A1A] rounded-full shadow-xl">
          <div className={`w-[10px] h-[10px] rounded-full shadow-[0_0_10px] ${
            botStatus === "online" 
              ? "bg-emerald-500 shadow-emerald-500/50 animate-pulse" 
              : "bg-red-500 shadow-red-500/50"
          }`} />
          <span className="text-[10px] font-bold uppercase tracking-tighter text-[#919191]">
            Status: {botStatus === "online" ? "Motor Ativo" : "Motor Offline"}
          </span>
        </div>
      </div>
    </div>
  )
}
