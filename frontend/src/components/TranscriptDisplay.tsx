
import React from 'react';
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from '@/lib/utils';

export interface Message {
  id: string;
  sender: 'Agent Alpha' | 'Agent Beta' | 'Judge' | 'System';
  text: string;
  timestamp: string;
}

interface TranscriptDisplayProps {
  messages: Message[];
}

const TranscriptDisplay: React.FC<TranscriptDisplayProps> = ({ messages }) => {
  const getSenderStyles = (sender: Message['sender']) => {
    switch (sender) {
      case 'Agent Alpha':
        return 'bg-agent-a/20 text-agent-a border-agent-a self-start rounded-r-lg rounded-bl-lg';
      case 'Agent Beta':
        return 'bg-agent-b/20 text-agent-b border-agent-b self-end rounded-l-lg rounded-br-lg';
      case 'Judge':
        return 'bg-judge/20 text-judge border-judge self-center my-2 text-center italic rounded-lg';
      case 'System':
        return 'bg-muted/50 text-muted-foreground self-center my-2 text-xs italic rounded-md';
      default:
        return 'bg-card text-card-foreground';
    }
  };

  return (
    <ScrollArea className="h-[400px] lg:h-[500px] w-full bg-card border border-border rounded-lg p-4 shadow-inner">
      <div className="flex flex-col space-y-4">
        {messages.map((msg, index) => (
          <div
            key={msg.id}
            className={cn(
              "p-3 border max-w-[75%] animate-fade-in",
              getSenderStyles(msg.sender),
              {"opacity-0": true} // Initial state for animation
            )}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <p className="font-semibold text-sm mb-1">
              {msg.sender}
              <span className="ml-2 text-xs text-muted-foreground font-normal">({msg.timestamp})</span>
            </p>
            <p className="text-base whitespace-pre-wrap">{msg.text}</p>
          </div>
        ))}
        {messages.length === 0 && (
          <p className="text-center text-muted-foreground">The debate will begin shortly...</p>
        )}
      </div>
    </ScrollArea>
  );
};

export default TranscriptDisplay;
