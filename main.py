import QTLogin
import QTGraffiti

from exceptions import NoConfigError


try:
    QTGraffiti.main()
except NoConfigError:
    QTLogin.main()
