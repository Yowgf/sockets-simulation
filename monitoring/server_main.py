import argparse

from server.server.server import Server
from common.log import log

logger = log.logger()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'ipver',
        action='store',
        type=str,
        help='IP version'
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
                "ipver": config.ipver,
                "port": config.port,
                "log_level": config.log_level,
            }
        ))
            
        server = Server(config)
        server.init()
        server.run()
    except Exception as e:
        logger.critical(f"Encountered fatal error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
