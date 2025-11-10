
import oracledb

class OracleDB:
    def __init__(self, user, password, dsn):
        self.user = user
        self.password = password
        self.dsn = dsn
        self.connection = self._connect()

    def _connect(self):
        return oracledb.connect(
            user=self.user,
            password=self.password,
            dsn=self.dsn
        )
