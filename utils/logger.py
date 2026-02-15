import logging
import os
from datetime import datetime

def setup_logger():
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"test_run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
    )

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file,mode="w"), #Saves logs to file
            logging.StreamHandler() #Prints logs in console
        ]
    )
    #This gives you a logger object so you can use: context.logger.info("Test started")
    return logging.getLogger()


#Log Levels Explained
#logger.debug("For developers")
#logger.info("General info")
#logger.warning("Something unexpected")
#logger.error("Test failed")
#logger.critical("System crash")

#Typical automation framework uses:
#INFO → normal flow
#ERROR → failures
#DEBUG → deep troubleshooting

