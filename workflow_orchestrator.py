"""
Multi-Agent Workflow Orchestrator using CrewAI
==============================================

A production-ready multi-agent system that demonstrates intelligent collaboration
between AI agents to research, write, edit, and publish high-quality content.

Author: Kato Ernest Henry
Version: 1.0.0
License: MIT
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import traceback

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriterTool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('outputs/logs/workflow.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """
    Multi-Agent Workflow Orchestrator using CrewAI
    
    This class manages a team of AI agents that work together to:
    1. Research a topic comprehensively
    2. Write high-quality content
    3. Proofread and edit for quality
    4. Publish the final result with proper formatting
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the orchestrator with configuration
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.setup_directories()
        self.setup_tools()
        self.setup_agents()
        self.workflow_metrics = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_cost": 0.0,
            "avg_duration": 0.0
        }
        
        logger.info("WorkflowOrchestrator initialized successfully")
    
    def setup_directories(self):
        """Create necessary directories for outputs and logs"""
        directories = [
            "outputs/blog_posts",
            "outputs/research_reports",
            "outputs/logs",
            "outputs/metrics"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        logger.info("Directory structure created")
    
    def setup_tools(self):
        """Initialize tools for web search and file operations"""
        try:
            # Web search tool for research
            self.search_tool = SerperDevTool()
            
            # File writer tool for publishing
            self.file_writer = FileWriterTool()
            
            logger.info("Tools initialized successfully")
        except Exception as e:
            logger.error(f"Error setting up tools: {e}")
            raise
    
    def setup_agents(self):
        """Define the four specialized agents for the workflow"""
        
        try:
            # 1. Researcher Agent
            self.researcher = Agent(
                role='Senior Research Analyst',
                goal='Conduct comprehensive research on assigned topics and provide detailed, accurate information',
                backstory="""You are a meticulous research analyst with expertise in technology, science, and current affairs.
                You excel at finding credible sources, synthesizing complex information, and presenting
                research findings in a structured, actionable format. Your research forms the foundation
                for high-quality content creation. You always verify facts from multiple sources and
                provide comprehensive analysis.""",
                tools=[self.search_tool],
                verbose=True,
                allow_delegation=False,
                max_execution_time=self.config.get('research_timeout', 300),
                memory=True,
                max_iter=3,
                max_rpm=10
            )
            
            # 2. Writer Agent
            self.writer = Agent(
                role='Expert Technical Writer',
                goal='Create engaging, well-structured, and informative content based on research findings',
                backstory="""You are a skilled technical writer with a talent for making complex topics
                accessible and engaging. You specialize in creating comprehensive articles that are both
                informative and readable, with perfect structure, flow, and clarity. You excel at
                turning research into compelling narratives that engage readers while maintaining
                accuracy and depth. Your writing style adapts to the target audience.""",
                verbose=True,
                allow_delegation=False,
                max_execution_time=self.config.get('writing_timeout', 600),
                memory=True,
                max_iter=3,
                max_rpm=8
            )
            
            # 3. Proofreader Agent
            self.proofreader = Agent(
                role='Senior Content Editor',
                goal='Review, edit, and enhance written content for quality, accuracy, and readability',
                backstory="""You are a meticulous editor with an eye for detail and a passion for
                perfect prose. You excel at improving clarity, fixing grammatical errors, enhancing
                readability, and ensuring content meets professional publishing standards. Your
                editing transforms good writing into exceptional content. You also verify facts,
                improve flow, and ensure consistency throughout the piece.""",
                verbose=True,
                allow_delegation=False,
                max_execution_time=self.config.get('editing_timeout', 300),
                memory=True,
                max_iter=2,
                max_rpm=10
            )
            
            # 4. Publisher Agent
            self.publisher = Agent(
                role='Content Publishing Specialist',
                goal='Format, finalize, and publish content with proper metadata and structure',
                backstory="""You are a publishing expert who specializes in preparing content for
                publication. You add proper formatting, metadata, SEO optimization, and ensure
                the final content is ready for distribution across various platforms. You understand
                different content formats and can optimize content for maximum reach and engagement.""",
                tools=[self.file_writer],
                verbose=True,
                allow_delegation=False,
                max_execution_time=self.config.get('publishing_timeout', 200),
                memory=True,
                max_iter=2,
                max_rpm=10
            )
            
            logger.info("All agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up agents: {e}")
            raise
    
    def create_tasks(self, topic: str, word_count: int = 2000) -> List[Task]:
        """Create the workflow tasks for the given topic"""
        
        tasks = []
        
        # Task 1: Research
        research_task = Task(
            description=f"""Conduct comprehensive research on the topic: {topic}
            
            Your research should include:
            1. Current state of the technology/topic
            2. Key concepts and principles
            3. Recent developments and breakthroughs
            4. Practical applications and use cases
            5. Future implications and trends
            6. Expert opinions and credible sources
            7. Statistical data and supporting evidence
            
            Provide a detailed research report with:
            - Executive summary
            - Key findings organized by subtopic
            - Credible sources and references
            - Potential angles for the article
            - Important statistics and data points
            
            Target length: 1000-1500 words of research notes
            Focus on accuracy, credibility, and comprehensiveness.""",
            agent=self.researcher,
            expected_output="Comprehensive research report with key findings, sources, and content angles"
        )
        tasks.append(research_task)
        
        # Task 2: Writing
        writing_task = Task(
            description=f"""Using the research provided, write a comprehensive {word_count}-word blog post on {topic}
            
            The article should include:
            1. Compelling introduction that hooks the reader
            2. Clear explanation of fundamental concepts
            3. Current state and recent developments
            4. Practical applications and real-world examples
            5. Future implications and predictions
            6. Conclusion that ties everything together
            7. Proper citations and references
            
            Requirements:
            - Exactly {word_count} words
            - Engaging and accessible tone
            - Proper structure with headers and subheaders
            - Include relevant examples and analogies
            - Use active voice and clear language
            - Maintain consistent style throughout
            
            Format: Blog post with markdown headers and proper structure""",
            agent=self.writer,
            expected_output=f"Complete {word_count}-word blog post with proper structure and engaging content",
            context=[research_task]
        )
        tasks.append(writing_task)
        
        # Task 3: Proofreading
        proofreading_task = Task(
            description=f"""Review and edit the blog post for:
            
            1. Grammar, spelling, and punctuation errors
            2. Clarity and readability improvements
            3. Logical flow and structure optimization
            4. Accuracy of technical information
            5. Consistency in tone and style
            6. Proper formatting and headers
            7. Fact-checking and verification
            
            Provide:
            - The edited version of the article
            - A summary of changes made
            - Suggestions for improvement
            - Quality assessment score
            
            Ensure the final content maintains exactly {word_count} words while improving quality.
            Focus on making the content more engaging and professional.""",
            agent=self.proofreader,
            expected_output="Polished, error-free blog post with editing summary and quality improvements",
            context=[writing_task]
        )
        tasks.append(proofreading_task)
        
        # Task 4: Publishing
        publishing_task = Task(
            description=f"""Prepare the final blog post for publication:
            
            1. Add proper metadata (title, author, date, tags, description)
            2. Format for web publication with proper HTML structure
            3. Add SEO-friendly elements and keywords
            4. Create a compelling meta description
            5. Generate relevant tags and categories
            6. Save the final content to appropriate files
            7. Create a publication summary
            
            Create multiple versions:
            - A markdown file for web publication
            - A formatted HTML version
            - A plain text version for distribution
            - A JSON file with metadata
            
            Include publishing metadata and distribution recommendations.
            Save files with timestamp and topic-based naming.""",
            agent=self.publisher,
            expected_output="Final published blog post with metadata, multiple formats, and publication summary",
            context=[proofreading_task]
        )
        tasks.append(publishing_task)
        
        return tasks
    
    def create_crew(self, tasks: List[Task]) -> Crew:
        """Create the crew with agents and tasks"""
        
        try:
            crew = Crew(
                agents=[self.researcher, self.writer, self.proofreader, self.publisher],
                tasks=tasks,
                process=Process.sequential,
                verbose=2,
                memory=True,
                embedder={
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-3-small"
                    }
                }
            )
            
            logger.info("Crew created successfully")
            return crew
            
        except Exception as e:
            logger.error(f"Error creating crew: {e}")
            raise
    
    def run_workflow(self, topic: str, word_count: int = 2000) -> Dict[str, Any]:
        """
        Execute the complete workflow
        
        Args:
            topic: The topic to research and write about
            word_count: Target word count for the article
            
        Returns:
            Dictionary containing workflow results and metrics
        """
        
        self.workflow_metrics["total_runs"] += 1
        start_time = datetime.now()
        
        logger.info(f"Starting workflow for topic: {topic}")
        logger.info(f"Target word count: {word_count}")
        
        try:
            # Create tasks and crew
            tasks = self.create_tasks(topic, word_count)
            crew = self.create_crew(tasks)
            
            # Execute the workflow
            logger.info("Executing workflow...")
            result = crew.kickoff(inputs={"topic": topic, "word_count": word_count})
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            # Update metrics
            self.workflow_metrics["successful_runs"] += 1
            self.workflow_metrics["avg_duration"] = (
                (self.workflow_metrics["avg_duration"] * (self.workflow_metrics["successful_runs"] - 1) + 
                 duration.total_seconds()) / self.workflow_metrics["successful_runs"]
            )
            
            # Save workflow results
            workflow_results = {
                "topic": topic,
                "word_count": word_count,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": str(duration),
                "duration_seconds": duration.total_seconds(),
                "final_output": str(result),
                "agents_used": len(crew.agents),
                "tasks_completed": len(crew.tasks),
                "success": True,
                "output_files": self._get_output_files(topic, start_time),
                "metrics": self.get_performance_metrics()
            }
            
            # Save results to file
            self._save_workflow_results(workflow_results)
            
            logger.info(f"Workflow completed successfully in {duration}")
            logger.info(f"Final output length: {len(str(result))} characters")
            
            return workflow_results
            
        except Exception as e:
            end_time = datetime.now()
            duration = end_time - start_time
            
            self.workflow_metrics["failed_runs"] += 1
            
            error_details = {
                "topic": topic,
                "word_count": word_count,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": str(duration),
                "error": str(e),
                "traceback": traceback.format_exc(),
                "success": False
            }
            
            logger.error(f"Workflow failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            # Save error details
            self._save_error_report(error_details)
            
            return error_details
    
    def _get_output_files(self, topic: str, timestamp: datetime) -> List[str]:
        """Get list of output files for the workflow"""
        
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_').lower()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        return [
            f"outputs/blog_posts/{safe_topic}_{timestamp_str}.md",
            f"outputs/blog_posts/{safe_topic}_{timestamp_str}.html",
            f"outputs/blog_posts/{safe_topic}_{timestamp_str}.txt",
            f"outputs/blog_posts/{safe_topic}_{timestamp_str}_metadata.json"
        ]
    
    def _save_workflow_results(self, results: Dict[str, Any]):
        """Save workflow results to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/metrics/workflow_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Workflow results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving workflow results: {e}")
    
    def _save_error_report(self, error_details: Dict[str, Any]):
        """Save error report to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/logs/error_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(error_details, f, indent=2, default=str)
            logger.info(f"Error report saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving error report: {e}")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and agent information"""
        
        return {
            "agents": [
                {
                    "role": agent.role,
                    "goal": agent.goal,
                    "tools": [tool.__class__.__name__ for tool in agent.tools] if agent.tools else [],
                    "memory_enabled": agent.memory,
                    "max_execution_time": agent.max_execution_time
                }
                for agent in [self.researcher, self.writer, self.proofreader, self.publisher]
            ],
            "configuration": self.config,
            "directories_created": True,
            "tools_initialized": True
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get workflow performance metrics"""
        
        return {
            "total_runs": self.workflow_metrics["total_runs"],
            "successful_runs": self.workflow_metrics["successful_runs"],
            "failed_runs": self.workflow_metrics["failed_runs"],
            "success_rate": (
                self.workflow_metrics["successful_runs"] / self.workflow_metrics["total_runs"] * 100
                if self.workflow_metrics["total_runs"] > 0 else 0
            ),
            "average_duration_seconds": self.workflow_metrics["avg_duration"],
            "estimated_cost_per_run": self._estimate_cost(),
            "last_updated": datetime.now().isoformat()
        }
    
    def _estimate_cost(self) -> float:
        """Estimate cost per workflow run"""
        # Rough estimate based on typical token usage
        # This is a simplified calculation
        estimated_tokens = 15000  # Average tokens per workflow
        cost_per_1k_tokens = 0.002  # GPT-4 pricing (approximate)
        return (estimated_tokens / 1000) * cost_per_1k_tokens
    
    def batch_process(self, topics: List[str], word_count: int = 2000) -> List[Dict[str, Any]]:
        """Process multiple topics in batch"""
        
        results = []
        
        logger.info(f"Starting batch processing for {len(topics)} topics")
        
        for i, topic in enumerate(topics, 1):
            logger.info(f"Processing topic {i}/{len(topics)}: {topic}")
            
            try:
                result = self.run_workflow(topic, word_count)
                results.append(result)
                
                if result["success"]:
                    logger.info(f"✅ Completed: {topic}")
                else:
                    logger.error(f"❌ Failed: {topic}")
                    
            except Exception as e:
                logger.error(f"❌ Error processing {topic}: {e}")
                results.append({
                    "topic": topic,
                    "error": str(e),
                    "success": False
                })
        
        logger.info(f"Batch processing completed: {len([r for r in results if r.get('success')])} successful, {len([r for r in results if not r.get('success')])} failed")
        
        return results

    def save_output_files(self, topic: str, content: str, timestamp: datetime) -> Dict[str, str]:
        """Save output files in multiple formats"""
        
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_').lower()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        
        files_saved = {}
        
        try:
            # Save markdown file
            md_filename = f"outputs/blog_posts/{safe_topic}_{timestamp_str}.md"
            with open(md_filename, 'w', encoding='utf-8') as f:
                f.write(content)
            files_saved["markdown"] = md_filename
            
            # Save text file
            txt_filename = f"outputs/blog_posts/{safe_topic}_{timestamp_str}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(content)
            files_saved["text"] = txt_filename
            
            # Save HTML file with basic formatting
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{topic}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; }}
        h1, h2, h3 {{ color: #333; }}
        p {{ margin-bottom: 16px; }}
        pre {{ background-color: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div id="content">
        {content.replace('\n', '<br>')}
    </div>
</body>
</html>"""
            
            html_filename = f"outputs/blog_posts/{safe_topic}_{timestamp_str}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            files_saved["html"] = html_filename
            
            # Save metadata JSON
            metadata = {
                "topic": topic,
                "timestamp": timestamp.isoformat(),
                "word_count": len(content.split()),
                "character_count": len(content),
                "files_created": files_saved,
                "created_by": "WorkflowOrchestrator"
            }
            
            json_filename = f"outputs/blog_posts/{safe_topic}_{timestamp_str}_metadata.json"
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            files_saved["metadata"] = json_filename
            
            logger.info(f"Files saved: {list(files_saved.values())}")
            
        except Exception as e:
            logger.error(f"Error saving output files: {e}")
            
        return files_saved


def main():
    """Main execution function for testing"""
    
    print("🤖 Multi-Agent Workflow Orchestrator")
    print("=====================================")
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set your OPENAI_API_KEY in a .env file")
        print("Example: OPENAI_API_KEY=sk-your_key_here")
        return
    
    # Initialize orchestrator
    try:
        orchestrator = WorkflowOrchestrator()
        print("✅ Orchestrator initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing orchestrator: {e}")
        return
    
    # Display workflow information
    print("\n📋 Workflow Configuration:")
    status = orchestrator.get_workflow_status()
    
    print(f"Agents: {len(status['agents'])}")
    for i, agent in enumerate(status['agents'], 1):
        print(f"  {i}. {agent['role']}")
        print(f"     Tools: {', '.join(agent['tools']) if agent['tools'] else 'None'}")
        print(f"     Memory: {agent['memory_enabled']}")
    
    # Run the workflow
    print("\n" + "=" * 60)
    topic = "Quantum Computing"
    print(f"🚀 Starting workflow for: {topic}")
    
    results = orchestrator.run_workflow(topic)
    
    if results["success"]:
        print(f"\n🎉 Workflow completed successfully!")
        print(f"⏱️  Duration: {results['duration']}")
        print(f"📝 Output files: {len(results['output_files'])}")
        print(f"💰 Estimated cost: ${orchestrator._estimate_cost():.3f}")
        
        # Display performance metrics
        metrics = orchestrator.get_performance_metrics()
        print(f"\n📊 Performance Metrics:")
        print(f"   Success rate: {metrics['success_rate']:.1f}%")
        print(f"   Average duration: {metrics['average_duration_seconds']:.1f}s")
        print(f"   Total runs: {metrics['total_runs']}")
        
        # Show output files
        print(f"\n📄 Output Files:")
        for file_path in results['output_files']:
            print(f"   📁 {file_path}")
            
    else:
        print(f"\n❌ Workflow failed!")
        print(f"⚠️  Error: {results.get('error', 'Unknown error')}")
        print(f"⏱️  Duration: {results.get('duration', 'N/A')}")
        
        # Show error details
        if results.get('traceback'):
            print(f"\n🔍 Error Details:")
            print(results['traceback'])
    
    # Display final status
    print("\n" + "=" * 60)
    print("🏁 Workflow execution completed")
    print(f"📊 Check outputs/ directory for results")
    print(f"📋 Check outputs/logs/ directory for detailed logs")


def demo_batch_processing():
    """Demo function for batch processing multiple topics"""
    
    print("🔄 Batch Processing Demo")
    print("=======================")
    
    # Sample topics for batch processing
    topics = [
        "Artificial Intelligence Ethics",
        "Sustainable Energy Solutions",
        "Future of Space Exploration",
        "Blockchain Technology Applications"
    ]
    
    try:
        orchestrator = WorkflowOrchestrator()
        
        print(f"📋 Processing {len(topics)} topics...")
        results = orchestrator.batch_process(topics, word_count=1500)
        
        # Display results summary
        successful = [r for r in results if r.get('success')]
        failed = [r for r in results if not r.get('success')]
        
        print(f"\n📊 Batch Processing Results:")
        print(f"   ✅ Successful: {len(successful)}")
        print(f"   ❌ Failed: {len(failed)}")
        
        if successful:
            print(f"\n🎉 Successfully processed:")
            for result in successful:
                print(f"   • {result['topic']} ({result['duration']})")
                
        if failed:
            print(f"\n⚠️  Failed topics:")
            for result in failed:
                print(f"   • {result['topic']}: {result.get('error', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Batch processing error: {e}")


def interactive_mode():
    """Interactive mode for user input"""
    
    print("🎮 Interactive Mode")
    print("==================")
    
    try:
        orchestrator = WorkflowOrchestrator()
        
        while True:
            print("\n" + "=" * 50)
            print("Enter a topic (or 'quit' to exit):")
            topic = input("Topic: ").strip()
            
            if topic.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not topic:
                print("Please enter a valid topic.")
                continue
                
            print(f"\nEnter word count (default: 2000):")
            word_count_input = input("Word count: ").strip()
            
            try:
                word_count = int(word_count_input) if word_count_input else 2000
            except ValueError:
                word_count = 2000
                print("Using default word count: 2000")
                
            print(f"\n🚀 Processing: {topic}")
            print(f"📝 Target words: {word_count}")
            
            results = orchestrator.run_workflow(topic, word_count)
            
            if results["success"]:
                print(f"✅ Completed in {results['duration']}")
                print(f"📁 Files saved: {len(results['output_files'])}")
            else:
                print(f"❌ Failed: {results.get('error', 'Unknown error')}")
                
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"❌ Error in interactive mode: {e}")


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            demo_batch_processing()
        elif sys.argv[1] == "interactive":
            interactive_mode()
        elif sys.argv[1] == "help":
            print("Usage:")
            print("  python workflow_orchestrator.py        # Run default demo")
            print("  python workflow_orchestrator.py batch  # Run batch processing demo")
            print("  python workflow_orchestrator.py interactive  # Run interactive mode")
            print("  python workflow_orchestrator.py help   # Show this help")
        else:
            print(f"Unknown command: {sys.argv[1]}")
            print("Use 'help' for available commands")
    else:
        # Run main demo
        main()