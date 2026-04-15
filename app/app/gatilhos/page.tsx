"use client"

import { useEffect, useState } from "react"
import { Target, Zap, Settings, ShieldCheck } from 'lucide-react'
import { supabase } from "@/lib/supabase"

export default function GatilhosPage() {
  const [executedTrades, setExecutedTrades] = useState<any[]>([])

  useEffect(() => {
    const fetchTrades = async () => {
      const { data } = await supabase
        .from('signals_liquidez')
        .select('*')
        .not('status', 'in', '("awaiting_consensus", "rejected")')
        .order('created_at', { ascending: false })
      if (data) setExecutedTrades(data)
    }
    fetchTrades()
  }, [])

  return (
    <div className="flex-1 flex flex-col gap-6 min-w-0 pb-12">
      <div className="flex items-center justify-between p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
        <div className="flex flex-col gap-1">
          <div className="flex items-center gap-2 text-[#0047AB]">
            <Target className="h-5 w-5" />
            <span className="text-xl font-medium tracking-wide">CENTRO DE GATILHOS EXECUTADOS</span>
          </div>
          <p className="text-sm text-gray-500">Detalhamento técnico de entradas realizadas e performance por operação.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
         <div className="p-4 bg-[#0D0D0D] rounded-xl border border-[#1A1A1A] flex flex-col gap-2">
            <span className="text-xs text-gray-500 uppercase font-bold">Estratégia</span>
            <span className="text-white font-medium">Liquidez H1 (Wick Retracement)</span>
         </div>
         <div className="p-4 bg-[#0D0D0D] rounded-xl border border-[#1A1A1A] flex flex-col gap-2">
            <span className="text-xs text-gray-500 uppercase font-bold">Timeframe</span>
            <span className="text-white font-medium">M5 (Entrada) / H1 (Zonas)</span>
         </div>
         <div className="p-4 bg-[#0D0D0D] rounded-xl border border-[#1A1A1A] flex flex-col gap-2">
            <span className="text-xs text-gray-500 uppercase font-bold">Risco/Retorno Médio</span>
            <span className="text-white font-medium">1:2.5</span>
         </div>
         <div className="p-4 bg-[#0D0D0D] rounded-xl border border-[#1A1A1A] flex flex-col gap-2">
            <span className="text-xs text-gray-500 uppercase font-bold">Consenso Agêntico</span>
            <span className="text-emerald-500 font-medium flex items-center gap-1">
               <ShieldCheck className="h-4 w-4" /> ATIVO
            </span>
         </div>
      </div>

      <div className="bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A] overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#1A1A1A]/50 text-gray-400 text-xs uppercase tracking-wider">
              <th className="p-4 font-medium">Data/Hora</th>
              <th className="p-4 font-medium">Tipo</th>
              <th className="p-4 font-medium">Preço</th>
              <th className="p-4 font-medium">SL / TP</th>
              <th className="p-4 font-medium">Status</th>
              <th className="p-4 font-medium text-right">Resultado</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#1A1A1A]">
            {executedTrades.map((trade) => (
              <tr key={trade.id} className="hover:bg-[#1A1A1A]/30 transition-colors">
                <td className="p-4 text-sm text-gray-300">
                  {new Date(trade.created_at).toLocaleString()}
                </td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-[10px] font-bold ${
                    trade.type === 'SELL' ? 'bg-red-500/10 text-red-500' : 'bg-emerald-500/10 text-emerald-500'
                  }`}>
                    {trade.type}
                  </span>
                </td>
                <td className="p-4 text-sm font-mono text-white">
                  {trade.price?.toFixed(5)}
                </td>
                <td className="p-4 text-[10px] font-mono text-gray-500">
                  SL: {trade.sl?.toFixed(5)} <br/>
                  TP: {trade.tp?.toFixed(5)}
                </td>
                <td className="p-4">
                  <span className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded ${
                    trade.status === 'closed' ? 'bg-gray-800 text-gray-400' : 
                    trade.status === 'active' ? 'bg-emerald-500/20 text-emerald-500' : 'bg-[#0047AB]/20 text-[#0047AB]'
                  }`}>
                    {trade.status}
                  </span>
                </td>
                <td className="p-4 text-right">
                  <span className={`text-sm font-bold font-mono ${
                    (trade.pnl || 0) > 0 ? 'text-emerald-500' : (trade.pnl || 0) < 0 ? 'text-red-500' : 'text-gray-500'
                  }`}>
                    {trade.pnl ? `${trade.pnl > 0 ? '+' : ''}${trade.pnl.toFixed(2)} USD` : 'OPEN'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
