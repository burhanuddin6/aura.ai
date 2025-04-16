"use client"

import { Check, ChevronsUpDown } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { useState } from "react"

const models = [
  {
    value: "aura-flash",
    label: "Aura",
    version: "2.0 Flash",
    description: "Fast responses, good for everyday tasks",
  },
  {
    value: "aura-pro",
    label: "Aura Pro",
    version: "1.5",
    description: "Balanced performance and quality",
  },
  {
    value: "aura-ultra",
    label: "Aura Ultra",
    version: "1.0",
    description: "Highest quality, best for complex tasks",
  },
]

interface ModelSelectorProps {
  onModelChange: (model: string) => void
}

export function ModelSelector({ onModelChange }: ModelSelectorProps) {
  const [open, setOpen] = useState(false)
  const [selectedModel, setSelectedModel] = useState(models[0])

  const handleSelect = (model: (typeof models)[0]) => {
    setSelectedModel(model)
    setOpen(false)
    onModelChange(model.label)
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="ghost" role="combobox" aria-expanded={open} className="justify-between gap-1 px-2 font-medium">
          <span className="text-xl">{selectedModel.label}</span>
          <ChevronsUpDown className="ml-1 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[250px] p-0">
        <Command>
          <CommandInput placeholder="Search models..." />
          <CommandList>
            <CommandEmpty>No model found.</CommandEmpty>
            <CommandGroup>
              {models.map((model) => (
                <CommandItem
                  key={model.value}
                  value={model.value}
                  onSelect={() => handleSelect(model)}
                  className="py-2"
                >
                  <div className="flex flex-col items-start">
                    <div className="flex items-center">
                      <Check
                        className={cn(
                          "mr-2 h-4 w-4",
                          selectedModel.value === model.value ? "opacity-100" : "opacity-0",
                        )}
                      />
                      <span className="font-medium">{model.label}</span>
                    </div>
                    <div className="ml-6 flex flex-col">
                      <span className="text-xs text-gray-500">{model.version}</span>
                      <span className="text-xs text-gray-500">{model.description}</span>
                    </div>
                  </div>
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
