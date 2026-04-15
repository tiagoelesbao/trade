"use client"

import { useEffect, useState } from "react"
import { ArrowUp, ArrowDown, ChevronsUpDown, Info } from 'lucide-react'
import { Area, AreaChart, ResponsiveContainer } from "recharts"
import { supabase } from "@/lib/supabase"

export function TickerList() {
  const [signals, setSignals] = useState<any[]>([])

  useEffect(() => {
    // Busca inicial
    const fetchSignals = async () => {
      const { data } = await supabase
        .from('signals_liquidez')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(5)
      if (data) setSignals(data)
    }
    
    fetchSignals()

    // Realtime Sub
    const channel = supabase
      .channel('live-signals')
      .on('postgres_changes', { event: 'INSERT', table: 'signals_liquidez' }, (payload) => {
        setSignals(prev => [payload.new, ...prev].slice(0, 5))
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [])

  return (
    <div className="bg-[#0D0D0D] rounded-2xl p-6 border border-[#1A1A1A]">
      <div className="flex items-center justify-between mb-4">
         <h3 className="text-white font-medium flex items-center gap-2">
           Gatilhos Institucionais
           <Info className="h-4 w-4 text-gray-500" />
         </h3>
      </div>
      <table className="w-full">
        <thead>
          <tr className="text-[#919191] text-sm border-b border-[#1A1A1A]">
            <th className="pb-4 text-left font-medium">Ativo</th>
            <th className="pb-4 text-left font-medium">Tipo</th>
            <th className="pb-4 text-right font-medium">Preço</th>
            <th className="pb-4 text-center font-medium">Status</th>
            <th className="pb-4 text-center font-medium">AIA</th>
            <th className="pb-4 text-right font-medium pr-2">Resultado</th>
          </tr>
        </thead>
        <tbody>
          {signals.length === 0 ? (
            <tr>
              <td colSpan={6} className="py-10 text-center text-gray-500 italic">
                Aguardando novas capturas de liquidez...
              </td>
            </tr>
          ) : (
            signals.map((item) => (
              <tr 
                key={item.id} 
                className="group transition-colors border-b border-[#1A1A1A]/50 last:border-0 hover:bg-[#1A1A1A]/50"
              >
                <td className="py-4">
                  <div className="flex items-center gap-3">
                    <span className="font-bold text-white">{item.symbol}</span>
                  </div>
                </td>
                <td className="py-4">
                  <span className={`px-2 py-1 rounded text-[10px] font-bold ${
                    item.type === 'SELL' ? 'bg-red-500/10 text-red-500' : 'bg-emerald-500/10 text-emerald-500'
                  }`}>
                    {item.type}
                  </span>
                </td>
                <td className="py-4 text-right text-white font-mono text-sm">{item.price?.toFixed(5)}</td>
                <td className="py-4 text-center">
                   <span className={`text-[10px] uppercase font-bold ${
                     item.status === 'closed' ? 'text-gray-500' : 
                     item.status === 'active' ? 'text-emerald-500 animate-pulse' : 
                     item.status === 'placed' ? 'text-[#0047AB]' : 'text-yellow-500'
                   }`}>
                     {item.status || 'pending'}
                   </span>
                </td>
                <td className="py-4 text-center">
                   <div className="flex items-center justify-center gap-1">
                      <div className={`w-2 h-2 rounded-full shadow-[0_0_8px_rgba(0,0,0,0.3)] ${
                        item.status === 'rejected' ? 'bg-red-500' : 'bg-emerald-500'
                      }`}></div>
                      <span className={`text-[10px] font-bold ${
                        item.status === 'rejected' ? 'text-red-500' : 'text-emerald-500'
                      }`}>
                        {item.status === 'rejected' ? 'VETO' : 'ALTA'}
                      </span>
                   </div>
                </td>
                <td className="py-4 text-right font-medium pr-2">
                  <div className={`flex items-center justify-end gap-1 font-mono ${
                    (item.pnl || 0) > 0 ? 'text-emerald-500' : (item.pnl || 0) < 0 ? 'text-red-500' : 'text-gray-500'
                  }`}>
                    {item.pnl ? `${item.pnl > 0 ? '+' : ''}${item.pnl.toFixed(2)} USD` : '---'}
                  </div>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
