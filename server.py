import uvicorn
import sys
import signal
import logging
import os
import asyncio
from main import app
# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/server.log")
    ]
)

# Global server config
server_config = {
    "should_exit": False
}

def signal_handler(sig, frame):
    logging.info("Initiating graceful shutdown...")
    server_config["should_exit"] = True

def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Default configuration
    host = "127.0.0.1"
    port = 8496
    
    logging.info(f"Starting server on {host}:{port}")
    
    try:
        # Configure uvicorn logging
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
        log_config["handlers"]["default"]["stream"] = sys.stdout

        config = uvicorn.Config(
            "main:app",
            host=host,
            port=port,
            reload=False,
            log_config=log_config,
            access_log=True
        )
        
        server = uvicorn.Server(config)
        server.run()
            
    except Exception as e:
        logging.error(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
