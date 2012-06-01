import logging

class Logs:
    pass

    def inicializarLogs():
        logger = logging.FileHandler('/home/usuario/ProyectoDesarrolloSoftware/misitio/misitio/logs/logs.log') #inicializacion para el manejo de logs
        logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logger.setFormatter(formatter)
