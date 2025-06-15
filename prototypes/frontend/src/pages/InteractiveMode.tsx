import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import AgentCard from '@/components/AgentCard';
import TranscriptDisplay, { Message } from '@/components/TranscriptDisplay';
import { MessageCircle, Scale } from 'lucide-react';

const InteractiveMode = () => {
  const [messages, setMessages] = useState<Message[]>([
    { 
      id: 'sys1', 
      sender: 'System', 
      text: 'Interactive mode initialized. You can start your conversation with the AI agent.', 
      timestamp: new Date().toLocaleTimeString() 
    }
  ]);
  const [isListening, setIsListening] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  const handleStartConversation = async () => {
    setIsListening(true);
    // Here we would integrate with the microphone and speech recognition
    // For now, just adding a placeholder message
    setMessages(prev => [...prev, {
      id: `user-${Date.now()}`,
      sender: 'User',
      text: 'Microphone access would be requested here',
      timestamp: new Date().toLocaleTimeString()
    }]);
  };

  const handleAskForVerdict = async () => {
    try {
      // Here we would make an API call to get the judge's verdict
      const verdictMessage = {
        id: `verdict-${Date.now()}`,
        sender: 'Judge',
        text: 'Based on the conversation, here is my verdict...',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, verdictMessage]);
    } catch (error) {
      console.error('Failed to get verdict:', error);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-4 lg:p-8 flex flex-col">
      <header className="text-center mb-8">
        <h1 className="text-4xl font-orbitron font-bold text-primary">
          Interactive Mode
        </h1>
        <p className="text-muted-foreground mt-2">
          Have a conversation with our AI Agent
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="lg:col-span-1">
          {/* Video frame placeholder */}
          <div className="aspect-video bg-black/10 rounded-lg overflow-hidden mb-4 flex items-center justify-center">
            <AgentCard
              agentName="Interactive Agent"
              agentType="A"
              isActive={isListening}
              avatarUrl="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3"
            />
          </div>
          
          <div className="flex gap-4 justify-center">
            <Button 
              onClick={handleStartConversation}
              size="lg"
              className={`${isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-primary hover:bg-primary/90'}`}
            >
              <MessageCircle className="mr-2 h-5 w-5" />
              {isListening ? 'Stop Speaking' : 'Start Speaking'}
            </Button>
            
            <Button 
              onClick={handleAskForVerdict}
              size="lg"
              variant="secondary"
            >
              <Scale className="mr-2 h-5 w-5" />
              Ask for Verdict
            </Button>
          </div>
        </div>

        <div className="lg:col-span-1">
          <TranscriptDisplay messages={messages} />
        </div>
      </div>

      <audio ref={audioRef} style={{ display: 'none' }} />
    </div>
  );
};

export default InteractiveMode;