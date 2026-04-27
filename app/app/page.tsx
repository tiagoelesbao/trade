"use client"

import { useEffect, useState, useCallback } from "react"
import { DashboardMetrics } from "@/components/dashboard-metrics"
import { PerformanceChart } from "@/components/performance-chart"
import { TickerList } from "@/components/ticker-list"
import { supabase } from "@/lib/supabase"

const HEARTBEAT_TIMEOUT_MS = 90_000 // 90 segundos = offline

function formatAgo(isoDate: string): string {
  const diff = Date.now() - new Date(isoDate).getTime()
  const secs = Math.floor(diff / 1000)
  if (secs < 60) return `${secs}s atrás`
  const mins = Math.floor(secs / 60)
  if (mins < 60) return `${mins}min atrás`
  return `${Math.floor(mins / 60)}h atrás`
}

export default function Dashboard() {
  const [botStatus, setBotStatus] = useState<"online" | "offline">("offline")
  const [lastHeartbeatAt, setLastHeartbeatAt] = useState<string | null>(null)
  const [agoLabel, setAgoLabel] = useState<string>("")

  const checkHeartbeat = useCallback(async () => {
    const { data } = await supabase
      .from('bot_heartbeats')
      .select('created_at')
      .order('created_at', { ascending: false })
      .limit(1)

    if (data && data.length > 0) {
      const ts = data[0].created_at
      const age = Date.now() - new Date(ts).getTime()
      setLastHeartbeatAt(ts)
      setBotStatus(age < HEARTBEAT_TIMEOUT_MS ? "online" : "offline")
    } else {
      setBotStatus("offline")
    }
  }, [])

  useEffect(() => {
    checkHeartbeat()

    // Re-verifica a cada 30s (fallback independente do Realtime)
    const poll = setInterval(checkHeartbeat, 30_000)

    // Atualiza o label "X min atrás" a cada 10s
    const labelTimer = setInterval(() => {
      if (lastHeartbeatAt) setAgoLabel(formatAgo(lastHeartbeatAt))
    }, 10_000)

    const sub = supabase
      .channel('heartbeats-status')
      .on('postgres_changes', { event: '*', schema: 'public', table: 'bot_heartbeats' }, () => {
        checkHeartbeat()
      })
      .subscribe()

    return () => {
      clearInterval(poll)
      clearInterval(labelTimer)
      supabase.removeChannel(sub)
    }
  }, [checkHeartbeat])

  // Atualiza label imediatamente quando o timestamp muda
  useEffect(() => {
    if (lastHeartbeatAt) setAgoLabel(formatAgo(lastHeartbeatAt))
  }, [lastHeartbeatAt])

  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <DashboardMetrics />
      <PerformanceChart />
      <TickerList />

      {/* Status Indicator */}
      <div className="flex items-center justify-end gap-3 mt-2">
        {agoLabel && (
          <span className="text-[10px] text-gray-600 uppercase tracking-widest">
            heartbeat {agoLabel}
          </span>
        )}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-[#0D0D0D] border border-[#1A1A1A] rounded-full">
          <div className={`w-[9px] h-[9px] rounded-full ${
            botStatus === "online"
              ? "bg-emerald-500 shadow-[0_0_8px_#10b981] animate-pulse"
              : "bg-red-500 shadow-[0_0_8px_#ef4444]"
          }`} />
          <span className="text-[10px] font-bold uppercase tracking-tighter text-[#919191]">
            {botStatus === "online" ? "Motor Ativo" : "Motor Offline"}
          </span>
        </div>
      </div>
    </div>
  )
}
