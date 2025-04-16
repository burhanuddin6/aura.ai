"use client"

import type React from "react"
import { type FormEvent, useRef } from "react"
import { Button } from "@/components/ui/button"
import FileUpload from "@/components/file-upload"

interface InputAreaProps {
  input: string
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  handleSubmit: (e: FormEvent<HTMLFormElement>) => void
  isLoading: boolean
  onFileUpload?: (files: string[]) => void
  uploadedFiles?: string[]
}

export default function InputArea({
  input,
  handleInputChange,
  handleSubmit,
  isLoading,
  onFileUpload,
  uploadedFiles = [],
}: InputAreaProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = "auto"
      textarea.style.height = `${Math.min(textarea.scrollHeight, 200)}px`
    }
  }

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    handleInputChange(e)
    adjustTextareaHeight()
  }

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    handleSubmit(e)
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
    }
  }

  return (
    <div className="p-4 relative">
      <form onSubmit={onSubmit} className="max-w-4xl mx-auto">
        <div className="relative rounded-2xl border bg-white shadow-sm">
          <div className="flex items-end p-2">
            <div className="flex items-center">
              <FileUpload onFileUpload={onFileUpload} uploadedFiles={uploadedFiles} />
            </div>

            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleTextareaChange}
              placeholder="Message Aura..."
              className="flex-1 border-0 bg-transparent resize-none max-h-[200px] focus:outline-none py-2 px-3"
              rows={1}
              disabled={isLoading}
            />

            <Button
              type="submit"
              size="icon"
              className="h-8 w-8 rounded-full"
              disabled={isLoading || !input.trim()}
              variant={input.trim() ? "default" : "ghost"}
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                  d="M22 2L11 13"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M22 2L15 22L11 13L2 9L22 2Z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </Button>
          </div>
        </div>
      </form>
    </div>
  )
}
