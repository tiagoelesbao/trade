"use client"

import { TickerList } from "@/components/ticker-list"
import { AgentWarRoom } from "@/components/agent-war-room"
import { Activity, ShieldAlert } from 'lucide-react'

export default function MonitorPage() {
  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <div className="flex items-center justify-between p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-[#0047AB]">
            <Activity className="h-5 w-5" />
            <span className="text-xl font-medium tracking-wide">MONITOR DE ZONAS H1</span>
          </div>
          <p className="text-sm text-gray-500">Monitoramento em tempo real de liquidez institucional e violinações.</p>
        </div>
        <div className="flex items-center gap-2 px-4 py-2 bg-[#1A1A1A] rounded-lg border border-[#333]">
           <ShieldAlert className="h-4 w-4 text-yellow-500" />
           <span className="text-xs text-white">MODO VIGILÂNCIA ATIVO</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
           <TickerList />
        </div>
        
        <div className="flex flex-col p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A] min-h-[400px]">
           <AgentWarRoom />
        </div>
      </div>
    </div>
  )
}

