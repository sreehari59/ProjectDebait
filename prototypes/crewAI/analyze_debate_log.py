#!/usr/bin/env python3
"""
Debate Log Analyzer
Analyzes the JSON debate logs to show what data is being captured
"""

import json
import sys
import os
from datetime import datetime

def analyze_debate_log(filename):
    """Analyze a specific debate log file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"\n{'='*60}")
        print(f"📋 DEBATE LOG ANALYSIS: {filename}")
        print(f"{'='*60}")
        
        # Basic info
        print(f"🎭 Topic: {data.get('topic', 'N/A')}")
        print(f"⏰ Timestamp: {data.get('timestamp', 'N/A')}")
        
        # Shared memory analysis
        shared_memory = data.get('shared_memory', {})
        print(f"\n🧠 SHARED MEMORY ANALYSIS:")
        print(f"{'='*40}")
        
        # Research Pro
        research_pro = shared_memory.get('research_pro', [])
        print(f"🔬 Pro Research: {len(research_pro)} entries")
        if research_pro:
            for i, entry in enumerate(research_pro):
                print(f"   Entry {i+1}: {entry.get('agent_role', 'Unknown')} at {entry.get('timestamp', 'Unknown')}")
                output_preview = str(entry.get('output', ''))[:100] + "..." if len(str(entry.get('output', ''))) > 100 else str(entry.get('output', ''))
                print(f"   Preview: {output_preview}")
        else:
            print("   ❌ No pro research captured")
        
        # Research Con
        research_con = shared_memory.get('research_con', [])
        print(f"\n🔬 Con Research: {len(research_con)} entries")
        if research_con:
            for i, entry in enumerate(research_con):
                print(f"   Entry {i+1}: {entry.get('agent_role', 'Unknown')} at {entry.get('timestamp', 'Unknown')}")
                output_preview = str(entry.get('output', ''))[:100] + "..." if len(str(entry.get('output', ''))) > 100 else str(entry.get('output', ''))
                print(f"   Preview: {output_preview}")
        else:
            print("   ❌ No con research captured")
        
        # Pro Debater
        pro_argument = shared_memory.get('pro_debater_argument', [])
        print(f"\n🗣️ Pro Debater: {len(pro_argument)} entries")
        if pro_argument:
            for i, entry in enumerate(pro_argument):
                print(f"   Entry {i+1}: {entry.get('agent_role', 'Unknown')} at {entry.get('timestamp', 'Unknown')}")
                output_preview = str(entry.get('output', ''))[:100] + "..." if len(str(entry.get('output', ''))) > 100 else str(entry.get('output', ''))
                print(f"   Preview: {output_preview}")
        else:
            print("   ❌ No pro argument captured")
        
        # Con Debater
        con_argument = shared_memory.get('con_debater_argument', [])
        print(f"\n🗣️ Con Debater: {len(con_argument)} entries")
        if con_argument:
            for i, entry in enumerate(con_argument):
                print(f"   Entry {i+1}: {entry.get('agent_role', 'Unknown')} at {entry.get('timestamp', 'Unknown')}")
                output_preview = str(entry.get('output', ''))[:100] + "..." if len(str(entry.get('output', ''))) > 100 else str(entry.get('output', ''))
                print(f"   Preview: {output_preview}")
        else:
            print("   ❌ No con argument captured")
        
        # Judge Evaluation
        judge_eval = shared_memory.get('judge_evaluation', [])
        print(f"\n⚖️ Judge Evaluation: {len(judge_eval)} entries")
        if judge_eval:
            for i, entry in enumerate(judge_eval):
                print(f"   Entry {i+1}: {entry.get('agent_role', 'Unknown')} at {entry.get('timestamp', 'Unknown')}")
                output_preview = str(entry.get('output', ''))[:100] + "..." if len(str(entry.get('output', ''))) > 100 else str(entry.get('output', ''))
                print(f"   Preview: {output_preview}")
        else:
            print("   ❌ No judge evaluation captured")
        
        # Summary
        total_captured = len(research_pro) + len(research_con) + len(pro_argument) + len(con_argument) + len(judge_eval)
        print(f"\n📊 CAPTURE SUMMARY:")
        print(f"{'='*40}")
        print(f"Total components captured: {total_captured}/5")
        if total_captured == 5:
            print("✅ All components successfully captured!")
        else:
            print(f"⚠️ {5 - total_captured} components missing")
        
        # Final result preview
        final_result = data.get('final_result', '')
        print(f"\n🏆 FINAL RESULT:")
        print(f"{'='*40}")
        if final_result:
            result_preview = final_result[:200] + "..." if len(final_result) > 200 else final_result
            print(result_preview)
        else:
            print("❌ No final result found")
        
        print(f"\n{'='*60}")
        
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {filename}")
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")

def list_debate_logs():
    """List all available debate log files"""
    log_files = [f for f in os.listdir('.') if f.startswith('debate_log_') and f.endswith('.json')]
    log_files.sort(reverse=True)  # Most recent first
    
    print(f"\n📁 AVAILABLE DEBATE LOGS:")
    print(f"{'='*40}")
    
    if not log_files:
        print("❌ No debate logs found")
        return []
    
    for i, log_file in enumerate(log_files, 1):
        # Get file modification time
        try:
            mtime = os.path.getmtime(log_file)
            formatted_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {log_file} (Modified: {formatted_time})")
        except:
            print(f"{i}. {log_file}")
    
    return log_files

def main():
    """Main function"""
    print("🔍 DEBATE LOG ANALYZER")
    
    if len(sys.argv) > 1:
        # Specific file provided
        filename = sys.argv[1]
        analyze_debate_log(filename)
    else:
        # List available logs and analyze most recent
        log_files = list_debate_logs()
        
        if log_files:
            print(f"\n🔍 Analyzing most recent log: {log_files[0]}")
            analyze_debate_log(log_files[0])
            
            if len(log_files) > 1:
                print(f"\n💡 To analyze other logs, use:")
                for log_file in log_files[1:3]:  # Show next 2
                    print(f"   python analyze_debate_log.py {log_file}")

if __name__ == "__main__":
    main()
