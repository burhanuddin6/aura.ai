"use client"

import { useEffect, useState } from "react"
import { Plus, List, HelpCircle, Clock, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Skeleton } from "@/components/ui/skeleton"
import { fetchRecentChats, formatChatDate, type Chat } from "@/lib/api"
import DataSourcesModal from "@/components/data-sources-modal"

interface SidebarProps {
  isOpen: boolean
  onNewChat: () => void
  onSelectChat: (chatId: string) => void
  selectedChatId: string | null
  onAddDataSources?: (sources: string[]) => void
}

export default function Sidebar({ isOpen, onNewChat, onSelectChat, selectedChatId, onAddDataSources }: SidebarProps) {
  const [recentChats, setRecentChats] = useState<Chat[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const loadRecentChats = async () => {
      setIsLoading(true)
      try {
        const chats = await fetchRecentChats()
        setRecentChats(chats)
      } catch (error) {
        console.error("Failed to load recent chats:", error)
      } finally {
        setIsLoading(false)
      }
    }

    loadRecentChats()
  }, [])

  if (!isOpen) return null

  return (
    <div className="w-80 h-full bg-gray-50 border-r flex flex-col overflow-hidden">
      <div className="p-4 space-y-2">
        <Button onClick={onNewChat} variant="outline" className="w-full justify-start gap-2 rounded-full bg-white">
          <Plus className="h-4 w-4" />
          New chat
        </Button>

        <DataSourcesModal />
      </div>

      <div className="flex-1 overflow-y-auto px-4">
        <div className="mb-6">
          <h2 className="text-sm font-medium mb-2">Recent</h2>
          {isLoading ? (
            // Loading skeletons
            <div className="space-y-2">
              {[...Array(5)].map((_, index) => (
                <div key={index} className="flex items-center gap-2">
                  <Skeleton className="h-4 w-4 rounded-full" />
                  <Skeleton className="h-8 w-full rounded" />
                </div>
              ))}
            </div>
          ) : recentChats.length > 0 ? (
            <ul className="space-y-1">
              {recentChats.map((chat) => (
                <li key={chat.id}>
                  <Button
                    variant={selectedChatId === chat.id ? "secondary" : "ghost"}
                    className="w-full justify-start gap-2 text-gray-700"
                    onClick={() => onSelectChat(chat.id)}
                  >
                    <List className="h-4 w-4 shrink-0" />
                    <div className="flex flex-col items-start overflow-hidden">
                      <span className="truncate text-left w-full">{chat.title}</span>
                      <span className="text-xs text-gray-500">{formatChatDate(chat.datetime)}</span>
                    </div>
                  </Button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-gray-500 py-2">No recent chats</p>
          )}
        </div>

        <div className="space-y-1">
          <Button variant="ghost" className="w-full justify-start gap-2 text-gray-700">
            <HelpCircle className="h-4 w-4" />
            <span>Help</span>
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-2 text-gray-700">
            <Clock className="h-4 w-4" />
            <span>Activity</span>
          </Button>
          <Button variant="ghost" className="w-full justify-start gap-2 text-gray-700">
            <Settings className="h-4 w-4" />
            <span>Settings</span>
          </Button>
        </div>
      </div>

      <div className="p-4 text-xs text-gray-500 border-t">
        <p className="text-center">AURA AI</p>
      </div>
    </div>
  )
}
