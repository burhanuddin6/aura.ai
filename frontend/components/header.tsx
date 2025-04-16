"use client"

import { Menu } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { ModelSelector } from "@/components/model-selector"

interface HeaderProps {
  toggleSidebar: () => void
  selectedModel: string
  setSelectedModel: (model: string) => void
}

export default function Header({ toggleSidebar, selectedModel, setSelectedModel }: HeaderProps) {
  return (
    <header className="flex items-center justify-between p-4 border-b bg-white">
      <div className="flex items-center">
        <Button variant="ghost" size="icon" onClick={toggleSidebar} className="mr-2">
          <Menu className="h-5 w-5" />
        </Button>

        <ModelSelector onModelChange={setSelectedModel} />

        <div className="ml-2 text-sm text-gray-500">2.0 Flash</div>
      </div>

      <div className="flex items-center">
        <Avatar className="h-8 w-8">
          <AvatarFallback className="bg-blue-100 text-blue-800">U</AvatarFallback>
          <AvatarImage src="/user-avatar.png" alt="User" />
        </Avatar>
      </div>
    </header>
  )
}
