"use client"

import { useState, useEffect } from "react"
import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid } from "recharts"
import { supabase } from "@/lib/supabase"

export function PerformanceChart() {
  const [chartData, setChartData] = useState<{date: string, pnl: number}[]>([])
  const [totalProfit, setTotalProfit] = useState(0)

  const fetchPerformance = async () => {
    // Puxa todos os sinais fechados com PNL válido para montar a curva
    const { data } = await supabase
      .from('signals_liquidez')
      .select('pnl, closed_at')
      .eq('status', 'closed')
      .not('pnl', 'is', null)
      .order('closed_at', { ascending: true })
    
    if (data) {
      let cumulativePnl = 0
      const formatted = data.map((item: any) => {
        cumulativePnl += item.pnl || 0
        return {
          date: new Date(item.closed_at).toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' }),
          pnl: cumulativePnl
        }
      })
      setChartData(formatted)
      setTotalProfit(cumulativePnl)
    }
  }

  useEffect(() => {
    fetchPerformance()

    // Escuta mudanças (Insert/Update) para atualizar o gráfico em tempo real
    const channel = supabase.channel('perf-realtime')
      .on('postgres_changes', { event: '*', table: 'signals_liquidez' }, () => {
        fetchPerformance()
      })
      .subscribe()

    return () => { supabase.removeChannel(channel) }
  }, [])

  return (
    <div className="flex flex-col gap-6 p-6 bg-[#0D0D0D] rounded-2xl border border-[#1A1A1A]">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <h2 className="text-xl font-medium text-white">Performance do Algoritmo</h2>
          <div className={`px-3 py-1 rounded-full border ${totalProfit >= 0 ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-500' : 'bg-red-500/10 border-red-500/20 text-red-500'}`}>
            <span className="text-sm font-medium">{totalProfit >= 0 ? '+' : ''}{totalProfit.toFixed(2)} USD</span>
          </div>
        </div>
      </div>

      <div className="h-[350px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData.length > 0 ? chartData : [{date: 'Aguardando', pnl: 0}]}>
            <defs>
              <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={totalProfit >= 0 ? "#10b981" : "#ef4444"} stopOpacity={0.3}/>
                <stop offset="95%" stopColor={totalProfit >= 0 ? "#10b981" : "#ef4444"} stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F1F1F" vertical={false} />
            <XAxis 
              dataKey="date" 
              hide 
            />
            <YAxis 
              tick={{ fill: '#666', fontSize: 12 }} 
              axisLine={false}
              tickLine={false}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip 
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  return (
                    <div className="bg-[#1A1A1A] border border-[#333] p-3 rounded-lg shadow-2xl">
                      <p className={`text-lg font-bold ${payload[0].value >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
                        {payload[0].value >= 0 ? '+' : ''}{payload[0].value?.toFixed(2)} USD
                      </p>
                      <p className="text-gray-500 text-xs mt-1">{payload[0].payload.date}</p>
                    </div>
                  )
                }
                return null
              }}
            />
            
            <Area 
              type="monotone" 
              dataKey="pnl" 
              stroke={totalProfit >= 0 ? "#10b981" : "#ef4444"} 
              strokeWidth={2} 
              fillOpacity={1} 
              fill="url(#colorPrice)" 
              animationDuration={1000}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
