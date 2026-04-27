"use client"

import { Blocks, BarChart3, Rabbit, Container, Banknote, Terminal, SquareArrowOutUpRight, Settings2, LogOut } from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="sticky top-24 h-[calc(100vh-8rem)] md:w-48 lg:w-64 bg-[#0D0D0D] rounded-2xl hidden md:flex flex-col p-8 overflow-y-auto">
      <nav className="flex flex-col gap-8">
        <Link href="/" className={`flex items-center gap-4 transition-colors cursor-pointer ${pathname === '/' ? 'text-[#E7E7E7]' : 'text-[#919191] hover:text-[#E7E7E7]'}`}>
          <Blocks className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">PAINEL AO VIVO</span>
        </Link>
        <Link href="/monitor" className={`flex items-center gap-4 transition-colors cursor-pointer ${pathname === '/monitor' ? 'text-[#E7E7E7]' : 'text-[#919191] hover:text-[#E7E7E7]'}`}>
          <Container className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">MONITOR ZONAS H1</span>
        </Link>
        <Link href="/historico" className={`flex items-center gap-4 transition-colors cursor-pointer ${pathname === '/historico' ? 'text-[#E7E7E7]' : 'text-[#919191] hover:text-[#E7E7E7]'}`}>
          <BarChart3 className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">HISTÓRICO</span>
        </Link>
        <Link href="/gatilhos" className={`flex items-center gap-4 transition-colors cursor-pointer ${pathname === '/gatilhos' ? 'text-[#E7E7E7]' : 'text-[#919191] hover:text-[#E7E7E7]'}`}>
          <Rabbit className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">GATILHOS</span>
        </Link>
        <Link href="/logs" className={`flex items-center gap-4 transition-colors cursor-pointer ${pathname === '/logs' ? 'text-[#E7E7E7]' : 'text-[#919191] hover:text-[#E7E7E7]'}`}>
          <Terminal className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">LOGS</span>
        </Link>
        <div className="flex items-center gap-4 text-[#919191] hover:text-[#E7E7E7] transition-colors cursor-pointer">
          <Banknote className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">PERFORMANCE</span>
        </div>
      </nav>

      <div className="mt-auto pt-8 border-t border-[#1F1F1F] flex flex-col gap-8">
        <div className="flex items-center gap-4 text-[#919191] hover:text-[#E7E7E7] transition-colors cursor-pointer">
          <SquareArrowOutUpRight className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">SYNCRA SUPPORT</span>
        </div>
        <div className="flex items-center gap-4 text-[#919191] hover:text-[#E7E7E7] transition-colors cursor-pointer">
          <Settings2 className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">SETTINGS</span>
        </div>
        <div className="flex items-center gap-4 text-[#919191] hover:text-[#E7E7E7] transition-colors cursor-pointer">
          <LogOut className="h-6 w-6" />
          <span className="text-sm font-medium tracking-wide">LOGOUT</span>
        </div>
      </div>
    </aside>
  )
}
