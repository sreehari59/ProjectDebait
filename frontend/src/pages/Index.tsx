import React, { useState, useEffect, useRef } from "react";
import AgentCard from "@/components/AgentCard";
import JudgePulpit from "@/components/JudgePulpit";
import TranscriptDisplay, { Message } from "@/components/TranscriptDisplay";
import { Button } from "@/components/ui/button";
import { PlayCircle, PauseCircle, RefreshCw } from "lucide-react";
import { Link } from "react-router-dom";

const initialMessages: Message[] = [
  {
    id: "sys1",
    sender: "System",
    text: "Debate arena initializing...",
    timestamp: new Date().toLocaleTimeString(),
  },
];

// Default debate configuration
const defaultDebateConfig = {
  topic: "Is artificial intelligence beneficial for society?",
  side_a_point: "AI brings significant benefits and advancement to society",
  side_b_point: "AI poses serious risks and challenges to society",
  rounds: 2,
};

const Index = () => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isDebateRunning, setIsDebateRunning] = useState(false);
  const [activeAgent, setActiveAgent] = useState<"A" | "B" | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);
  const [debateMessages, setDebateMessages] = useState<string[]>([]);
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  useEffect(() => {
    let isPlaying = true;

    const playNextMessage = async () => {
      if (
        !isDebateRunning ||
        currentMessageIndex >= debateMessages.length ||
        !isPlaying
      ) {
        setIsDebateRunning(false);
        setActiveAgent(null);
        return;
      }

      const message = debateMessages[currentMessageIndex];
      const sender = message.startsWith("side_a:")
        ? "Agent A"
        : message.startsWith("side_b:")
          ? "Agent B"
          : message.startsWith("VERDICT:")
            ? "Judge"
            : "System";

      setMessages((prev) => [
        ...prev,
        {
          id: `msg${prev.length}`,
          sender,
          text: message.replace(/^(side_a:|side_b:|VERDICT:)\s*/, ""),
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);

      setActiveAgent(
        sender === "Agent A" ? "A" : sender === "Agent B" ? "B" : null,
      );

      if (audioRef.current) {
        audioRef.current.src = `http://localhost:5000/stream_message?message=${encodeURIComponent(message)}`;
        await audioRef.current.play();
        audioRef.current.onended = () => {
          setCurrentMessageIndex((prev) => prev + 1);
        };
      }
    };

    if (isDebateRunning) {
      playNextMessage();
    }

    return () => {
      isPlaying = false;
      if (audioRef.current) {
        audioRef.current.pause();
      }
    };
  }, [isDebateRunning, currentMessageIndex, debateMessages]);

  const startDebate = async () => {
    try {
      setMessages([
        {
          id: "sys-restart",
          sender: "System",
          text: "Starting new debate...",
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);

      const params = new URLSearchParams({
        ...defaultDebateConfig,
      });

      const response = await fetch(
        `http://localhost:5000/start_debate?${params}`,
      );
      const data = await response.json();

      setDebateMessages(data.messages);
      setCurrentMessageIndex(0);
      setIsDebateRunning(true);
    } catch (error) {
      console.error("Failed to start debate:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: `error-${Date.now()}`,
          sender: "System",
          text: "Failed to start debate. Please try again.",
          timestamp: new Date().toLocaleTimeString(),
        },
      ]);
    }
  };

  const pauseDebate = () => {
    setIsDebateRunning(false);
  };

  const resetDebate = () => {
    setIsDebateRunning(false);
    setMessages(initialMessages);
    setCurrentMessageIndex(0);
    setActiveAgent(null);
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-4 lg:p-8 flex flex-col font-sans">
      <header className="text-center mb-8">
        <h1
          className="text-5xl lg:text-6xl font-orbitron font-bold text-primary animate-fade-in"
          style={{ animationDelay: "0s" }}
        >
          Project <span className="text-agent-a">De</span>
          <span className="text-agent-b">ba</span>
          <span className="text-judge">it</span>
        </h1>
        <p
          className="text-muted-foreground text-lg mt-2 animate-fade-in"
          style={{ animationDelay: "0.2s" }}
        >
          AI Agents Battle for Intellectual Supremacy
        </p>
      </header>
      {/* Navigation */}
      <div className="flex justify-center mb-8">
        <Link to="/ai-chat">
          <Button size="lg" className="bg-primary hover:bg-primary/90">
            {/* <MessageSquare className="mr-2" size={20} /> */}
            Chat with AI Agent
          </Button>
        </Link>
      </div>
      <div
        className="mb-6 text-center animate-fade-in"
        style={{ animationDelay: "0.4s" }}
      >
        <h2 className="text-2xl font-orbitron text-judge">Debate Topic</h2>
        <p className="text-xl text-foreground mt-1">
          {defaultDebateConfig.topic}
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6 flex-grow items-start">
        <div className="animate-fade-in" style={{ animationDelay: "0.6s" }}>
          <AgentCard
            agentName="Agent Alpha"
            agentType="A"
            isActive={activeAgent === "A"}
            avatarUrl="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8YWl8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=100&q=60"
          />
        </div>

        <div
          className="lg:col-span-1 order-first lg:order-none animate-fade-in"
          style={{ animationDelay: "0.8s" }}
        >
          <JudgePulpit
            judgeName="Judge Omega"
            avatarUrl="https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dGVjaHxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=100&q=60"
          />
        </div>

        <div className="animate-fade-in" style={{ animationDelay: "1s" }}>
          <AgentCard
            agentName="Agent Beta"
            agentType="B"
            isActive={activeAgent === "B"}
            avatarUrl="https://images.unsplash.com/photo-1461749280684-dccba630e2f6?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29kZXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=100&q=60"
          />
        </div>
      </div>

      <div className="mb-6 animate-fade-in" style={{ animationDelay: "1.2s" }}>
        <TranscriptDisplay messages={messages} />
      </div>

      <audio ref={audioRef} style={{ display: "none" }} />
      <footer
        className="mt-auto text-center space-x-4 py-4 animate-fade-in"
        style={{ animationDelay: "1.4s" }}
      >
        {!isDebateRunning ? (
          <Button
            onClick={startDebate}
            size="lg"
            className="bg-primary hover:bg-primary/90 text-primary-foreground"
          >
            <PlayCircle className="mr-2 h-5 w-5" />
            {currentMessageIndex >= debateMessages.length
              ? "Restart Debate"
              : "Start Debate"}
          </Button>
        ) : (
          <Button onClick={pauseDebate} size="lg" variant="secondary">
            <PauseCircle className="mr-2 h-5 w-5" />
            Pause Debate
          </Button>
        )}
        <Button
          onClick={resetDebate}
          size="lg"
          variant="outline"
          className="border-destructive text-destructive hover:bg-destructive/10 hover:text-destructive"
        >
          <RefreshCw className="mr-2 h-5 w-5" />
          Reset
        </Button>
      </footer>
    </div>
  );
};

export default Index;
