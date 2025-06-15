
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { MessageSquare } from 'lucide-react';
import AgentCard from '@/components/AgentCard';
import JudgePulpit from '@/components/JudgePulpit';
import TranscriptDisplay, { Message } from '@/components/TranscriptDisplay';

const Index = () => {
  const [messages] = useState<Message[]>([
    {
      id: '1',
      sender: 'System',
      text: 'Debate session initialized. Agents are ready.',
      timestamp: '10:00:00'
    },
    {
      id: '2',
      sender: 'Agent A',
      text: 'I believe artificial intelligence will fundamentally improve human society by automating routine tasks and enabling us to focus on creative and meaningful work.',
      timestamp: '10:00:15'
    },
    {
      id: '3',
      sender: 'Agent B',
      text: 'While AI has benefits, we must consider the risks of job displacement and the potential loss of human agency. The transition may cause more harm than good in the short term.',
      timestamp: '10:00:45'
    },
    {
      id: '4',
      sender: 'Judge',
      text: 'Both arguments have merit. Agent A, please elaborate on how society will handle the transition period.',
      timestamp: '10:01:20'
    }
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20 p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-orbitron font-bold text-primary mb-4">
            AI Debate Platform
          </h1>
          <p className="text-lg text-muted-foreground mb-6">
            Watch intelligent agents engage in structured debates
          </p>
          
          {/* Navigation */}
          <div className="flex justify-center mb-8">
            <Link to="/ai-chat">
              <Button size="lg" className="bg-primary hover:bg-primary/90">
                <MessageSquare className="mr-2" size={20} />
                Chat with AI Agent
              </Button>
            </Link>
          </div>
        </div>

        {/* Judge Section */}
        <div className="mb-8 flex justify-center">
          <div className="w-full max-w-md">
            <JudgePulpit judgeName="AI Judge Alpha" />
          </div>
        </div>

        {/* Main Content */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Agent A */}
          <div className="space-y-4">
            <AgentCard 
              agentName="Agent Logos" 
              agentType="A" 
              isActive={false}
            />
          </div>

          {/* Center - Transcript */}
          <div className="lg:col-span-1">
            <Card className="bg-card/50 backdrop-blur-sm border-2 border-primary/20 shadow-xl">
              <CardHeader>
                <CardTitle className="text-xl font-orbitron text-center">Live Transcript</CardTitle>
              </CardHeader>
              <CardContent>
                <TranscriptDisplay messages={messages} />
              </CardContent>
            </Card>
          </div>

          {/* Agent B */}
          <div className="space-y-4">
            <AgentCard 
              agentName="Agent Ethos" 
              agentType="B" 
              isActive={true}
            />
          </div>
        </div>

        {/* Controls Section */}
        <div className="mt-8 flex justify-center space-x-4">
          <Button variant="outline" size="lg">
            Start Debate
          </Button>
          <Button variant="outline" size="lg">
            Pause
          </Button>
          <Button variant="outline" size="lg">
            Reset
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Index;
