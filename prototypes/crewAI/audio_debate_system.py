#!/usr/bin/env python3
"""
Audio-Enhanced AI Debate System
Real-time conversational debates with ElevenLabs voice synthesis
"""

import os
import sys
import json
import argparse
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.llm import LLM

# Load environment variables
load_dotenv()

# Check for ElevenLabs availability
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play, stream
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("⚠️ ElevenLabs not installed. Run: pip install elevenlabs")

# Initialize LLMs
mistral_llm = LLM(
    model="mistral-large-2411",
    api_base="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY")
)

# ElevenLabs client
if ELEVENLABS_AVAILABLE and os.getenv("ELEVENLABS_API_KEY"):
    elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
else:
    elevenlabs_client = None

# Voice configuration for different agents
VOICE_CONFIG = {
    "pro_debater": {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - Professional female
        "name": "Rachel (Pro Debater)",
        "style": "confident and persuasive"
    },
    "con_debater": {
        "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi - Analytical male  
        "name": "Domi (Con Debater)", 
        "style": "analytical and critical"
    },
    "judge": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL",  # Bella - Neutral professional
        "name": "Bella (Judge)",
        "style": "balanced and authoritative"
    },
    "researcher": {
        "voice_id": "ErXwobaYiN019PkySvjV",  # Antoni - Information delivery
        "name": "Antoni (Researcher)",
        "style": "informative and clear"
    }
}

