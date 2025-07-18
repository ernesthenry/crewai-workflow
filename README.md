# 🤖 Multi-Agent Workflow Orchestrator

A production-ready multi-agent system built with CrewAI that demonstrates intelligent collaboration between AI agents to research, write, edit, and publish high-quality content.

## 📋 Project Overview

This orchestrator showcases a complete content creation pipeline where four specialized AI agents work together:

```
🔍 Researcher → ✍️ Writer → 📝 Proofreader → 🚀 Publisher
```

Each agent has specific expertise and tools, creating a seamless workflow that produces professional-quality blog posts from a simple topic input.

## 🎯 Features

- **Multi-Agent Collaboration**: Four specialized agents working in sequence
- **Intelligent Handoffs**: Context preservation between workflow stages
- **Web Research Integration**: Real-time information gathering
- **Quality Assurance**: Built-in editing and proofreading
- **Automated Publishing**: Formatted output with metadata
- **Performance Monitoring**: Detailed metrics and logging
- **Error Handling**: Robust error recovery and reporting
- **Extensible Design**: Easy to customize and extend

## 🏗️ Project Structure

```
crewai-workflow/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── workflow_orchestrator.py     # Main orchestrator class
├── test_setup.py               # Setup verification script
├── run_workflow.py             # Simple execution script
├── config/
│   └── agents_config.py        # Agent configurations
├── outputs/                    # Generated content
│   ├── blog_posts/
│   ├── research_reports/
│   └── logs/
└── examples/
    └── sample_outputs/
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd crewai-workflow
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Run Workflow
```bash
python run_workflow.py
```

## 🔧 Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- ~$5-10 in OpenAI credits

### Step-by-Step Installation

1. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **API Configuration**
   - Get OpenAI API key from https://platform.openai.com/api-keys
   - Copy `.env.example` to `.env`
   - Add your API key to `.env`

4. **Verify Installation**
   ```bash
   python test_setup.py
   ```

## 🎮 Usage

### Basic Usage
```python
from workflow_orchestrator import WorkflowOrchestrator

# Initialize orchestrator
orchestrator = WorkflowOrchestrator()

# Run workflow
results = orchestrator.run_workflow("Quantum Computing")

# Check results
if results["success"]:
    print(f"✅ Completed in {results['duration']}")
    print(f"📄 Output: {results['output_file']}")
```

### Advanced Usage
```python
# Custom configuration
config = {
    "word_count": 3000,
    "tone": "technical",
    "include_references": True
}

# Run with custom settings
results = orchestrator.run_workflow(
    topic="Machine Learning in Healthcare",
    config=config
)
```

### Command Line Interface
```bash
# Basic run
python run_workflow.py "Artificial Intelligence"

# With custom word count
python run_workflow.py "Blockchain Technology" --words 2500

# Verbose output
python run_workflow.py "Space Exploration" --verbose
```

## 🤖 Agent Architecture

### 1. 🔍 Researcher Agent
- **Role**: Senior Research Analyst
- **Tools**: Web search, data analysis
- **Output**: Comprehensive research report with sources

### 2. ✍️ Writer Agent
- **Role**: Expert Technical Writer
- **Tools**: Content generation, structure optimization
- **Output**: Well-structured, engaging blog post

### 3. 📝 Proofreader Agent
- **Role**: Senior Content Editor
- **Tools**: Grammar checking, style improvement
- **Output**: Polished, error-free content

### 4. 🚀 Publisher Agent
- **Role**: Content Publishing Specialist
- **Tools**: File operations, metadata generation
- **Output**: Publication-ready formatted content

## 📊 Performance Metrics

### Typical Workflow Performance
- **Duration**: 3-8 minutes
- **Cost**: $0.50-2.00 per run
- **Output Quality**: Professional-grade content
- **Word Count**: 2000+ words (configurable)

### Resource Usage
- **API Calls**: ~15-25 per workflow
- **Memory**: <100MB
- **Storage**: ~1MB per output

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
SERPER_API_KEY=your-serper-key    # For enhanced web search
OPENAI_MODEL=gpt-4                # Default model
MAX_TOKENS=4000                   # Token limit per request
TEMPERATURE=0.7                   # Creativity level
```

### Agent Configuration (config/agents_config.py)
```python
AGENT_CONFIGS = {
    "researcher": {
        "model": "gpt-4",
        "max_execution_time": 300,
        "memory": True,
        "tools": ["web_search", "data_analysis"]
    },
    "writer": {
        "model": "gpt-4",
        "max_execution_time": 600,
        "memory": True,
        "creativity": 0.8
    }
    # ... more configurations
}
```

## 📈 Monitoring and Logging

### Built-in Monitoring
- Real-time progress tracking
- Agent performance metrics
- Cost tracking per workflow
- Error logging and recovery

### Log Files
```
outputs/logs/
├── workflow_YYYYMMDD_HHMMSS.log
├── agent_performance.log
├── error_reports.log
└── cost_analysis.log
```

### Monitoring Dashboard
```python
# Get workflow status
status = orchestrator.get_workflow_status()

# View metrics
metrics = orchestrator.get_performance_metrics()

# Cost analysis
costs = orchestrator.get_cost_analysis()
```

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
```bash
# Check .env file
cat .env | grep OPENAI_API_KEY

# Verify key format (should start with sk-)
```

**"Insufficient credits"**
- Add funds to OpenAI account
- Check billing dashboard
- Consider using GPT-3.5-turbo for lower costs

**"Rate limit exceeded"**
- Wait 60 seconds and retry
- Check OpenAI usage limits
- Consider upgrading API plan

**"Agent execution timeout"**
- Increase `max_execution_time` in config
- Simplify the task complexity
- Check internet connection for research tasks

### Debug Mode
```python
# Enable verbose logging
orchestrator = WorkflowOrchestrator(debug=True)

# Or use environment variable
export CREWAI_DEBUG=true
```

## 🧪 Testing

### Run All Tests
```bash
python test_setup.py
python -m pytest tests/ -v
```

### Test Individual Components
```bash
# Test agent creation
python -c "from workflow_orchestrator import WorkflowOrchestrator; w = WorkflowOrchestrator(); print('✅ Agents created successfully')"

# Test API connection
python -c "import openai; print('✅ OpenAI connection works')"
```

## 🚀 Deployment

### Local Development
```bash
# Install in development mode
pip install -e .

# Run with auto-reload
python run_workflow.py --dev
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt --no-dev

# Set production environment
export ENVIRONMENT=production

# Run with production config
python run_workflow.py --config production
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "run_workflow.py"]
```

## 📚 Examples

### Example 1: Basic Blog Post
```python
orchestrator = WorkflowOrchestrator()
results = orchestrator.run_workflow("Climate Change Technology")
```

### Example 2: Technical Documentation
```python
config = {
    "style": "technical",
    "include_code_examples": True,
    "target_audience": "developers"
}
results = orchestrator.run_workflow("API Design Best Practices", config)
```

### Example 3: Batch Processing
```python
topics = ["AI Ethics", "Quantum Computing", "Space Technology"]
for topic in topics:
    results = orchestrator.run_workflow(topic)
    print(f"✅ Completed: {topic}")
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repo-url>
cd crewai-workflow

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings to all functions
- Run `black` for formatting

### Testing
- Write tests for new features
- Ensure 90%+ code coverage
- Test with multiple OpenAI models

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework
- [OpenAI](https://openai.com) for the language models
- [Langchain](https://langchain.com) for the underlying AI tools

## 📞 Support

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: support@yourproject.com

---

**Made with ❤️ by Kato Ernest Henry**