import os
import sys
import logging
from dotenv import load_dotenv
from studocu_client import StudocuClient
from bot import main as bot_main

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = ['TELEGRAM_BOT_TOKEN', 'STUDOCU_EMAIL', 'STUDOCU_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please check your .env file and ensure all required variables are set.")
        return False
    return True

def test_studocu_login():
    """Test Studocu login credentials."""
    try:
        client = StudocuClient(
            email=os.getenv('STUDOCU_EMAIL'),
            password=os.getenv('STUDOCU_PASSWORD')
        )
        if client.login():
            logger.info("Successfully authenticated with Studocu")
            return True
        else:
            logger.error("Failed to authenticate with Studocu. Please check your credentials.")
            return False
    except Exception as e:
        logger.error(f"Error testing Studocu login: {str(e)}")
        return False

def main():
    """Main entry point of the application."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Check environment variables
        if not check_environment():
            sys.exit(1)
            
        # Test Studocu login
        if not test_studocu_login():
            sys.exit(1)
            
        # Start the bot
        logger.info("Starting Telegram bot...")
        bot_main()
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
