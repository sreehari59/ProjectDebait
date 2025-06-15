import React, { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Mic, MicOff, Gavel, ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";

const AiChat = () => {
  const [isListening, setIsListening] = useState(false);
  const [isAgentSpeaking, setIsAgentSpeaking] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);

  const handleMicToggle = () => {
    setIsListening(!isListening);
    // TODO: Implement actual microphone functionality
    console.log("Microphone toggled:", !isListening);
  };

  const handleJudgeVerdict = () => {
    // TODO: Implement judge verdict request
    console.log("Judge verdict requested");
  };

  // Simulate agent speaking animation
  useEffect(() => {
    if (isListening) {
      const interval = setInterval(() => {
        setIsAgentSpeaking((prev) => !prev);
      }, 2000);
      return () => clearInterval(interval);
    }
  }, [isListening]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-background to-secondary/20 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Link
            to="/"
            className="flex items-center space-x-2 text-primary hover:text-primary/80 transition-colors"
          >
            <ArrowLeft size={20} />
            <span>Back to Debate</span>
          </Link>
          <h1 className="text-3xl font-orbitron font-bold text-primary">
            Interactive Debate
          </h1>
          <div></div>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Video Frame */}
          <Card className="bg-card/50 backdrop-blur-sm border-2 border-primary/20">
            <CardHeader>
              <CardTitle className="text-xl font-orbitron text-center">
                AI Agent
              </CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <div className="relative h-[600px] bg-gradient-to-br from-primary/10 to-accent/20 rounded-lg overflow-hidden border-2 border-primary/30">
                {/* Agent Video iframe */}
                <iframe
                  // src="https://bey.chat/defaultAgent"
                  src="https://bey.chat/2862f4c4-3ecf-4c6e-8b32-70dff029dc0a"
                  allow="camera; microphone"
                  allowFullScreen
                  className="absolute inset-0 w-full h-full border-0"
                />

                {/* Speaking indicator */}
                {isAgentSpeaking && (
                  <div className="absolute bottom-4 left-4 flex space-x-1">
                    <div className="w-3 h-3 bg-primary rounded-full animate-bounce"></div>
                    <div
                      className="w-3 h-3 bg-primary rounded-full animate-bounce"
                      style={{ animationDelay: "0.1s" }}
                    ></div>
                    <div
                      className="w-3 h-3 bg-primary rounded-full animate-bounce"
                      style={{ animationDelay: "0.2s" }}
                    ></div>
                  </div>
                )}

                {/* Status indicator */}
                <div className="absolute top-4 right-4">
                  <div
                    className={`w-3 h-3 rounded-full ${isListening ? "bg-green-500" : "bg-gray-400"}`}
                  ></div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Controls */}
          <div className="space-y-6">
            {/* Judge Verdict Button */}
            <Card className="bg-judge/10 border-2 border-judge/30">
              <CardHeader>
                <CardTitle className="text-lg font-orbitron text-judge">
                  Request Judgment
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={handleJudgeVerdict}
                  size="lg"
                  className="w-full h-16 bg-judge hover:bg-judge/90 text-judge-foreground"
                >
                  <Gavel className="mr-2" size={24} />
                  Ask for a Judge Verdict
                </Button>
                <p className="text-sm text-muted-foreground text-center mt-3">
                  Request the judge to provide a verdict on your discussion
                </p>
              </CardContent>
            </Card>

            {/* Status Information */}
            <Card className="bg-card/50 backdrop-blur-sm border-2 border-primary/20">
              <CardHeader>
                <CardTitle className="text-lg font-orbitron">
                  Session Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Connection:</span>
                    <span className="text-green-600 font-medium">
                      Connected
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Microphone:</span>
                    <span
                      className={
                        isListening
                          ? "text-green-600 font-medium"
                          : "text-gray-500"
                      }
                    >
                      {isListening ? "Active" : "Inactive"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Agent Status:</span>
                    <span
                      className={
                        isAgentSpeaking
                          ? "text-blue-600 font-medium"
                          : "text-gray-500"
                      }
                    >
                      {isAgentSpeaking ? "Speaking" : "Listening"}
                    </span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AiChat;
