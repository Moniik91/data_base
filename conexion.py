import psycopg_pool
from logger_base import log
from psycopg_pool import ConnectionPool
import sys

class Conexion:
    _DATABASE = 'test_db'
    _USERNAME = 'postgres'
    _PASSWORD = 'Chaos2022'
    _DB_PORT = '5432'
    _HOST = '127.0.0.1'
    #definir variables, que indiquen numero minimo y maximo de conexiones
    _MIN_CON = 1
    _MAX_CON = 5
    _pool = None

    @classmethod
    def obtenerPool(cls):
        if cls._pool is None:
            try:
                # Crear el string de conexión con todos los parámetros
                conninfo = (f"host={cls._HOST} user={cls._USERNAME} password={cls._PASSWORD} "
                            f"port={cls._DB_PORT} dbname={cls._DATABASE}")

                # Crear el pool de conexiones
                cls._pool = psycopg_pool.ConnectionPool(
                    conninfo=conninfo,
                    min_size=cls._MIN_CON,
                    max_size=cls._MAX_CON)
                log.debug(f'Creación del pool exitoso:{cls._pool}')
                return(cls._pool)
                #print("Pool creado con éxito")
            except Exception as e:
                log.error(f"Error al crear el pool de conexiones: {e}")
                sys.exit()
        else:
            return cls._pool

    @classmethod
    def obtenerConexion(cls):
        conexion = cls.obtenerPool().getconn()
        log.debug(f'Conexion obtenida del pool: {conexion}')
        return conexion

    @classmethod
    def liberarConexion(cls, conexion):
        #regresar el objeto conexion que ya no se esta usando
        cls.obtenerPool().putconn(conexion)
        log.debug(f'Regresamos la conexion al pool: {conexion}')

    @classmethod
    def cerrarConexiones(cls):
        cls.obtenerPool().closeall()

if __name__ == '__main__':
    conexion1= Conexion.obtenerConexion()
    Conexion.liberarConexion(conexion1)
    conexion2= Conexion.obtenerConexion()
    # conexion3= Conexion.obtenerConexion()
    # conexion4= Conexion.obtenerConexion()
    # conexion5= Conexion.obtenerConexion()
    # conexion6= Conexion.obtenerConexion()
    # conexion7= Conexion.obtenerConexion()
