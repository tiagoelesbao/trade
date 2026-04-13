"use client"

import { Wallet, Activity, Target, Zap } from 'lucide-react'

interface MetricsProps {
  activeZones?: number
  signalsToday?: number
  efficiency?: number
  pnl?: string
  resultDay?: string
}

export function DashboardMetrics({ activeZones = 0, signalsToday = 0, efficiency = 0, pnl = "--", resultDay = "$0.00" }: MetricsProps) {
  return (
    <div className="flex flex-col xl:flex-row gap-8 xl:items-center justify-between p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-2 text-gray-400">
          <Activity className="h-5 w-5 text-[#0047AB]" />
          <span className="text-lg">Zonas H1 Ativas</span>
        </div>
        <div className="text-5xl md:text-4xl lg:text-5xl font-bold text-white">{activeZones}</div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-8 xl:gap-16">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Zap className="h-4 w-4" />
            <span>Sinais (24h)</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-white">{signalsToday}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Target className="h-4 w-4" />
            <span>Pavio Médio %</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-[#0047AB]">{efficiency}%</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <span>Result (Day)</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-[#86efac]">{resultDay}</span>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-gray-400 text-sm">
            <Wallet className="h-4 w-4" />
            <span>Total PNL</span>
          </div>
          <span className="text-2xl md:text-xl lg:text-2xl font-semibold text-[#86efac]">{pnl}</span>
        </div>
      </div>
    </div>
  )
}
