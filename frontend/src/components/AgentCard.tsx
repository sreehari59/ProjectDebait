
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { User, Cpu } from 'lucide-react'; // Using Cpu for AI agent

interface AgentCardProps {
  agentName: string;
  agentType: 'A' | 'B';
  avatarUrl?: string; // For future use with actual avatars
  isActive?: boolean;
}

const AgentCard: React.FC<AgentCardProps> = ({ agentName, agentType, avatarUrl, isActive }) => {
  const bgColor = agentType === 'A' ? 'bg-agent-a/10' : 'bg-agent-b/10';
  const borderColor = agentType === 'A' ? 'border-agent-a' : 'border-agent-b';
  const textColor = agentType === 'A' ? 'text-agent-a' : 'text-agent-b';
  const activeRing = isActive ? (agentType === 'A' ? 'ring-2 ring-agent-a ring-offset-2 ring-offset-background' : 'ring-2 ring-agent-b ring-offset-2 ring-offset-background') : '';

  return (
    <Card className={`w-full ${bgColor} ${borderColor} border-2 rounded-lg shadow-xl transition-all duration-300 ${activeRing} ${isActive ? 'scale-105' : ''}`}>
      <CardHeader className="flex flex-row items-center space-x-4 p-4">
        {avatarUrl ? (
          <img src={avatarUrl} alt={agentName} className="w-16 h-16 rounded-full border-2 border-muted" />
        ) : (
          <div className={`w-16 h-16 rounded-full flex items-center justify-center ${agentType === 'A' ? 'bg-agent-a' : 'bg-agent-b'} text-background`}>
            <Cpu size={32} />
          </div>
        )}
        <div>
          <CardTitle className={`text-2xl font-orbitron ${textColor}`}>{agentName}</CardTitle>
          <p className="text-sm text-muted-foreground">Debating Agent</p>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        {isActive && (
          <div className="flex items-center space-x-2 text-sm animate-pulse-glow">
             <div className={`w-3 h-3 rounded-full ${agentType === 'A' ? 'bg-agent-a' : 'bg-agent-b'}`}></div>
            <span className={`${textColor}`}>Active</span>
          </div>
        )}
        {!isActive && <p className="text-sm text-muted-foreground">Waiting...</p>}
      </CardContent>
    </Card>
  );
};

export default AgentCard;
