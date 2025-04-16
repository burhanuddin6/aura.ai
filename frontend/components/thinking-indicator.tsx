"use client"

import { useEffect, useState } from "react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export default function ThinkingIndicator() {
  const [dots, setDots] = useState(".")

  // Animate the dots
  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => {
        if (prev.length >= 3) return "."
        return prev + "."
      })
    }, 500)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex items-start gap-4 mb-6 animate-fade-in">
      <Avatar>
        <AvatarFallback className="bg-purple-100 text-purple-800">A</AvatarFallback>
        <AvatarImage src="/aura-avatar.png" />
      </Avatar>

      <div className="relative bg-white rounded-lg p-3 shadow-sm max-w-[80%] overflow-hidden">
        <p className="text-gray-800">Thinking{dots}</p>

        {/* Shining animation */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute inset-0 shine-effect"></div>
        </div>
      </div>
    </div>
  )
}

// Add this to your globals.css