class AudioDebateSystem:
    def __init__(self, mode="individual", streaming=True):
        self.mode = mode  # "individual", "conversation", "mixed"
        self.streaming = streaming  # True for real-time streaming, False for file generation
        self.debate_topic = ""
        self.audio_enabled = elevenlabs_client is not None
        self.save_audio = True
        self.audio_dir = f"audio_debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.shared_memory = {
            "research_pro": [],
            "research_con": [],
            "pro_debater_argument": [],
            "con_debater_argument": [],
            "judge_evaluation": [],
            "audio_files": [],
            "debate_context": "",
            "streaming_mode": streaming,
            "timestamp": datetime.now().isoformat()
        }
        
        if self.save_audio and not streaming:
            os.makedirs(self.audio_dir, exist_ok=True)
    
    def stream_text_realtime(self, text, agent_type):
        """Stream text to speech for real-time audio debate"""
        if not self.audio_enabled:
            print(f"🔇 Audio disabled: {agent_type}")
            return
            
        try:
            voice_config = VOICE_CONFIG.get(agent_type, VOICE_CONFIG["judge"])
            
            print(f"🎙️ {voice_config['name']} speaking live...")
            print(f"💬 \"{text[:100]}{'...' if len(text) > 100 else ''}\"")
            
            # Stream audio in real-time
            audio_stream = elevenlabs_client.text_to_speech.stream(
                text=text,
                voice_id=voice_config["voice_id"],
                model_id="eleven_multilingual_v2"
            )
            
            print(f"🔊 Live streaming...")
            stream(audio_stream)
            print(f"✅ Stream complete\n")
            
        except Exception as e:
            print(f"❌ Streaming error for {agent_type}: {e}")

    def speak_text(self, text, agent_type, save_filename=None, play_audio=True):
        """Convert text to speech using ElevenLabs streaming"""
        if not self.audio_enabled:
            print(f"🔇 Audio disabled: {agent_type}")
            return None
            
        try:
            voice_config = VOICE_CONFIG.get(agent_type, VOICE_CONFIG["judge"])
            
            print(f"🎙️ {voice_config['name']} speaking...")
            
            if play_audio and not save_filename:
                # Option 1: Stream and play immediately (real-time)
                audio_stream = elevenlabs_client.text_to_speech.stream(
                    text=text,
                    voice_id=voice_config["voice_id"],
                    model_id="eleven_multilingual_v2"
                )
                
                print(f"🔊 Streaming audio for {voice_config['name']}...")
                stream(audio_stream)
                print(f"✅ Audio stream complete")
                return None
                
            else:
                # Option 2: Generate and save audio (with optional playback)
                audio_stream = elevenlabs_client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_config["voice_id"],
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128"
                )
                
                # Convert generator to bytes
                audio = b"".join(audio_stream)
                
                # Save audio file
                if save_filename:
                    filepath = os.path.join(self.audio_dir, f"{save_filename}.mp3")
                    with open(filepath, "wb") as f:
                        f.write(audio)
                    self.shared_memory["audio_files"].append({
                        "agent_type": agent_type,
                        "filename": filepath,
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"💾 Audio saved: {filepath}")
                
                # Play audio if requested
                if play_audio:
                    play(audio)
                    
                return audio
            
        except Exception as e:
            print(f"❌ Audio error for {agent_type}: {e}")
            return None
    
    def create_dialogue_audio(self, dialogue_segments):
        """Create conversational dialogue audio using ElevenLabs Text-to-Dialogue"""
        if not self.audio_enabled:
            return None
            
        try:
            # Prepare dialogue inputs
            inputs = []
            for segment in dialogue_segments:
                agent_type = segment["agent_type"]
                text = segment["text"]
                voice_config = VOICE_CONFIG.get(agent_type, VOICE_CONFIG["judge"])
                
                # Add emotional context to text for more natural conversation
                styled_text = f"[{voice_config['style']}] {text}"
                
                inputs.append({
                    "text": styled_text,
                    "voice_id": voice_config["voice_id"]
                })
            
            print(f"🎭 Creating conversational dialogue with {len(inputs)} segments...")
            
            # Generate dialogue audio
            audio_stream = elevenlabs_client.text_to_dialogue.convert(inputs=inputs)
            
            # Convert generator to bytes
            audio = b"".join(audio_stream)
            
            # Save dialogue audio
            dialogue_file = os.path.join(self.audio_dir, "full_dialogue.mp3")
            with open(dialogue_file, "wb") as f:
                f.write(audio)
            
            print(f"🎬 Dialogue audio saved: {dialogue_file}")
            
            # Play dialogue
            play(audio)
            
            return audio
            
        except Exception as e:
            print(f"❌ Dialogue audio error: {e}")
            return None
    
    def create_agents(self):
        """Create the debating agents with audio-enhanced backstories"""
        
        # Research Agent for Pro side
        self.research_agent_pro = Agent(
            role="Pro Research Specialist",
            goal=f"Gather comprehensive research supporting the PRO position on: {self.debate_topic}",
            backstory="""You are a thorough research specialist who excels at finding credible sources, 
            statistics, case studies, and expert opinions that support the pro side of any debate topic. 
            You focus on gathering factual evidence, real-world examples, and authoritative references.
            Your research will be presented audibly in a conversational debate format.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Research Agent for Con side
        self.research_agent_con = Agent(
            role="Con Research Specialist", 
            goal=f"Gather comprehensive research supporting the CON position on: {self.debate_topic}",
            backstory="""You are a thorough research specialist who excels at finding credible sources,
            statistics, case studies, and expert opinions that support the con side of any debate topic.
            You focus on identifying risks, limitations, counterexamples, and critical perspectives.
            Your research will be presented audibly in a conversational debate format.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Pro Debater with audio personality
        self.agent_pro = Agent(
            role="Pro Debater",
            goal=f"Present compelling audio arguments in favor of: {self.debate_topic}",
            backstory=f"""You are an experienced debater with a confident and persuasive speaking style.
            You specialize in presenting strong arguments in favor of any given topic using logical reasoning, 
            evidence from research, and persuasive rhetoric. Your arguments will be spoken aloud using the 
            voice of {VOICE_CONFIG['pro_debater']['name']}, so structure your responses for natural speech.
            Use conversational language, pause points, and emphasis for maximum impact.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Con Debater with audio personality
        self.agent_con = Agent(
            role="Con Debater",
            goal=f"Present compelling audio arguments against: {self.debate_topic}",
            backstory=f"""You are an experienced debater with an analytical and critical speaking style.
            You specialize in identifying weaknesses and presenting strong counter-arguments against any given topic.
            Your arguments will be spoken aloud using the voice of {VOICE_CONFIG['con_debater']['name']}, 
            so structure your responses for natural speech. Use conversational language, logical reasoning, 
            and critical analysis for maximum impact.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Judge with audio personality
        self.judge_agent = Agent(
            role="Audio Debate Judge",
            goal="Provide balanced audio evaluation of the debate arguments",
            backstory=f"""You are an impartial and experienced debate judge with a balanced and authoritative 
            speaking style. You evaluate arguments based on logic, evidence quality, research credibility, 
            persuasiveness, and overall coherence. Your evaluation will be spoken aloud using the voice of 
            {VOICE_CONFIG['judge']['name']}, so structure your response for natural speech with clear reasoning 
            and a definitive conclusion.""",
            llm=mistral_llm,
            verbose=True
        )
    
    def create_tasks(self):
        """Create tasks optimized for audio presentation"""
        
        # Research tasks (background - may not be spoken)
        self.task_research_pro = Task(
            description=f"""Conduct thorough research to support the PRO position on: {self.debate_topic}
            
            Focus on finding:
            - Statistical data and factual evidence
            - Case studies and success stories  
            - Expert opinions and authoritative sources
            - Benefits and positive outcomes
            - Responses to common counterarguments
            
            Structure findings clearly for use in audio debate arguments.
            """,
            expected_output="Comprehensive research findings formatted for audio debate presentation",
            agent=self.research_agent_pro
        )
        
        self.task_research_con = Task(
            description=f"""Conduct thorough research to support the CON position on: {self.debate_topic}
            
            Focus on finding:
            - Statistical data and opposing evidence
            - Case studies and failure examples
            - Expert opinions and critical perspectives  
            - Risks and negative outcomes
            - Rebuttals to common pro arguments
            
            Structure findings clearly for use in audio debate arguments.
            """,
            expected_output="Comprehensive research findings formatted for audio debate presentation",
            agent=self.research_agent_con
        )

        # Audio-optimized debate tasks
        self.task_pro = Task(
            description=f"""Present a compelling 2-3 minute audio argument in FAVOR of: {self.debate_topic}
            
            Your argument will be spoken aloud, so:
            - Use natural, conversational language
            - Structure with clear main points (2-3 key arguments)
            - Include specific evidence and examples from research
            - Use rhetorical devices for impact
            - End with a strong conclusion
            - Aim for 250-350 words for optimal audio length
            - Write as if speaking directly to an audience
            
            Research context: Use findings from the Pro Research Specialist
            """,
            expected_output="A persuasive 2-3 minute audio argument with natural speech patterns",
            agent=self.agent_pro,
            context=[self.task_research_pro]
        )
        
        self.task_con = Task(
            description=f"""Present a compelling 2-3 minute audio argument AGAINST: {self.debate_topic}
            
            Your argument will be spoken aloud, so:
            - Use natural, conversational language
            - Structure with clear main points (2-3 key counterarguments)
            - Include specific evidence and examples from research
            - Address and refute pro arguments
            - End with a strong conclusion
            - Aim for 250-350 words for optimal audio length
            - Write as if speaking directly to an audience
            
            Research context: Use findings from the Con Research Specialist
            """,
            expected_output="A persuasive 2-3 minute audio argument with natural speech patterns",
            agent=self.agent_con,
            context=[self.task_research_con]
        )
        
        self.task_judge = Task(
            description=f"""Provide a balanced audio evaluation of the debate on: {self.debate_topic}
            
            Your evaluation will be spoken aloud, so:
            - Start with acknowledgment of both sides
            - Analyze argument strength, evidence quality, and persuasiveness
            - Use clear, authoritative language
            - Explain your reasoning step by step
            - Conclude with a clear winner declaration
            - Aim for 200-300 words for optimal audio length
            - Speak as if addressing a live audience
            
            Consider both research quality and argument presentation.
            """,
            expected_output="A balanced audio evaluation with clear winner declaration",
            agent=self.judge_agent,
            context=[self.task_research_pro, self.task_research_con, self.task_pro, self.task_con]
        )
    
    def update_shared_memory(self, key, data):
        """Update shared memory with new information"""
        if key in self.shared_memory:
            if isinstance(self.shared_memory[key], list):
                self.shared_memory[key].append(data)
            else:
                self.shared_memory[key] = data
        else:
            self.shared_memory[key] = data
        self.shared_memory["timestamp"] = datetime.now().isoformat()
    
    def capture_task_output_with_audio(self, task_name, agent_role, output, agent_type):
        """Capture task output and generate audio (streaming or recorded)"""
        task_data = {
            "agent_role": agent_role,
            "timestamp": datetime.now().isoformat(),
            "output": str(output),
            "audio_generated": False,
            "streaming_mode": self.streaming
        }
        
        # Store in shared memory
        if task_name == "research_pro":
            self.update_shared_memory("research_pro", task_data)
        elif task_name == "research_con":
            self.update_shared_memory("research_con", task_data)
        elif task_name == "argument_pro":
            self.update_shared_memory("pro_debater_argument", task_data)
            # Generate audio for pro argument
            if self.mode in ["individual", "mixed"]:
                if self.streaming:
                    print(f"\n🎭 PRO DEBATER PRESENTING LIVE:")
                    print("="*50)
                    self.stream_text_realtime(str(output), agent_type)
                else:
                    self.speak_text(str(output), agent_type, f"pro_argument_{datetime.now().strftime('%H%M%S')}")
                task_data["audio_generated"] = True
        elif task_name == "argument_con":
            self.update_shared_memory("con_debater_argument", task_data)
            # Generate audio for con argument
            if self.mode in ["individual", "mixed"]:
                if self.streaming:
                    print(f"\n🎭 CON DEBATER PRESENTING LIVE:")
                    print("="*50)
                    self.stream_text_realtime(str(output), agent_type)
                else:
                    self.speak_text(str(output), agent_type, f"con_argument_{datetime.now().strftime('%H%M%S')}")
                task_data["audio_generated"] = True
        elif task_name == "judge_evaluation":
            self.update_shared_memory("judge_evaluation", task_data)
            # Generate audio for judge evaluation
            if self.mode in ["individual", "mixed"]:
                if self.streaming:
                    print(f"\n⚖️ JUDGE DELIVERING VERDICT LIVE:")
                    print("="*50)
                    self.stream_text_realtime(str(output), agent_type)
                else:
                    self.speak_text(str(output), agent_type, f"judge_evaluation_{datetime.now().strftime('%H%M%S')}")
                task_data["audio_generated"] = True
    
    def run_streaming_conversational_debate(self):
        """Run real-time streaming conversational debate"""
        if not self.audio_enabled:
            print("❌ Audio not available for conversational mode")
            return None
            
        print(f"\n🎙️ LIVE STREAMING CONVERSATIONAL DEBATE")
        print(f"{'='*60}")
        print(f"🔴 LIVE - Real-time audio streaming")
        print(f"🎭 Topic: {self.debate_topic}")
        print(f"{'='*60}\n")
        
        # Create agents and tasks
        self.create_agents()
        self.create_tasks()
        
        # Run text-based debate first to generate content
        debate_crew = Crew(
            agents=[self.research_agent_pro, self.research_agent_con, self.agent_pro, self.agent_con, self.judge_agent],
            tasks=[self.task_research_pro, self.task_research_con, self.task_pro, self.task_con, self.task_judge],
            verbose=True
        )
        
        print("🚀 Generating debate content...")
        result = debate_crew.kickoff()
        
        # Get the arguments
        pro_arg = str(self.task_pro.output) if hasattr(self.task_pro, 'output') else "Pro argument not available"
        con_arg = str(self.task_con.output) if hasattr(self.task_con, 'output') else "Con argument not available"
        judge_eval = str(self.task_judge.output) if hasattr(self.task_judge, 'output') else "Judge evaluation not available"
        
        # Stream the debate live in conversational format
        print(f"\n🎬 STARTING LIVE DEBATE STREAM...")
        print(f"{'='*60}")
        
        # Opening
        opening_text = f"Welcome to today's live debate on: {self.debate_topic}. I'm your moderator, and we have two expert debaters ready to present their cases. Let's begin with our first speaker."
        self.stream_text_realtime(opening_text, "judge")
        
        # Pro argument
        print(f"🎯 PRO POSITION:")
        pro_intro = "Thank you, moderator. Ladies and gentlemen, I'm here to argue in favor of this proposition."
        self.stream_text_realtime(pro_intro, "pro_debater")
        self.stream_text_realtime(pro_arg, "pro_debater")
        
        # Transition
        transition_text = "Thank you for that compelling argument. Now let's hear from our opposing debater."
        self.stream_text_realtime(transition_text, "judge")
        
        # Con argument  
        print(f"🎯 CON POSITION:")
        con_intro = "Thank you. I appreciate the previous speaker's points, but I must respectfully disagree."
        self.stream_text_realtime(con_intro, "con_debater")
        self.stream_text_realtime(con_arg, "con_debater")
        
        # Closing and judgment
        closing_text = "We've heard compelling arguments from both sides. Let me now provide my evaluation and final judgment."
        self.stream_text_realtime(closing_text, "judge")
        self.stream_text_realtime(judge_eval, "judge")
        
        # Final closing
        final_text = "That concludes today's live debate. Thank you to both our debaters and to you for listening."
        self.stream_text_realtime(final_text, "judge")
        
        print(f"\n{'='*60}")
        print("🏁 LIVE DEBATE STREAM COMPLETE!")
        print(f"{'='*60}")
        
        return result

    def run_conversational_debate(self):
        """Run debate in conversational dialogue format"""
        if not self.audio_enabled:
            print("❌ Audio not available for conversational mode")
            return None
            
        print(f"\n🎭 CONVERSATIONAL AUDIO DEBATE")
        print(f"{'='*50}")
        
        # Create agents and tasks
        self.create_agents()
        self.create_tasks()
        
        # Run text-based debate first
        debate_crew = Crew(
            agents=[self.research_agent_pro, self.research_agent_con, self.agent_pro, self.agent_con, self.judge_agent],
            tasks=[self.task_research_pro, self.task_research_con, self.task_pro, self.task_con, self.task_judge],
            verbose=True
        )
        
        print("🚀 Generating debate content...")
        result = debate_crew.kickoff()
        
        # Capture outputs
        pro_arg = str(self.task_pro.output) if hasattr(self.task_pro, 'output') else "Pro argument not available"
        con_arg = str(self.task_con.output) if hasattr(self.task_con, 'output') else "Con argument not available"
        judge_eval = str(self.task_judge.output) if hasattr(self.task_judge, 'output') else "Judge evaluation not available"
        
        # Create dialogue segments
        dialogue_segments = [
            {
                "agent_type": "judge",
                "text": f"Welcome to today's debate on: {self.debate_topic}. Let's hear from our first speaker."
            },
            {
                "agent_type": "pro_debater", 
                "text": pro_arg[:500] + "..." if len(pro_arg) > 500 else pro_arg  # Trim for dialogue
            },
            {
                "agent_type": "judge",
                "text": "Thank you. Now let's hear the opposing viewpoint."
            },
            {
                "agent_type": "con_debater",
                "text": con_arg[:500] + "..." if len(con_arg) > 500 else con_arg  # Trim for dialogue
            },
            {
                "agent_type": "judge",
                "text": judge_eval[:400] + "..." if len(judge_eval) > 400 else judge_eval  # Trim for dialogue
            }
        ]
        
        # Generate conversational audio
        print(f"\n🎬 Creating conversational debate audio...")
        self.create_dialogue_audio(dialogue_segments)
        
        return result
    
    def save_audio_debate_log(self, result):
        """Save complete debate session including audio information"""
        log_data = {
            "topic": self.debate_topic,
            "mode": self.mode,
            "timestamp": self.shared_memory["timestamp"],
            "shared_memory": self.shared_memory,
            "audio_directory": self.audio_dir,
            "audio_enabled": self.audio_enabled,
            "final_result": str(result)
        }
        
        filename = f"audio_debate_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
            print(f"📁 Audio debate log saved: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save audio debate log: {e}")
    
    def run_audio_debate(self, topic):
        """Run the complete audio-enhanced debate"""
        self.debate_topic = topic
        self.shared_memory["debate_context"] = f"Audio Debate on: {topic}"
        
        print(f"\n{'='*60}")
        print(f"🎙️ AUDIO-ENHANCED AI DEBATE SYSTEM")
        print(f"📋 TOPIC: {topic}")
        print(f"🎭 MODE: {self.mode.upper()}")
        print(f"🔊 AUDIO: {'✅ Enabled' if self.audio_enabled else '❌ Disabled'}")
        print(f"📡 STREAMING: {'✅ Live' if self.streaming else '❌ Recorded'}")
        print(f"{'='*60}\n")
        
        if self.mode == "conversation":
            if self.streaming:
                result = self.run_streaming_conversational_debate()
            else:
                result = self.run_conversational_debate()
        else:
            # Individual or mixed mode
            self.create_agents()
            self.create_tasks()
            
            # Create and run crew
            debate_crew = Crew(
                agents=[self.research_agent_pro, self.research_agent_con, self.agent_pro, self.agent_con, self.judge_agent],
                tasks=[self.task_research_pro, self.task_research_con, self.task_pro, self.task_con, self.task_judge],
                verbose=True
            )
            
            if self.streaming:
                print("🔴 Starting live streaming audio debate...")
            else:
                print("🚀 Starting audio-enhanced debate...")
            
            result = debate_crew.kickoff()
            
            # Capture outputs with audio generation
            if self.streaming:
                print("\n📡 Live streaming debate components...")
            else:
                print("\n🎙️ Generating speech for debate components...")
            
            try:
                if hasattr(self.task_research_pro, 'output'):
                    self.capture_task_output_with_audio("research_pro", "Pro Research Specialist", self.task_research_pro.output, "researcher")
                
                if hasattr(self.task_research_con, 'output'):
                    self.capture_task_output_with_audio("research_con", "Con Research Specialist", self.task_research_con.output, "researcher")
                
                if hasattr(self.task_pro, 'output'):
                    self.capture_task_output_with_audio("argument_pro", "Pro Debater", self.task_pro.output, "pro_debater")
                
                if hasattr(self.task_con, 'output'):
                    self.capture_task_output_with_audio("argument_con", "Con Debater", self.task_con.output, "con_debater")
                
                if hasattr(self.task_judge, 'output'):
                    self.capture_task_output_with_audio("judge_evaluation", "Debate Judge", self.task_judge.output, "judge")
                    
            except Exception as e:
                print(f"⚠️ Error in audio generation: {e}")
        
        print(f"\n{'='*60}")
        if self.streaming:
            print("🏆 LIVE AUDIO DEBATE COMPLETE!")
            print("📡 Real-time streaming session finished")
        else:
            print("🏆 AUDIO DEBATE COMPLETE!")
            print(f"🎵 Audio files saved in: {self.audio_dir}")
        print(f"{'='*60}")
        
        # Save complete log
        self.save_audio_debate_log(result)
        
        return result

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description="Audio-Enhanced AI Debate System")
    parser.add_argument("topic", nargs="*", help="Debate topic")
    parser.add_argument("--mode", choices=["individual", "conversation", "mixed"], 
                       default="individual", help="Audio debate mode")
    parser.add_argument("--save-audio", action="store_true", help="Save audio files")
    parser.add_argument("--no-playback", action="store_true", help="Don't play audio during debate")
    
    args = parser.parse_args()
    
    # Get topic
    if args.topic:
        topic = " ".join(args.topic)
    else:
        topic = input("Enter the debate topic: ").strip()
    
    if not topic:
        print("❌ Please provide a debate topic!")
        return
    
    # Check audio requirements
    if not ELEVENLABS_AVAILABLE:
        print("❌ ElevenLabs library not installed!")
        print("📦 Install with: pip install elevenlabs")
        return
    
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("❌ ElevenLabs API key not found!")
        print("🔑 Add ELEVENLABS_API_KEY to your .env file")
        return
    
    try:
        # Create audio debate system
        audio_system = AudioDebateSystem(mode=args.mode)
        audio_system.save_audio = args.save_audio or True  # Default to saving
        
        if args.no_playback:
            print("🔇 Audio playback disabled")
        
        # Run debate
        result = audio_system.run_audio_debate(topic)
        
        # Show results
        print("\n" + "="*60)
        print("📋 FINAL JUDGMENT:")
        print("="*60)
        print(result)
        print("\n" + "="*60)
        print("✨ Audio features used:")
        print("🎙️ Text-to-Speech - Arguments spoken aloud")
        print("🎭 Voice Personalities - Distinct voices for each agent")
        print("🎵 Audio Logging - Speech files saved")
        if args.mode == "conversation":
            print("🎬 Conversational Dialogue - Real-time debate format")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error running audio debate: {str(e)}")
        print("Please check your API keys and internet connection.")

if __name__ == "__main__":
    main()
