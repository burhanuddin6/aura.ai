import { NextResponse } from "next/server"

// Mock data for recent chats
const mockChats = [
  {
    id: "chat-1",
    title: "HackerRank and Apps Dataset Analysis",
    datetime: new Date("2025-04-15T14:30:00Z").toISOString(),
  },
  {
    id: "chat-2",
    title: "LaTeX Formatting of Code Systems",
    datetime: new Date("2025-04-14T09:15:00Z").toISOString(),
  },
  {
    id: "chat-3",
    title: "AI Startup Plan for Pakistan",
    datetime: new Date("2025-04-13T16:45:00Z").toISOString(),
  },
  {
    id: "chat-4",
    title: "Pakistan AI Chatbot Startup Plan",
    datetime: new Date("2025-04-12T11:20:00Z").toISOString(),
  },
  {
    id: "chat-5",
    title: "High Throughput Data System Design",
    datetime: new Date("2025-04-11T13:10:00Z").toISOString(),
  },
]

export async function GET() {
  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Return the array directly, not wrapped in an object
  return NextResponse.json(mockChats)
}

export async function POST(request: Request) {
  const body = await request.json()
  const { message } = body

  // Create a new chat with the message
  const newChat = {
    id: `chat-${Date.now()}`,
    title: message.slice(0, 30) + (message.length > 30 ? "..." : ""),
    datetime: new Date().toISOString(),
  }

  // In a real app, you would save this to a database

  return NextResponse.json(newChat)
}
