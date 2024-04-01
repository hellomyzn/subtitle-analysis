"""Entry point"""
#########################################################
# Builtin packages
#########################################################
# (None)

#########################################################
# 3rd party packages
#########################################################
# (None)

#########################################################
# Own packages
#########################################################
from common.log import initialize_logger
from controllers import SubtitleController


def main():
    """main"""
    initialize_logger()
    controller = SubtitleController()
    controller.add()


if __name__ == "__main__":
    main()
