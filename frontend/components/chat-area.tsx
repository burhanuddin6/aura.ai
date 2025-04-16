"use client"

import { useEffect, useRef, useState } from "react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Skeleton } from "@/components/ui/skeleton"
import { fetchChatById } from "@/lib/api"
import ThinkingIndicator from "@/components/thinking-indicator"

interface Message {
  role: "user" | "assistant"
  content: string
  attachments?: string[]
}

interface ChatAreaProps {
  selectedChatId: string | null
  messages: Message[]
  isNewChat: boolean
  isThinking: boolean
}

export default function ChatArea({ selectedChatId, messages, isNewChat, isThinking }: ChatAreaProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [chatMessages, setChatMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)

  // Scroll to bottom when messages change or when thinking
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, chatMessages, isThinking])

  // Fetch chat messages when selectedChatId changes
  useEffect(() => {
    if (!selectedChatId || isNewChat) {
      setChatMessages([])
      return
    }

    const loadChatMessages = async () => {
      setIsLoading(true)
      try {
        const loadedMessages = await fetchChatById(selectedChatId)
        setChatMessages(loadedMessages)
      } catch (error) {
        console.error("Failed to load chat messages:", error)
      } finally {
        setIsLoading(false)
      }
    }

    loadChatMessages()
  }, [selectedChatId, isNewChat])

  // Combine API messages with current session messages
  const allMessages = isNewChat ? messages : [...chatMessages, ...messages]

  // If loading, show skeleton
  if (isLoading) {
    return (
      <div className="p-4 max-w-4xl mx-auto space-y-6">
        {[...Array(3)].map((_, index) => (
          <div key={index} className="flex items-start gap-4">
            <Skeleton className="h-10 w-10 rounded-full" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-4 w-32" />
              <Skeleton className="h-20 w-full" />
            </div>
          </div>
        ))}
      </div>
    )
  }

  // If no messages and new chat, show welcome message
  if (allMessages.length === 0 && !isThinking) {
    return (
      <div className="flex flex-col items-center justify-center h-full p-4 text-center">
        <h1 className="text-4xl font-light text-blue-500 mb-2">
          Hello, <span className="text-purple-500">User</span>
        </h1>
        <p className="text-gray-500 max-w-md">
          Ask me anything or upload a file to get started. I'm here to help with information, creative tasks, and more.
        </p>
      </div>
    )
  }

  return (
    <div className="p-4 max-w-4xl mx-auto">
      {allMessages.map((message, index) => (
        <div key={index} className="mb-6">
          {message.role === "user" ? (
            <div className="flex items-start gap-4">
              <Avatar>
                <AvatarFallback className="bg-blue-100 text-blue-800">U</AvatarFallback>
                <AvatarImage src="/user-avatar.png" />
              </Avatar>
              <div className="bg-blue-50 rounded-lg p-3 max-w-[80%]">
                <p className="text-gray-800">{message.content}</p>

                {/* Show file attachments if any */}
                {message.attachments && message.attachments.length > 0 && (
                  <div className="mt-2 pt-2 border-t border-blue-100">
                    <p className="text-xs text-blue-600 font-medium">Attached files:</p>
                    <ul className="text-xs text-blue-500">
                      {message.attachments.map((file, i) => (
                        <li key={i} className="truncate">
                          {file}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex items-start gap-4">
              <Avatar>
                <AvatarFallback className="bg-purple-100 text-purple-800">A</AvatarFallback>
                <AvatarImage src="/aura-avatar.png" />
              </Avatar>
              <div className="bg-white rounded-lg p-3 shadow-sm max-w-[80%]">
                <p className="text-gray-800">{message.content}</p>
              </div>
            </div>
          )}
        </div>
      ))}

      {/* Show thinking indicator when waiting for response */}
      {isThinking && <ThinkingIndicator />}

      <div ref={messagesEndRef} />
    </div>
  )
}
