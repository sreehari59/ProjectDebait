
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Gavel } from 'lucide-react';

interface JudgePulpitProps {
  judgeName: string;
  avatarUrl?: string;
}

const JudgePulpit: React.FC<JudgePulpitProps> = ({ judgeName, avatarUrl }) => {
  return (
    <Card className="w-full bg-judge/10 border-judge border-2 rounded-lg shadow-xl">
      <CardHeader className="flex flex-row items-center space-x-4 p-4">
         {avatarUrl ? (
          <img src={avatarUrl} alt={judgeName} className="w-16 h-16 rounded-full border-2 border-muted" />
        ) : (
          <div className="w-16 h-16 rounded-full flex items-center justify-center bg-judge text-judge-foreground">
            <Gavel size={32} />
          </div>
        )}
        <div>
          <CardTitle className="text-2xl font-orbitron text-judge">{judgeName}</CardTitle>
          <p className="text-sm text-muted-foreground">Presiding Judge</p>
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <p className="text-sm text-judge-foreground">Overseeing the debate impartially.</p>
      </CardContent>
    </Card>
  );
};

export default JudgePulpit;
