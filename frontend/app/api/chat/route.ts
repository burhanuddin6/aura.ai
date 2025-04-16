import { NextResponse } from "next/server"
import { openai } from "@ai-sdk/openai"
import { generateText } from "ai"

export const runtime = "nodejs"

export async function POST(req: Request) {
  const { messages } = await req.json()

  try {
    // Use the AI SDK to generate a response
    const response = await generateText({
      model: openai("gpt-4o"),
      prompt: messages.map((message: any) => message.content).join("\n"),
      system:
        "You are Gemini, a helpful AI assistant created by Google. You are knowledgeable, creative, and designed to be helpful in a wide range of tasks.",
    })

    // Return the response as a streaming text response
    return NextResponse.json({ role: "assistant", content: response.text })
  } catch (error) {
    console.error("Error generating AI response:", error)
    return NextResponse.json({ error: "Failed to generate response" }, { status: 500 })
  }
}
