import QTLogin
import QTGraffiti

from exceptions import NoConfigError

import logging
import logging.config
logging.config.fileConfig("logging.ini")


try:
    QTGraffiti.main()
except NoConfigError:
    QTLogin.main()
except Exception as e:
    logging.error(f"Something went wrong: {e}")
