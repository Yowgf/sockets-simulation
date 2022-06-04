import argparse

from client.client.client import Client
from common.log import log

logger = log.logger()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'host',
        action='store',
        type=str,
        help='Host'
    )
    parser.add_argument(
        'port',
        action='store',
        type=int,
        help='Port'
    )
    parser.add_argument(
        '-log-level',
        dest='log_level',
        action='store',
        required=False,
        type=str,
        help="logging level"
    )
    args = parser.parse_args()

    return args

def main():
    try:
        config = parse_args()
        if config.log_level != None:
            log.set_level(config.log_level)
        logger.info("Received config:\n{}".format(
            {
                "host": config.host,
                "port": config.port,
                "log_level": config.log_level,
            }
        ))
            
        client = Client(config)
        client.init()
        client.run()
    except Exception as e:
        logger.critical("Encountered fatal error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
