import { NextResponse } from "next/server"
import { openai } from "@ai-sdk/openai"
import { generateText } from "ai"

export const runtime = "nodejs"

export async function POST(request: Request, { params }: { params: { chatId: string } }) {
  const chatId = params.chatId
  const body = await request.json()
  const { message } = body

  try {
    // Generate a response using AI SDK
    const response = await generateText({
      model: openai("gpt-4o"),
      prompt: message,
      system:
        "You are Gemini, a helpful AI assistant. You are knowledgeable, creative, and designed to be helpful in a wide range of tasks.",
    })

    // In a real app, you would save this message and response to a database

    return NextResponse.json({
      success: true,
      chatId,
      message: {
        role: "user",
        content: message,
      },
      response: {
        role: "assistant",
        content: response.text,
      },
    })
  } catch (error) {
    console.error("Error generating response:", error)
    return NextResponse.json({ error: "Failed to generate response" }, { status: 500 })
  }
}
