"use client"

import type React from "react"

import { useState } from "react"
import Sidebar from "@/components/sidebar"
import ChatArea from "@/components/chat-area"
import InputArea from "@/components/input-area"
import Header from "@/components/header"
import { useMediaQuery } from "@/hooks/use-media-query"
import { createNewChat, sendMessage } from "@/lib/api"

interface Message {
  role: "user" | "assistant"
  content: string
  attachments?: string[]
}

export default function AuraInterface() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const isDesktop = useMediaQuery("(min-width: 768px)")
  const [selectedModel, setSelectedModel] = useState("Aura")
  const [selectedChatId, setSelectedChatId] = useState<string | null>(null)
  const [isNewChat, setIsNewChat] = useState(true)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([])
  const [dataSources, setDataSources] = useState<string[]>([])

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen)
  }

  const handleNewChat = () => {
    setSelectedChatId(null)
    setIsNewChat(true)
    setMessages([])
    setUploadedFiles([])
    setDataSources([])
  }

  const handleSelectChat = (chatId: string) => {
    setSelectedChatId(chatId)
    setIsNewChat(false)
    setMessages([]) // Clear current messages as we'll load from API
    setUploadedFiles([])
    setDataSources([])
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
  }

  const handleFileUpload = (files: string[]) => {
    setUploadedFiles(files)
  }

  const handleDataSourcesAdd = (sources: string[]) => {
    setDataSources(sources)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    if (!input.trim()) return

    const userMessage = input
    setInput("")

    // Show thinking indicator
    setIsThinking(true)
    setIsLoading(true)

    try {
      if (isNewChat) {
        // Add user message to the UI immediately
        setMessages([
          ...messages,
          {
            role: "user",
            content: userMessage,
            attachments: uploadedFiles.length > 0 ? [...uploadedFiles] : undefined,
          },
        ])

        // Create a new chat with the message and any files/data sources
        createNewChat(userMessage, uploadedFiles, dataSources).then(({ chatId, response }) => {
          // Add AI response
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: response,
            },
          ])

          setSelectedChatId(chatId)
          setIsNewChat(false)
          setIsThinking(false)
          setIsLoading(false)

          // Clear uploaded files after sending
          setUploadedFiles([])
        })
      } else if (selectedChatId) {
        // Add user message to the UI immediately
        setMessages([
          ...messages,
          {
            role: "user",
            content: userMessage,
            attachments: uploadedFiles.length > 0 ? [...uploadedFiles] : undefined,
          },
        ])

        // Send message to API with any files/data sources
        sendMessage(selectedChatId, userMessage, uploadedFiles, dataSources).then(({ response }) => {
          setMessages((prev) => [...prev, response])
          setIsThinking(false)
          setIsLoading(false)

          // Clear uploaded files after sending
          setUploadedFiles([])
        })
      }
    } catch (error) {
      console.error("Error sending message:", error)
      setIsThinking(false)
      setIsLoading(false)
    }
  }

  return (
    <div className="flex h-full bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen && isDesktop}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
        selectedChatId={selectedChatId}
        onAddDataSources={handleDataSourcesAdd}
      />

      {/* Main Content */}
      <div className="flex flex-col flex-1 h-full overflow-hidden">
        <Header toggleSidebar={toggleSidebar} selectedModel={selectedModel} setSelectedModel={setSelectedModel} />

        <div className="flex-1 overflow-auto">
          <ChatArea selectedChatId={selectedChatId} messages={messages} isNewChat={isNewChat} isThinking={isThinking} />
        </div>

        <InputArea
          input={input}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
          onFileUpload={handleFileUpload}
          uploadedFiles={uploadedFiles}
        />
      </div>
    </div>
  )
}
