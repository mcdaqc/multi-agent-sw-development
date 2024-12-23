from agents.collector_agent import RequirementCollector
from agents.generator_agent import CodeGenerator
from agents.validator_agent import CodeValidator
from agents.coordinator_agent import TaskCoordinator
from utils.firecrawl_wrapper import FirecrawlWrapper
from utils.nemo_utils import NeMoUtils
from utils.security import SecurityManager
from utils.rag_manager import RAGManager
from utils.logger import LogManager
from pathlib import Path

def main():
    # Initialize logging
    logger = LogManager(Path("data/logs")).get_logger(__name__)
    
    try:
        # Initialize components
        collector = RequirementCollector()
        generator = CodeGenerator()
        validator = CodeValidator()
        coordinator = TaskCoordinator()
        rag_manager = RAGManager()
        security_manager = SecurityManager()
        
        # Initialize utilities
        firecrawl = FirecrawlWrapper()
        nemo_utils = NeMoUtils()

        # Step 1: Collect Requirements
        user_requirements = collector.collect_requirements()

        # Step 2: Gather relevant data
        data = firecrawl.scrape_data(user_requirements)

        # Step 3: Process data with NeMo
        structured_data = nemo_utils.process_data(data)

        # Step 4: Generate Code
        generated_code = generator.generate_code(user_requirements, structured_data)

        # Step 5: Validate Code
        validation_results = validator.validate_code(generated_code)

        # Step 6: Handle validation results
        if not validation_results['valid']:
            coordinator.reassign_task(generator, validation_results['errors'])
        else:
            coordinator.provide_feedback(generated_code)

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main() 