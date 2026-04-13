"use client"

import { TickerList } from "@/components/ticker-list"
import { BarChart3 } from 'lucide-react'

export default function HistoricoPage() {
  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <div className="flex items-center gap-2 p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
        <BarChart3 className="h-6 w-6 text-[#0047AB]" />
        <span className="text-xl font-medium tracking-wide">HISTÓRICO DE SINAIS</span>
      </div>

      <div className="p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
         <TickerList />
      </div>
    </div>
  )
}
