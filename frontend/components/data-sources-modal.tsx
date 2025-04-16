"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { FileText, Link, Plus, Upload } from "lucide-react"

export default function DataSourcesModal() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [url, setUrl] = useState("")
  const [urls, setUrls] = useState<string[]>([])
  const [isOpen, setIsOpen] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0])
    }
  }

  const handleAddUrl = () => {
    if (url.trim() && isValidUrl(url)) {
      setUrls([...urls, url])
      setUrl("")
    }
  }

  const handleRemoveUrl = (indexToRemove: number) => {
    setUrls(urls.filter((_, index) => index !== indexToRemove))
  }

  const isValidUrl = (string: string) => {
    try {
      new URL(string)
      return true
    } catch (_) {
      return false
    }
  }

  const handleUploadFile = () => {
    if (selectedFile) {
      console.log("Uploading file:", selectedFile)
      // Here you would handle the actual file upload
      setSelectedFile(null)
    }
  }

  const handleAddSources = () => {
    console.log("Adding sources:", { file: selectedFile, urls })
    // Here you would handle adding all sources
    setIsOpen(false)
    setSelectedFile(null)
    setUrls([])
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline" className="w-full justify-start gap-2 rounded-full bg-white mt-2">
          <Plus className="h-4 w-4" />
          Add data sources
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Add Data Sources</DialogTitle>
          <DialogDescription>
            Upload documents or add URLs to documentation that Aura can reference when answering your questions.
          </DialogDescription>
        </DialogHeader>

        <Tabs defaultValue="file" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="file">Upload File</TabsTrigger>
            <TabsTrigger value="url">Add URL</TabsTrigger>
          </TabsList>

          <TabsContent value="file" className="py-4">
            <div className="space-y-4">
              <div className="flex flex-col gap-2">
                <Label htmlFor="file-upload">Upload document</Label>
                <Input
                  id="file-upload"
                  type="file"
                  accept=".pdf,.doc,.docx,.txt,.md"
                  onChange={handleFileChange}
                  className="cursor-pointer"
                />
                <p className="text-xs text-gray-500">Supported formats: PDF, Word, Text, and Markdown files</p>
              </div>

              {selectedFile && (
                <div className="rounded-md border p-3 bg-gray-50">
                  <div className="flex items-center gap-2">
                    <FileText className="h-5 w-5 text-blue-500" />
                    <div className="flex-1">
                      <p className="text-sm font-medium">{selectedFile.name}</p>
                      <p className="text-xs text-gray-500">{(selectedFile.size / 1024).toFixed(1)} KB</p>
                    </div>
                    <Button variant="ghost" size="sm" onClick={() => setSelectedFile(null)} className="h-8 w-8 p-0">
                      &times;
                    </Button>
                  </div>
                </div>
              )}

              <div className="flex justify-end">
                <Button onClick={handleUploadFile} disabled={!selectedFile}>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload Document
                </Button>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="url" className="py-4">
            <div className="space-y-4">
              <div className="flex flex-col gap-2">
                <Label htmlFor="url-input">Add documentation URL</Label>
                <div className="flex gap-2">
                  <Input
                    id="url-input"
                    type="url"
                    placeholder="https://docs.example.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                  />
                  <Button onClick={handleAddUrl} disabled={!url.trim() || !isValidUrl(url)}>
                    Add
                  </Button>
                </div>
                <p className="text-xs text-gray-500">
                  Add URLs to documentation websites, GitHub repositories, or knowledge bases
                </p>
              </div>

              {urls.length > 0 && (
                <div className="rounded-md border p-3 bg-gray-50">
                  <p className="text-sm font-medium mb-2">Added URLs:</p>
                  <ul className="space-y-2">
                    {urls.map((url, index) => (
                      <li key={index} className="flex items-center gap-2">
                        <Link className="h-4 w-4 text-blue-500 shrink-0" />
                        <span className="text-sm truncate flex-1">{url}</span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRemoveUrl(index)}
                          className="h-6 w-6 p-0"
                        >
                          &times;
                        </Button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex justify-end gap-2 mt-4">
          <Button variant="outline" onClick={() => setIsOpen(false)}>
            Cancel
          </Button>
          <Button onClick={handleAddSources}>Add Sources</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
