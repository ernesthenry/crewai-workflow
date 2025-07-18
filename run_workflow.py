from workflow_orchestrator import WorkflowOrchestrator

def main():
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_workflow("Machine Learning in Healthcare")
    print(f"Workflow completed: {result['success']}")

if __name__ == "__main__":
    main()