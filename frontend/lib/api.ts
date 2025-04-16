// Simple API with dummy data
import { formatDistanceToNow } from "date-fns"

// Types
export interface Chat {
  id: string
  title: string
  datetime: string
}

export interface Message {
  role: "user" | "assistant"
  content: string
  attachments?: string[]
}

// Dummy data for recent chats
const dummyChats: Chat[] = [
  {
    id: "chat-1",
    title: "HackerRank and Apps Dataset Analysis",
    datetime: "2025-04-15T14:30:00Z",
  },
  {
    id: "chat-2",
    title: "LaTeX Formatting of Code Systems",
    datetime: "2025-04-14T09:15:00Z",
  },
  {
    id: "chat-3",
    title: "AI Startup Plan for Pakistan",
    datetime: "2025-04-13T16:45:00Z",
  },
  {
    id: "chat-4",
    title: "Pakistan AI Chatbot Startup Plan",
    datetime: "2025-04-12T11:20:00Z",
  },
  {
    id: "chat-5",
    title: "High Throughput Data System Design",
    datetime: "2025-04-11T13:10:00Z",
  },
]

// Dummy data for chat messages
const dummyChatMessages: Record<string, Message[]> = {
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
  "chat-3": [
    { role: "user", content: "Help me create an AI startup plan for Pakistan" },
    {
      role: "assistant",
      content:
        "I'd be happy to help you create an AI startup plan for Pakistan. Let's start by identifying key market opportunities and challenges specific to the region.",
    },
  ],
  "chat-4": [
    { role: "user", content: "I need to build a chatbot for a Pakistani startup" },
    {
      role: "assistant",
      content:
        "Creating a chatbot for a Pakistani startup is a great idea. We should consider language support for Urdu and English, and focus on use cases that are relevant to the local market.",
    },
  ],
  "chat-5": [
    { role: "user", content: "Design a high throughput data system" },
    {
      role: "assistant",
      content:
        "For a high throughput data system, you'll want to consider distributed architecture, efficient data storage, and optimized query processing. Let's break down the key components.",
    },
  ],
}

// Helper function to format date
export const formatChatDate = (dateString: string): string => {
  try {
    const date = new Date(dateString)
    return formatDistanceToNow(date, { addSuffix: true })
  } catch (error) {
    return "Unknown date"
  }
}

// API functions
export const fetchRecentChats = async (): Promise<Chat[]> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Return sorted chats (newest first)
  return [...dummyChats].sort((a, b) => new Date(b.datetime).getTime() - new Date(a.datetime).getTime())
}

export const fetchChatById = async (chatId: string): Promise<Message[]> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 800))

  // Return chat messages or empty array if not found
  return dummyChatMessages[chatId] || []
}

// Simulated LLM response generator
export const generateLLMResponse = async (
  message: string,
  files?: string[],
  dataSources?: string[],
): Promise<string> => {
  // Simulate API delay - 2 seconds as requested
  await new Promise((resolve) => setTimeout(resolve, 2000))

  // Generate a response based on the message content and any files/data sources
  let response = ""

  if (files && files.length > 0) {
    response += `I've analyzed the ${files.length} file(s) you provided. `

    // Add some specific responses based on file types
    if (files.some((file) => file.endsWith(".pdf"))) {
      response += "The PDF document contains some interesting data that I can help interpret. "
    }
    if (files.some((file) => file.endsWith(".txt") || file.endsWith(".md"))) {
      response += "I've processed the text content you shared. "
    }
  }

  if (dataSources && dataSources.length > 0) {
    response += `I've also referenced the ${dataSources.length} data source(s) you mentioned. `
  }

  // Add a response based on the message content
  if (message.toLowerCase().includes("help")) {
    response += "I'm here to help! What specific assistance do you need?"
  } else if (message.toLowerCase().includes("explain")) {
    response += "Let me explain this in detail. The concept involves several key components..."
  } else if (message.toLowerCase().includes("create") || message.toLowerCase().includes("make")) {
    response += "I'd be happy to help you create that. Here's a step-by-step approach we can take..."
  } else if (message.toLowerCase().includes("analyze") || message.toLowerCase().includes("review")) {
    response += "Based on my analysis, there are several important patterns and insights to consider..."
  } else {
    response += `Regarding your question about "${message.substring(0, 30)}${message.length > 30 ? "..." : ""}", I can provide the following insights: `
    response += "The key factors to consider include context, methodology, and implementation strategy. "
    response += "Would you like me to elaborate on any specific aspect of this topic?"
  }

  return response
}

export const sendMessage = async (
  chatId: string,
  message: string,
  files?: string[],
  dataSources?: string[],
): Promise<{ message: Message; response: Message }> => {
  // Create user message
  const userMessage: Message = {
    role: "user",
    content: message,
    attachments: files,
  }

  // Generate AI response using our new function
  const responseText = await generateLLMResponse(message, files, dataSources)

  const aiResponse: Message = {
    role: "assistant",
    content: responseText,
  }

  return {
    message: userMessage,
    response: aiResponse,
  }
}

export const createNewChat = async (
  message: string,
  files?: string[],
  dataSources?: string[]
): Promise<{ chatId: string; title: string; response: string }> => {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Create a new chat ID and title
  const chatId = "2"
  const title = message.slice(0, 30) + (message.length > 30 ? "..." : "")
  
  // Generate response
  const response = await generateLLMResponse(message, files, dataSources)

  return {
    chatId,
    title,
    response,
  }
}
