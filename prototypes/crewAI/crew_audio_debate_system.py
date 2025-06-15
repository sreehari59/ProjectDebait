#!/usr/bin/env python3
"""
CrewAI Audio Debate System with Dedicated Audio Agents
Uses specialized CrewAI agents for audio generation and playback
"""

import os
import sys
import threading
import time
import subprocess
import platform
import json
import tempfile
from datetime import datetime
from debate_system import DebatingSystem, mistral_llm
from crewai import Agent, Task, Crew
from elevenlabs.client import ElevenLabs
from elevenlabs import play

class CrewAudioDebateSystem(DebatingSystem):
    def __init__(self):
        super().__init__()
        
        # Initialize ElevenLabs client
        try:
            self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
            self.audio_enabled = True
        except:
            self.audio_enabled = False
            print("⚠️ Audio disabled - ElevenLabs not available")
        
        # Voice mapping for different roles
        self.voice_ids = {
            "Pro Debater": "21m00Tcm4TlvDq8ikWAM",  # Rachel
            "Con Debater": "awJYCdDwxfD901AaAI0b",  # Drew  
            "Debate Judge": "2EiwWnXFnvU5JabPnv8n"  # Clyde
        }
        
        # Audio storage
        self.audio_outputs = {}
        
        # Structured debate tracking
        self.conversation_history = []
        self.current_turn = 0
        self.max_turns_per_agent = 3
        
        # Threading for audio and response generation
        self.audio_threads = []
        self.response_ready = threading.Event()
        self.audio_complete = threading.Event()
        
    def create_topic_generator_agent(self):
        """Create agent to generate debate topics"""
        self.topic_generator = Agent(
            role="Debate Topic Generator",
            goal="Generate engaging, balanced debate topics that have clear pro and con sides",
            backstory="""You are an experienced debate moderator who creates thought-provoking 
            topics that inspire meaningful discussion. Your topics are clear, controversial enough 
            to have strong arguments on both sides, and relevant to current issues.""",
            llm=mistral_llm,
            verbose=True
        )
    
    def create_structured_debate_agents(self):
        """Create agents optimized for natural conversational debate"""
        
        # Pro Debater - Enhanced for natural dialogue
        self.agent_pro = Agent(
            role="Pro Debater",
            goal=f"Engage in natural conversational debate arguing FOR the topic",
            backstory="""You are a skilled conversationalist having a natural debate. 
            Speak like a real person in conversation - use 3-4 short, clear sentences. 
            Always acknowledge what your opponent just said, then make your point. 
            Be conversational and direct. Use phrases like "I hear you, but..." or "True, however..."
            Keep responses under 30 words for quick audio generation.
            
            Optional:
            Your argument should include:
            - Clear main points supporting your position backed by research and popular opinion
            - Specific statistics, case studies, and expert opinions from your research
            - Logical reasoning connecting research findings to your points
            - Address potential counterarguments using research-based rebuttals
            - Keep your argument compelling and well-evidenced
            
            """,
            llm=mistral_llm,
            verbose=False
        )
        
        # Con Debater - Enhanced for natural dialogue  
        self.agent_con = Agent(
            role="Con Debater", 
            goal=f"Engage in natural conversational debate arguing AGAINST the topic",
            backstory="""You are a skilled conversationalist having a natural debate.
            Speak like a real person in conversation - use 3-4 short, clear sentences.
            Always respond directly to what your opponent just said, then counter.
            Be conversational and direct. Use phrases like "I disagree because..." or "Actually..."
            Keep responses under 30 words for quick audio generation.
            
            Optional:
            Your argument should include:
             - Clear main points opposing the position backed by research and popular opinion
             - Logical reasoning connecting research findings to your points
             - Address and refute pro arguments using research-based evidence
             - Keep your argument compelling and well-evidenced
             - Specific statistics, case studies, and expert opinions from your research
            """,
            llm=mistral_llm,
            verbose=False
        )
        
        # Judge - Enhanced for conversational evaluation
        self.judge_agent = Agent(
            role="Debate Judge",
            goal="Evaluate the natural conversation and determine the winner",
            backstory="""You are an impartial judge who evaluates natural conversational debates. 
            You assess how well each person engaged with their opponent's points, made persuasive 
            arguments, and maintained a coherent position throughout the discussion. You value 
            natural flow, direct responses, and overall persuasiveness in conversational debate.
            Keep your evaluation concise - 2-3 sentences maximum for quick audio.""",
            llm=mistral_llm,
            verbose=False
        )
    
    def create_topic_generation_task(self):
        """Create task for generating debate topic"""
        self.task_topic = Task(
            description="""Generate an engaging debate topic that:
            - Is stated in 1-2 clear lines
            - Has strong arguments available for both pro and con sides
            - Is relevant and thought-provoking
            - Can be debated meaningfully in a structured format
            - Avoids topics that are purely factual or have obvious answers
            
            Examples of good topics:
            - "Should social media platforms be held legally responsible for content posted by users?"
            - "Is remote work better for both employees and companies than traditional office work?"
            - "Should artificial intelligence development be regulated by international law?"
            
            Format your response as: "TOPIC: [Your debate topic here]"
            """,
            expected_output="A single debate topic formatted as 'TOPIC: [topic text]'",
            agent=self.topic_generator
        )
    
    def create_turn_based_tasks(self, topic, turn_number, previous_exchange=None):
        """Create tasks for natural conversational debate turns"""
        
        # Build conversation context
        context_text = ""
        if self.conversation_history:
            context_text = "\n\nCONVERSATION SO FAR:\n"
            for i, exchange in enumerate(self.conversation_history, 1):
                context_text += f"\nExchange {i}:\n"
                context_text += f"Pro: {exchange['pro']}\n"
                context_text += f"Con: {exchange['con']}\n"
        
        # Pro Debater Task - Natural conversation style
        if turn_number == 1:
            pro_description = f"""Start the conversation by arguing FOR: {topic}
            
            This is your opening statement (Exchange 1 of 3). Speak naturally like you're having 
            a real conversation with someone. Use 1-3 short, clear sentences. Be direct and 
            engaging, not formal or academic.
            
            Example style: "I really think [topic] because [main reason]. It just makes sense when you consider [supporting point]."
            
            Keep it conversational and under 30 words.
            """
        else:
            last_con_response = self.conversation_history[-1]['con'] if self.conversation_history else ""
            pro_description = f"""Respond naturally to what your opponent just said about: {topic}
            
            This is Exchange {turn_number} of 3. Your opponent just said:
            "{last_con_response}"
            
            Respond directly to their point first, then make your own. Use 1-2 short sentences 
            like you're having a real conversation. Be natural and conversational.
            
            Example style: "I see your point about X, but here's the thing - [your counter]. Plus, [additional point]."
            
            {context_text}
            
            Keep it conversational and under 30 words.
            """
        
        self.task_pro_turn = Task(
            description=pro_description,
            expected_output="A natural, conversational response of 1-2 sentences (under 30 words)",
            agent=self.agent_pro
        )
        
        # Con Debater Task - Natural conversation style
        if turn_number == 1:
            con_description = f"""Respond naturally to the Pro debater's opening statement about: {topic}
            
            This is Exchange 1 of 3. The Pro debater just made their opening point. Respond 
            directly to what they said, then make your counter-argument. Use 1-3 short, clear 
            sentences like you're having a real conversation.
            
            The Pro debater said: "{previous_exchange if previous_exchange else 'Opening statement'}"
            
            Example style: "I disagree with that because [reason]. Actually, [your counter-point]."
            
            Keep it conversational and under 30 words.
            """
        else:
            last_pro_response = self.conversation_history[-1]['pro'] if self.conversation_history else ""
            con_description = f"""Respond naturally to what your opponent just said about: {topic}
            
            This is Exchange {turn_number} of 3. Your opponent just said:
            "{last_pro_response}"
            
            Respond directly to their point first, then make your own. Use 1-2 short sentences 
            like you're having a real conversation. Be natural and conversational.
            
            Example style: "That's not quite right because [reason]. What you're missing is [your point]."
            
            {context_text}
            
            Keep it conversational and under 30 words.
            """
        
        self.task_con_turn = Task(
            description=con_description,
            expected_output="A natural, conversational response of 1-2 sentences (under 30 words)",
            agent=self.agent_con,
            context=[self.task_pro_turn] if turn_number == 1 else []
        )
    
    def create_final_judgment_task(self):
        """Create task for evaluating the natural conversation"""
        
        # Build complete conversation history
        complete_history = "\n\nCOMPLETE CONVERSATION:\n"
        for i, exchange in enumerate(self.conversation_history, 1):
            complete_history += f"\nExchange {i}:\n"
            complete_history += f"Pro: {exchange['pro']}\n"
            complete_history += f"Con: {exchange['con']}\n"
        
        self.task_final_judgment = Task(
            description=f"""Evaluate this natural conversation about: {self.debate_topic}
            
            Judge this like a real conversation between two people. Consider:
            - How well each person responded to what the other said
            - Who made more convincing points in natural dialogue
            - Who engaged better with their opponent's arguments
            - Overall persuasiveness in conversational format
            
            {complete_history}
            
            Give a brief evaluation (3-4 sentences) and declare the winner with reasoning.
            Be conversational in your assessment.
            """,
            expected_output="A brief conversational evaluation with clear winner declaration",
            agent=self.judge_agent
        )
    
    def generate_and_play_audio(self, text, agent_role):
        """Generate and play audio with proper threading"""
        role_emoji = {
            "Pro Debater": "👤",
            "Con Debater": "👥", 
            "Debate Judge": "⚖️"
        }
        
        emoji = role_emoji.get(agent_role, "🗣️")
        print(f"{emoji} {agent_role}: {text}")
        
        if not self.audio_enabled:
            print("📝 (Text-only mode)\n")
            return
            
        try:
            print(f"🎙️ Generating audio for {agent_role}...")
            
            # Generate audio using ElevenLabs
            voice_id = self.voice_ids.get(agent_role, self.voice_ids["Pro Debater"])
            
            # Use the stream method and collect all bytes
            audio_stream = self.elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_turbo_v2"  # Faster model for real-time
            )
            
            # Convert generator to bytes if needed
            if hasattr(audio_stream, '__iter__') and not isinstance(audio_stream, (bytes, bytearray)):
                audio_bytes = b''.join(audio_stream)
            else:
                audio_bytes = audio_stream
            
            # Store audio for potential reuse
            self.audio_outputs[agent_role] = audio_bytes
            
            # Play audio in background thread
            audio_thread = threading.Thread(
                target=self.play_audio_async,
                args=(audio_bytes, agent_role)
            )
            audio_thread.daemon = True
            audio_thread.start()
            self.audio_threads.append(audio_thread)
            
        except Exception as e:
            print(f"⚠️ Audio error for {agent_role}: {e}")
            print("📝 Continuing with text-only...\n")
    
    def play_audio_async(self, audio_bytes, agent_role):
        """Play audio asynchronously without blocking the main thread"""
        try:
            print(f"🔊 Playing audio for {agent_role}...")
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, mode='wb') as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # Try platform-specific players
            playback_success = False
            
            if platform.system() == "Darwin":  # macOS
                try:
                    subprocess.run(
                        ["afplay", temp_file_path], 
                        check=True, 
                        capture_output=True, 
                        timeout=30
                    )
                    playback_success = True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
                    print(f"⚠️ afplay failed: {e}")
            
            # Fallback to ElevenLabs play
            if not playback_success:
                try:
                    play(audio_bytes)
                    playback_success = True
                except Exception as play_error:
                    print(f"⚠️ ElevenLabs play failed: {play_error}")
            
            if playback_success:
                print(f"✅ {agent_role} finished speaking\n")
            else:
                print(f"⚠️ Could not play audio for {agent_role}\n")
                
            # Clean up
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Audio playback error: {e}")
        finally:
            # Signal that audio is complete
            self.audio_complete.set()
    
    
    def play_audio(self, audio_bytes, agent_role):
        """Play audio using the best available method"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, mode='wb') as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            print(f"🔊 Playing audio for {agent_role}...")
            
            # Try platform-specific players
            playback_success = False
            
            if platform.system() == "Darwin":  # macOS
                try:
                    subprocess.run(
                        ["afplay", temp_file_path], 
                        check=True, 
                        capture_output=True, 
                        timeout=60
                    )
                    playback_success = True
                except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                    print(f"⚠️ afplay failed: {e}")
            
            # Fallback to ElevenLabs play
            if not playback_success:
                print("🔄 Using ElevenLabs play function...")
                try:
                    play(audio_bytes)
                    playback_success = True
                except Exception as play_error:
                    print(f"⚠️ ElevenLabs play failed: {play_error}")
            
            if playback_success:
                print(f"✅ {agent_role} finished speaking\n")
            else:
                print(f"⚠️ Could not play audio for {agent_role}\n")
                
            # Clean up
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
        except Exception as e:
            print(f"⚠️ Audio playback error: {e}")
    
    def execute_debate_turn(self, turn_number):
        """Execute a single exchange with concurrent audio and response generation"""
        print(f"📝 === Exchange {turn_number} ===")
        
        # Get previous exchange for context if not the first turn
        previous_exchange = None
        if turn_number == 1 and len(self.conversation_history) == 0:
            previous_exchange = None
        elif len(self.conversation_history) > 0:
            previous_exchange = self.conversation_history[-1]['pro']
        
        # Create tasks for this exchange
        self.create_turn_based_tasks(self.debate_topic, turn_number, previous_exchange)
        
        # Execute Pro argument
        print("🤖 Pro generating response...")
        pro_crew = Crew(
            agents=[self.agent_pro],
            tasks=[self.task_pro_turn],
            verbose=False
        )
        pro_crew.kickoff()
        pro_response = str(self.task_pro_turn.output).strip()
        
        # Start Pro audio generation and playback
        self.generate_and_play_audio(pro_response, "Pro Debater")
        
        # While Pro audio is playing, prepare Con's response
        # Update Pro's response in the tasks for Con to use as context
        self.create_turn_based_tasks(self.debate_topic, turn_number, pro_response)
        
        print("🤖 Con generating response...")
        con_crew = Crew(
            agents=[self.agent_con],
            tasks=[self.task_con_turn],
            verbose=False
        )
        
        # Start Con response generation while Pro audio might still be playing
        con_crew.kickoff()
        con_response = str(self.task_con_turn.output).strip()
        
        # Wait for Pro audio to finish before starting Con audio
        if self.audio_enabled and self.audio_threads:
            for thread in self.audio_threads:
                if thread.is_alive():
                    thread.join(timeout=15)  # Max 15 second wait
        
        # Start Con audio generation and playback
        self.generate_and_play_audio(con_response, "Con Debater")
        
        # Store this exchange in conversation history
        exchange = {
            "turn": turn_number,
            "pro": pro_response,
            "con": con_response,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(exchange)
        
        # Wait for Con audio to finish before next exchange
        if self.audio_enabled and self.audio_threads:
            for thread in self.audio_threads:
                if thread.is_alive():
                    thread.join(timeout=15)  # Max 15 second wait
        
        print(f"✅ Exchange {turn_number} complete\n")
        return exchange
    
    def save_debate_log(self, result, final_judgment):
        """Save debate log with complete conversation history"""
        log_data = {
            "topic": self.debate_topic,
            "timestamp": self.shared_memory["timestamp"],
            "shared_memory": self.shared_memory,
            "conversation_history": self.conversation_history,
            "final_judgment": str(final_judgment),
            "total_turns": len(self.conversation_history),
            "audio_enabled": self.audio_enabled,
            "debate_type": "structured_turn_based_debate"
        }
        
        # Ensure logs directory exists
        logs_dir = "/Users/A200303816/Documents/EuroTech-2/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"structured_debate_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
            print(f"📁 Structured debate log saved to: logs/{filename}")
        except Exception as e:
            print(f"⚠️ Could not save debate log: {e}")
    
    def run_structured_debate(self, provided_topic=None):
        """Run a natural conversational debate"""
        
        print(f"\n{'='*60}")
        print(f"💬 NATURAL CONVERSATIONAL DEBATE")
        print(f"📋 Format: 3 exchanges (6 short responses total)")
        print(f"🎙️ Real-time Audio | 🗣️ Natural dialogue style")
        print(f"{'='*60}\n")
        
        try:
            # Step 1: Generate or use provided topic
            if provided_topic:
                self.debate_topic = provided_topic
                print(f"💭 TOPIC: {self.debate_topic}\n")
            else:
                print("🎯 Generating conversation topic...")
                self.create_topic_generator_agent()
                self.create_topic_generation_task()
                
                topic_crew = Crew(
                    agents=[self.topic_generator],
                    tasks=[self.task_topic],
                    verbose=False
                )
                topic_crew.kickoff()
                
                topic_output = str(self.task_topic.output)
                # Extract topic from "TOPIC: ..." format
                if "TOPIC:" in topic_output:
                    self.debate_topic = topic_output.split("TOPIC:", 1)[1].strip()
                else:
                    self.debate_topic = topic_output.strip()
                
                print(f"💭 GENERATED TOPIC: {self.debate_topic}\n")
            
            self.shared_memory["debate_context"] = f"Natural Conversation on: {self.debate_topic}"
            
            # Step 2: Create conversation agents
            print("🤖 Preparing conversation participants...")
            self.create_structured_debate_agents()
            
            # Step 3: Have natural conversation (3 exchanges)
            print("🗣️ Starting conversation...\n")
            print("="*60)
            
            for exchange in range(1, self.max_turns_per_agent + 1):
                self.execute_debate_turn(exchange)
                
                # Brief pause between exchanges for readability
                if exchange < self.max_turns_per_agent:
                    time.sleep(1)
            
            # Step 4: Judge evaluation
            print("⚖️ === CONVERSATION EVALUATION ===")
            
            self.create_final_judgment_task()
            judge_crew = Crew(
                agents=[self.judge_agent],
                tasks=[self.task_final_judgment],
                verbose=False
            )
            judge_crew.kickoff()
            final_judgment = str(self.task_final_judgment.output)
            
            # Display judge's evaluation
            self.generate_and_play_audio(final_judgment, "Debate Judge")
            
            # Step 5: Summary
            print("="*60)
            print("✅ CONVERSATION COMPLETE!")
            print(f"📊 Total exchanges: {len(self.conversation_history)}")
            print(f"🗣️ Responses per person: {len(self.conversation_history)}")
            print("="*60)
            
            # Save conversation log
            self.save_debate_log("Natural conversation completed", final_judgment)
            
            return {
                "topic": self.debate_topic,
                "conversation_history": self.conversation_history,
                "final_judgment": final_judgment,
                "total_exchanges": len(self.conversation_history)
            }
            
        except Exception as e:
            print(f"❌ Conversation error: {e}")
            return None

def main():
    """Main function for natural conversational debate"""
    print("💬 Welcome to Natural Conversational Debate System!")
    print("🎙️ Featuring short, natural dialogue exchanges with real-time audio")
    
    crew_audio_system = CrewAudioDebateSystem()
    
    # Get topic from command line or user input
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
        print(f"📋 Using provided topic: {topic}")
    else:
        print("\n🎯 Choose your option:")
        print("1. Enter a conversation topic")
        print("2. Generate a topic automatically")
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "2":
            topic = None  # Will trigger automatic generation
            print("🤖 Will generate topic automatically...")
        else:
            topic = input("Enter conversation topic: ").strip()
            if not topic:
                print("❌ Please provide a conversation topic!")
                return
    
    try:
        if crew_audio_system.audio_enabled:
            print("🎧 Audio system ready! Real-time voice generation enabled.")
        else:
            print("📝 Audio disabled - text-only mode.")
        
        print("▶️ Starting conversational debate...")
        
        # Run the natural conversation system
        result = crew_audio_system.run_structured_debate(topic)
        
        if result:
            print("\n" + "="*60)
            print("📋 CONVERSATION COMPLETED:")
            print("="*60)
            print(f"💭 Topic: {result['topic']}")
            print(f"🔄 Total exchanges: {result['total_exchanges']}")
            print(f"🗣️ Responses per person: {result['total_exchanges']}")
            print("\n⚖️ Final Evaluation:")
            print("-" * 40)
            print(result['final_judgment'])
            print("\n" + "="*60)
            print("✨ Natural Conversation Features:")
            print("🗣️ Short, natural dialogue style (1-2 sentences)")
            print("🔄 Contextual responses building on previous statements")
            if crew_audio_system.audio_enabled:
                print("🎙️ Real-time audio generation and playback")
                print("🎭 Voice personalities for each debater")
                print("⚡ Concurrent audio/response generation")
            else:
                print("📝 Real-time text conversation")
            print("⚖️ Conversational evaluation")
            print("💭 Automatic topic generation available")
            print("📁 Complete conversation logging")
            print("="*60)
        else:
            print("❌ Conversation failed to complete")
        
    except KeyboardInterrupt:
        print("\n🛑 Conversation interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
