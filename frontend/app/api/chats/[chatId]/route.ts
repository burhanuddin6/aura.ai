import { NextResponse } from "next/server"

// Mock data for chat messages
const mockChatMessages = {
  "chat-1": [
    { role: "user", content: "Can you analyze this HackerRank dataset for me?" },
    {
      role: "assistant",
      content: "I'd be happy to analyze the HackerRank dataset for you. What specific insights are you looking for?",
    },
  ],
  "chat-2": [
    { role: "user", content: "How do I format code in LaTeX?" },
    {
      role: "assistant",
      content:
        "To format code in LaTeX, you can use the 'verbatim' environment for simple code snippets or the 'listings' package for more advanced code formatting with syntax highlighting.",
    },
  ],
}

export async function GET(request: Request, { params }: { params: { chatId: string } }) {
  const chatId = params.chatId

  // Simulate network delay
  await new Promise((resolve) => setTimeout(resolve, 800))

  // Return mock data or empty array if chat doesn't exist
  const messages = mockChatMessages[chatId as keyof typeof mockChatMessages] || []

  return NextResponse.json({ id: chatId, messages })
}

export async function POST(request: Request, { params }: { params: { chatId: string } }) {
  const chatId = params.chatId
  const body = await request.json()

  // In a real app, you would save this message to a database

  return NextResponse.json({ success: true, chatId })
}
