from vgu import QTLogin
from vgu import QTGraffiti
from vgu.exceptions import NoConfigError

import logging
import logging.config
logging.config.fileConfig("logging.ini")


try:
    QTGraffiti.main()
except NoConfigError:
    QTLogin.main()
except Exception as e:
    logging.error(f"Something went wrong: {e}")
