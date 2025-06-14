import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai.llm import LLM
import sys
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Mistral LLM
mistral_llm = LLM(
    model="mistral-large-2411",
    api_base="https://api.mistral.ai/v1",
    api_key=os.getenv("MISTRAL_API_KEY")
)

class DebatingSystem:
    def __init__(self):
        self.debate_topic = ""
        self.shared_memory = {
            # "research_pro": [],
            # "research_con": [],
            "pro_debater_argument": [],
            "con_debater_argument": [],
            "judge_evaluation": [],
            "arguments": [],  # Keep for backward compatibility
            "debate_context": "",
            "timestamp": datetime.now().isoformat()
        }
        
    def create_agents(self):
        """Create the debating agents, research agents, and judge"""
        
        # # Research Agent for Pro side
        # self.research_agent_pro = Agent(
        #     role="Pro Research Specialist",
        #     goal=f"Gather comprehensive research supporting the PRO position on: {self.debate_topic}",
        #     backstory="""You are a thorough research specialist who excels at finding credible sources, 
        #     statistics, case studies, and expert opinions that support the pro side of any debate topic. 
        #     You focus on gathering factual evidence, real-world examples, and authoritative references.""",
        #     llm=mistral_llm,
        #     verbose=True
        # )
        
        # # Research Agent for Con side
        # self.research_agent_con = Agent(
        #     role="Con Research Specialist", 
        #     goal=f"Gather comprehensive research supporting the CON position on: {self.debate_topic}",
        #     backstory="""You are a thorough research specialist who excels at finding credible sources,
        #     statistics, case studies, and expert opinions that support the con side of any debate topic.
        #     You focus on identifying risks, limitations, counterexamples, and critical perspectives.""",
        #     llm=mistral_llm,
        #     verbose=True
        # )
        
        # Agent 1 - Pro side (Enhanced with research context)
        self.agent_pro = Agent(
            role="Pro Debater",
            goal=f"Argue convincingly in favor of the debate topic using research: {self.debate_topic}",
            backstory="""You are an experienced debater who specializes in finding and presenting 
            strong arguments in favor of any given topic. You use logical reasoning, evidence from research, 
            and persuasive rhetoric to make compelling cases for the pro side. You work closely with your 
            research team to build evidence-based arguments.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Agent 2 - Con side (Enhanced with research context)
        self.agent_con = Agent(
            role="Con Debater",
            goal=f"Argue convincingly against the debate topic using research: {self.debate_topic}",
            backstory="""You are an experienced debater who specializes in identifying weaknesses 
            and presenting strong counter-arguments against any given topic. You use critical thinking, 
            evidence from research, and logical reasoning to make compelling cases for the con side.
            You work closely with your research team to build evidence-based arguments.""",
            llm=mistral_llm,
            verbose=True
        )
        
        # Judge Agent (Enhanced to consider research quality)
        self.judge_agent = Agent(
            role="Debate Judge",
            goal="Evaluate the debate arguments objectively and determine the winner based on evidence quality",
            backstory="""You are an impartial and experienced debate judge. You evaluate arguments 
            based on logic, evidence quality, research credibility, persuasiveness, and overall coherence. 
            You provide fair and detailed assessments of both sides before declaring a winner, paying special 
            attention to how well each side used their research.""",
            llm=mistral_llm,
            verbose=True
        )
    
    def create_tasks(self):
        """Create the research and debate tasks with shared memory integration"""
        
        # # Research task for Pro side
        # self.task_research_pro = Task(
        #     description=f"""Conduct thorough research to support the PRO position on: {self.debate_topic}
            
        #     Research should include:
        #     - Statistical data and factual evidence supporting the pro position
        #     - Case studies, examples, and success stories
        #     - Expert opinions and authoritative sources
        #     - Benefits, advantages, and positive outcomes
        #     - Responses to common counterarguments
            
        #     Store your findings in a structured format that can be used by the Pro Debater.
        #     """,
        #     expected_output="Comprehensive research findings with sources, statistics, and evidence supporting the pro position",
        #     agent=self.research_agent_pro
        # )
        
        # # Research task for Con side
        # self.task_research_con = Task(
        #     description=f"""Conduct thorough research to support the CON position on: {self.debate_topic}
            
        #     Research should include:
        #     - Statistical data and factual evidence opposing the position
        #     - Case studies, examples, and failure stories
        #     - Expert opinions and critical perspectives
        #     - Risks, disadvantages, and negative outcomes
        #     - Rebuttals to common pro arguments
            
        #     Store your findings in a structured format that can be used by the Con Debater.
        #     """,
        #     expected_output="Comprehensive research findings with sources, statistics, and evidence supporting the con position",
        #     agent=self.research_agent_con
        # )


        # --------------- working code ---------------
 


        # # Pro argument task (Enhanced with research context)
        # self.task_pro = Task(
        #     description=f"""Using the research provided, present a strong, well-reasoned argument in FAVOR of: {self.debate_topic}
            
        #     Your argument should include:
        #     - Clear main points supporting your position backed by research
        #     - Specific statistics, case studies, and expert opinions from your research
        #     - Logical reasoning connecting research findings to your points
        #     - Address potential counterarguments using research-based rebuttals
        #     - Keep your argument compelling and well-evidenced (aim for 3-4 paragraphs)
            
        #     Context from shared memory: {json.dumps(self.shared_memory, indent=2)}
        #     """,
        #     expected_output="A persuasive pro argument with clear reasoning and strong research-based evidence",
        #     agent=self.agent_pro,
        #     context=[self.task_research_pro]
        # )
        
        # # Con argument task (Enhanced with research context)
        # self.task_con = Task(
        #     description=f"""Using the research provided, present a strong, well-reasoned argument AGAINST: {self.debate_topic}
            
        #     Your argument should include:
        #     - Clear main points opposing the position backed by research
        #     - Specific statistics, case studies, and expert opinions from your research
        #     - Logical reasoning connecting research findings to your points
        #     - Address and refute pro arguments using research-based evidence
        #     - Keep your argument compelling and well-evidenced (aim for 3-4 paragraphs)
            
        #     Context from shared memory: {json.dumps(self.shared_memory, indent=2)}
        #     """,
        #     expected_output="A persuasive con argument with clear reasoning and strong research-based evidence",
        #     agent=self.agent_con,
        #     context=[self.task_research_con]
        # )
        
        # # Judge evaluation task (Enhanced to consider research quality)
        # self.task_judge = Task(
        #     description=f"""Evaluate the research-backed debate on: {self.debate_topic}
            
        #     Review both the PRO and CON arguments and their supporting research. Analyze them based on:
        #     - Quality and credibility of research sources
        #     - Strength of reasoning and logic
        #     - Relevance and accuracy of evidence presented
        #     - How well research was integrated into arguments
        #     - Persuasiveness and clarity of presentation
        #     - How well each side addressed counterarguments with evidence
        #     - Overall coherence and research-backed credibility
            
        #     Provide detailed evaluation of research quality and argument strength, then declare a winner.
            
        #     Context from shared memory: {json.dumps(self.shared_memory, indent=2)}
        #     """,
        #     expected_output="""A detailed evaluation of both arguments and their research backing, followed by a clear 
        #     declaration of the winner with specific reasons focusing on research quality and argument strength""",
        #     agent=self.judge_agent,
        #     context=[self.task_research_pro, self.task_research_con, self.task_pro, self.task_con]
        # )

        # Create simplified tasks without research context
        self.task_pro = Task(
            description=f"""Present a strong, well-reasoned argument in FAVOR of: {self.debate_topic}
            
            Your argument should include:
            - Clear main points supporting your position
            - Logical reasoning and evidence
            - Address potential counterarguments
            - Keep your argument compelling and well-structured (aim for 3-4 paragraphs)
            """,
            expected_output="A persuasive pro argument with clear reasoning and evidence",
            agent=self.agent_pro
            # Remove: context=[self.task_research_pro]
        )
        
        # Modify Con argument task (remove research context):
        self.task_con = Task(
            description=f"""Present a strong, well-reasoned argument AGAINST: {self.debate_topic}
            
            Your argument should include:
            - Clear main points opposing the position
            - Logical reasoning and evidence
            - Address and refute pro arguments
            - Keep your argument compelling and well-structured (aim for 3-4 paragraphs)
            """,
            expected_output="A persuasive con argument with clear reasoning and evidence",
            agent=self.agent_con
            # Remove: context=[self.task_research_con]
        )

        # Modify Judge task (remove research context):
        self.task_judge = Task(
            description=f"""Evaluate the debate on: {self.debate_topic}
            
            Review both the PRO and CON arguments. Analyze them based on:
            - Strength of reasoning and logic
            - Quality of evidence presented
            - Persuasiveness and clarity
            - How well each side addressed counterarguments
            - Overall coherence and credibility
            
            Provide detailed evaluation, then declare a winner.
            """,
            expected_output="A detailed evaluation of both arguments followed by a clear declaration of the winner",
            agent=self.judge_agent,
            context=[self.task_pro, self.task_con]
            # Remove: self.task_research_pro, self.task_research_con from context
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
    
    def capture_task_output(self, task_name, agent_role, output):
        """Capture and store task outputs in shared memory"""
        task_data = {
            "agent_role": agent_role,
            "timestamp": datetime.now().isoformat(),
            "output": str(output)
        }
        
        if task_name == "research_pro":
            self.update_shared_memory("research_pro", task_data)
        elif task_name == "research_con":
            self.update_shared_memory("research_con", task_data)
        elif task_name == "argument_pro":
            self.update_shared_memory("pro_debater_argument", task_data)
        elif task_name == "argument_con":
            self.update_shared_memory("con_debater_argument", task_data)
        elif task_name == "judge_evaluation":
            self.update_shared_memory("judge_evaluation", task_data)
    
    def save_debate_log(self, result):
        """Save the complete debate session to a log file"""
        log_data = {
            "topic": self.debate_topic,
            "timestamp": self.shared_memory["timestamp"],
            "shared_memory": self.shared_memory,
            "final_result": str(result)
        }
        
        filename = f"debate_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(log_data, f, indent=2, default=str)
            print(f"📁 Debate log saved to: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save debate log: {e}")

    def run_debate(self, topic):
        """Run the complete enhanced debate process with research and shared memory"""
        self.debate_topic = topic
        self.shared_memory["debate_context"] = f"Debate on: {topic}"
        
        print(f"\n{'='*60}")
        print(f"🎭 SIMPLIFIED AI DEBATE SYSTEM")
        print(f"📋 TOPIC: {topic}")
        print(f"🗣️ Direct Arguments | 🧠 Shared Memory | 👥 Multi-Agent")
        print(f"{'='*60}\n")
        
        # Create agents and tasks
        self.create_agents()
        self.create_tasks()
        
        # Create and run the crew with enhanced workflow
        debate_crew = Crew(
            agents=[
                # self.research_agent_pro, 
                # self.research_agent_con, 
                self.agent_pro, 
                self.agent_con, 
                self.judge_agent
            ],
            tasks=[
                # self.task_research_pro,
                # self.task_research_con, 
                self.task_pro, 
                self.task_con, 
                self.task_judge
            ],
            verbose=True
        )
        
        print("🚀 Starting enhanced debate process...")
        print("🗣️  Phase 1: Pro Arguments")
        print("🗣️  Phase 2: Con Arguments & Rebuttals")
        print("⚖️  Phase 3: Evaluation & Judgment\n")
        
        # Execute the crew and capture individual task outputs
        result = debate_crew.kickoff()
        
        # Capture individual task outputs after execution using a more reliable method
        print("\n📝 Capturing debate components...")
        
        # Access task outputs directly from the completed tasks
        try:
            # Comment out research output capture since we're not using research agents
            # # Capture Research Pro output
            # if hasattr(self.task_research_pro, 'output') and self.task_research_pro.output:
            #     self.capture_task_output("research_pro", "Pro Research Specialist", self.task_research_pro.output)
            #     print("✅ Pro research captured")
            
            # # Capture Research Con output  
            # if hasattr(self.task_research_con, 'output') and self.task_research_con.output:
            #     self.capture_task_output("research_con", "Con Research Specialist", self.task_research_con.output)
            #     print("✅ Con research captured")
                
            # Capture Pro Debater output
            if hasattr(self.task_pro, 'output') and self.task_pro.output:
                self.capture_task_output("argument_pro", "Pro Debater", self.task_pro.output)
                print("✅ Pro argument captured")
                
            # Capture Con Debater output
            if hasattr(self.task_con, 'output') and self.task_con.output:
                self.capture_task_output("argument_con", "Con Debater", self.task_con.output)
                print("✅ Con argument captured")
                
            # Capture Judge output
            if hasattr(self.task_judge, 'output') and self.task_judge.output:
                self.capture_task_output("judge_evaluation", "Debate Judge", self.task_judge.output)
                print("✅ Judge evaluation captured")
                
        except Exception as e:
            print(f"⚠️ Error capturing some outputs: {e}")
            print("🔄 Attempting alternative capture method...")
            
            # Fallback method using crew tasks
            if hasattr(debate_crew, 'tasks') and debate_crew.tasks:
                for i, task in enumerate(debate_crew.tasks):
                    try:
                        if hasattr(task, 'output') and task.output:
                            # Updated indices since we removed research tasks
                            if i == 0:  # Pro Argument (was index 2)
                                self.capture_task_output("argument_pro", "Pro Debater", task.output)
                                print("✅ Pro argument captured (fallback)")
                            elif i == 1:  # Con Argument (was index 3)
                                self.capture_task_output("argument_con", "Con Debater", task.output)
                                print("✅ Con argument captured (fallback)")
                            elif i == 2:  # Judge (was index 4)
                                self.capture_task_output("judge_evaluation", "Debate Judge", task.output)
                                print("✅ Judge evaluation captured (fallback)")
                            # # Comment out research task capture
                            # elif i == 0:  # Research Pro
                            #     self.capture_task_output("research_pro", "Pro Research Specialist", task.output)
                            #     print("✅ Pro research captured (fallback)")
                            # elif i == 1:  # Research Con
                            #     self.capture_task_output("research_con", "Con Research Specialist", task.output)
                            #     print("✅ Con research captured (fallback)")
                    except Exception as task_error:
                        print(f"⚠️ Could not capture task {i}: {task_error}")
        
        # Show summary of captured data
        print(f"\n📊 Shared Memory Summary:")
        # Comment out research summaries since we're not using research agents
        # print(f"   🔬 Pro Research: {'✅' if self.shared_memory['research_pro'] else '❌'}")
        # print(f"   🔬 Con Research: {'✅' if self.shared_memory['research_con'] else '❌'}")  
        print(f"   🗣️ Pro Argument: {'✅' if self.shared_memory['pro_debater_argument'] else '❌'}")
        print(f"   🗣️ Con Argument: {'✅' if self.shared_memory['con_debater_argument'] else '❌'}")
        print(f"   ⚖️ Judge Evaluation: {'✅' if self.shared_memory['judge_evaluation'] else '❌'}")
        
        print(f"\n{'='*60}")
        print("🏆 ENHANCED DEBATE COMPLETE!")
        print(f"{'='*60}")
        
        # Save debate log with all captured data
        self.save_debate_log(result)
        
        return result

def main():
    """Main function to run the debating system"""
    debating_system = DebatingSystem()
    
    if len(sys.argv) > 1:
        # Topic provided as command line argument
        topic = " ".join(sys.argv[1:])
    else:
        # Ask for topic input
        topic = input("Enter the debate topic: ").strip()
    
    if not topic:
        print("❌ Please provide a debate topic!")
        return
    
    try:
        result = debating_system.run_debate(topic)
        print("\n" + "="*60)
        print("📋 FINAL JUDGMENT:")
        print("="*60)
        print(result)
        print("\n" + "="*60)
        print("✨ Enhanced features used:")
        # Comment out research agents line since we're not using them
        # print("🔬 Research Agents - Gathered evidence for both sides")
        print("🗣️ Direct Debate - Pro and Con arguments")
        print("🧠 Shared Memory - Maintained context throughout debate") 
        print("📁 Debate Logging - Session saved for review")
        print("="*60)
    except Exception as e:
        print(f"❌ Error running enhanced debate: {str(e)}")
        print("Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
