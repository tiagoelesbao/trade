import type { Metadata } from 'next'
import { Space_Grotesk } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'
import { Header } from '@/components/header'
import { Sidebar } from '@/components/sidebar'

const spaceGrotesk = Space_Grotesk({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: 'Syncra AIOX | Trading Dashboard',
  description: 'Painel operacional para robô de liquidez institucional',
  icons: {
    icon: [
      {
        url: '/icon-light-32x32.png',
        media: '(prefers-color-scheme: light)',
      },
      {
        url: '/icon-dark-32x32.png',
        media: '(prefers-color-scheme: dark)',
      },
      {
        url: '/icon.svg',
        type: 'image/svg+xml',
      },
    ],
    apple: '/apple-icon.png',
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`${spaceGrotesk.className} antialiased bg-black text-white`}>
        <div className="relative h-screen w-full overflow-hidden">
          <Header />
          <div className="h-full overflow-y-auto no-scrollbar">
            <main className="flex gap-6 p-6 pt-24 min-h-full">
              <Sidebar />
              {children}
            </main>
          </div>
        </div>
        <Analytics />
      </body>
    </html>
  )
}
