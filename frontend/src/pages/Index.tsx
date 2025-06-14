
import React, { useState, useEffect } from 'react';
import AgentCard from '@/components/AgentCard';
import JudgePulpit from '@/components/JudgePulpit';
import TranscriptDisplay, { Message } from '@/components/TranscriptDisplay';
import { Button } from '@/components/ui/button';
import { PlayCircle, PauseCircle, RefreshCw } from 'lucide-react';

const initialMessages: Message[] = [
  { id: 'sys1', sender: 'System', text: 'Debate arena initializing...', timestamp: new Date().toLocaleTimeString() },
];

const sampleDebateFlow: Array<Omit<Message, 'id' | 'timestamp'>> = [
  { sender: 'System', text: 'The debate topic is: "Is pineapple a valid pizza topping?"' },
  { sender: 'Agent A', text: "Greetings. I will argue that pineapple, with its sweet and tangy profile, offers a delightful contrast to savory pizza ingredients, thus making it a valid and enjoyable topping." },
  { sender: 'Agent B', text: "I respectfully disagree. The acidity and texture of pineapple clash with the traditional flavors of pizza, creating an incongruous culinary experience. It has no place on a pizza." },
  { sender: 'Judge', text: "Interesting opening statements. Agent A, please elaborate on your position." },
  { sender: 'Agent A', text: "Certainly, Judge. The combination of sweet and savory is a well-established culinary principle. Think of salted caramel or honey-glazed ham. Pineapple on pizza, particularly with ingredients like ham or spicy pepperoni, provides this very balance, enhancing the overall flavor complexity." },
  { sender: 'Agent B', text: "While sweet and savory can coexist, the specific application matters. Pineapple's high water content can make the pizza soggy, and its dominant flavor often overpowers more subtle ingredients. A pizza should be a harmonious blend, not a battle of strong flavors." },
  { sender: 'Judge', text: "Both valid points. Let's pause here for initial thoughts. The debate will continue." },
];

const Index = () => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [isDebateRunning, setIsDebateRunning] = useState(false);
  const [activeAgent, setActiveAgent] = useState<'A' | 'B' | null>(null);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isDebateRunning && currentMessageIndex < sampleDebateFlow.length) {
      timer = setTimeout(() => {
        const nextMessage = sampleDebateFlow[currentMessageIndex];
        setMessages(prev => [...prev, { ...nextMessage, id: `msg${prev.length}`, timestamp: new Date().toLocaleTimeString() }]);
        
        if (nextMessage.sender === 'Agent A') setActiveAgent('A');
        else if (nextMessage.sender === 'Agent B') setActiveAgent('B');
        else setActiveAgent(null);

        setCurrentMessageIndex(prev => prev + 1);
      }, 2000 + Math.random() * 2000); // Simulate thinking time
    } else if (currentMessageIndex >= sampleDebateFlow.length) {
      setIsDebateRunning(false);
      setActiveAgent(null);
    }
    return () => clearTimeout(timer);
  }, [isDebateRunning, currentMessageIndex]);

  const startDebate = () => {
    if (messages.length <= 1 || currentMessageIndex >= sampleDebateFlow.length) { // Reset if at start or end
      setMessages([
        { id: 'sys-restart', sender: 'System', text: 'Debate restarting...', timestamp: new Date().toLocaleTimeString() }
      ]);
      setCurrentMessageIndex(0);
    }
    setIsDebateRunning(true);
  };

  const pauseDebate = () => {
    setIsDebateRunning(false);
  };
  
  const resetDebate = () => {
    setIsDebateRunning(false);
    setMessages(initialMessages);
    setCurrentMessageIndex(0);
    setActiveAgent(null);
  }

  return (
    <div className="min-h-screen bg-background text-foreground p-4 lg:p-8 flex flex-col font-sans">
      <header className="text-center mb-8">
        <h1 className="text-5xl lg:text-6xl font-orbitron font-bold text-primary animate-fade-in" style={{animationDelay: '0s'}}>
          Project <span className="text-agent-a">De</span><span className="text-agent-b">ba</span><span className="text-judge">te</span>
        </h1>
        <p className="text-muted-foreground text-lg mt-2 animate-fade-in" style={{animationDelay: '0.2s'}}>
          AI Agents Battle for Intellectual Supremacy
        </p>
      </header>

      <div className="mb-6 text-center animate-fade-in" style={{animationDelay: '0.4s'}}>
        <h2 className="text-2xl font-orbitron text-judge">Debate Topic</h2>
        <p className="text-xl text-foreground mt-1">
          {currentMessageIndex > 0 && sampleDebateFlow[0].sender === 'System' ? sampleDebateFlow[0].text.replace('The debate topic is: ','') : "Is pineapple a valid pizza topping?"}
        </p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 flex-grow items-start">
        <div className="animate-fade-in" style={{animationDelay: '0.6s'}}>
          <AgentCard agentName="Agent Alpha" agentType="A" isActive={activeAgent === 'A'} avatarUrl="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YWl8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=100&q=60" />
        </div>

        <div className="lg:col-span-1 order-first lg:order-none animate-fade-in" style={{animationDelay: '0.8s'}}>
          <JudgePulpit judgeName="Judge Omega" avatarUrl="https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=100&q=60" />
        </div>
        
        <div className="animate-fade-in" style={{animationDelay: '1s'}}>
          <AgentCard agentName="Agent Beta" agentType="B" isActive={activeAgent === 'B'} avatarUrl="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29kZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=100&q=60" />
        </div>
      </div>

      <div className="mb-6 animate-fade-in" style={{animationDelay: '1.2s'}}>
        <TranscriptDisplay messages={messages} />
      </div>

      <footer className="mt-auto text-center space-x-4 py-4 animate-fade-in" style={{animationDelay: '1.4s'}}>
        {!isDebateRunning ? (
          <Button onClick={startDebate} size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground">
            <PlayCircle className="mr-2 h-5 w-5" />
            {currentMessageIndex >= sampleDebateFlow.length ? "Restart Debate" : "Start Debate"}
          </Button>
        ) : (
          <Button onClick={pauseDebate} size="lg" variant="secondary">
            <PauseCircle className="mr-2 h-5 w-5" />
            Pause Debate
          </Button>
        )}
         <Button onClick={resetDebate} size="lg" variant="outline" className="border-destructive text-destructive hover:bg-destructive/10 hover:text-destructive">
            <RefreshCw className="mr-2 h-5 w-5" />
            Reset
          </Button>
      </footer>
    </div>
  );
};

export default Index;

