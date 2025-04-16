"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { ImageIcon, FileText, Upload, X } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"

interface FileUploadProps {
  onFileUpload?: (files: string[]) => void
  uploadedFiles?: string[]
}

export default function FileUpload({ onFileUpload, uploadedFiles = [] }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadType, setUploadType] = useState<"image" | "document">("document")
  const [isOpen, setIsOpen] = useState(false)
  const [localFiles, setLocalFiles] = useState<string[]>([])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleUpload = () => {
    if (!selectedFile) return

    // Add the file to our local state
    const newFiles = [...localFiles, selectedFile.name]
    setLocalFiles(newFiles)

    // Notify parent component
    if (onFileUpload) {
      onFileUpload(newFiles)
    }

    // Reset the selected file
    setSelectedFile(null)
  }

  const handleRemoveFile = (fileToRemove: string) => {
    const newFiles = localFiles.filter((file) => file !== fileToRemove)
    setLocalFiles(newFiles)

    // Notify parent component
    if (onFileUpload) {
      onFileUpload(newFiles)
    }
  }

  // Use uploaded files from props if provided
  const filesToDisplay = uploadedFiles.length > 0 ? uploadedFiles : localFiles

  return (
    <div>
      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogTrigger asChild>
          <Button variant="outline" size="sm" className="gap-2">
            <Upload className="h-4 w-4" />
            <span>Upload</span>
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Upload file</DialogTitle>
            <DialogDescription>Upload an image or document to include in your conversation.</DialogDescription>
          </DialogHeader>

          <Tabs
            defaultValue="document"
            className="w-full"
            onValueChange={(value) => setUploadType(value as "image" | "document")}
          >
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="image">Image</TabsTrigger>
              <TabsTrigger value="document">Document</TabsTrigger>
            </TabsList>

            <TabsContent value="image" className="py-4">
              <div className="space-y-4">
                <div className="flex flex-col gap-2">
                  <Label htmlFor="image-upload">Select image</Label>
                  <Input
                    id="image-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="cursor-pointer"
                  />
                </div>

                {selectedFile && (
                  <div className="rounded-md border p-2">
                    <p className="text-sm font-medium">Selected file:</p>
                    <p className="text-sm text-gray-500">{selectedFile.name}</p>
                  </div>
                )}

                <div className="flex justify-end">
                  <Button onClick={handleUpload} disabled={!selectedFile}>
                    <ImageIcon className="mr-2 h-4 w-4" />
                    Upload Image
                  </Button>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="document" className="py-4">
              <div className="space-y-4">
                <div className="flex flex-col gap-2">
                  <Label htmlFor="document-upload">Select document</Label>
                  <Input
                    id="document-upload"
                    type="file"
                    accept=".pdf,.doc,.docx,.txt,.md"
                    onChange={handleFileChange}
                    className="cursor-pointer"
                  />
                </div>

                {selectedFile && (
                  <div className="rounded-md border p-2">
                    <p className="text-sm font-medium">Selected file:</p>
                    <p className="text-sm text-gray-500">{selectedFile.name}</p>
                  </div>
                )}

                <div className="flex justify-end">
                  <Button onClick={handleUpload} disabled={!selectedFile}>
                    <FileText className="mr-2 h-4 w-4" />
                    Upload Document
                  </Button>
                </div>
              </div>
            </TabsContent>
          </Tabs>

          {/* Display uploaded files */}
          {filesToDisplay.length > 0 && (
            <div className="border-t pt-4 mt-2">
              <p className="text-sm font-medium mb-2">Uploaded files:</p>
              <div className="flex flex-wrap gap-2">
                {filesToDisplay.map((file, index) => (
                  <Badge key={index} variant="secondary" className="flex items-center gap-1">
                    <FileText className="h-3 w-3" />
                    <span className="truncate max-w-[150px]">{file}</span>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-4 w-4 p-0 ml-1"
                      onClick={() => handleRemoveFile(file)}
                    >
                      <X className="h-3 w-3" />
                    </Button>
                  </Badge>
                ))}
              </div>
            </div>
          )}

          <div className="flex justify-end gap-2 mt-4">
            <Button variant="outline" onClick={() => setIsOpen(false)}>
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Display uploaded files in the input area */}
      {filesToDisplay.length > 0 && (
        <div className="flex flex-wrap gap-1 ml-2">
          {filesToDisplay.map((file, index) => (
            <Badge key={index} variant="outline" className="flex items-center gap-1 text-xs">
              <FileText className="h-3 w-3" />
              <span className="truncate max-w-[100px]">{file}</span>
              <Button variant="ghost" size="sm" className="h-4 w-4 p-0 ml-1" onClick={() => handleRemoveFile(file)}>
                <X className="h-3 w-3" />
              </Button>
            </Badge>
          ))}
        </div>
      )}
    </div>
  )
}
