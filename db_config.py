# db_config.py
class DatabaseConfig:
    SERVER = 'MARIAMGHAREEB'
    DATABASE = 'World_OF_Food'
    DRIVER = '{ODBC Driver 17 for SQL Server}'
    
    @classmethod
    def get_connection_string(cls):
        return (
            f"DRIVER={cls.DRIVER};"
            f"SERVER={cls.SERVER};"
            f"DATABASE={cls.DATABASE};"
            f"Trusted_Connection=yes;"
        ) 