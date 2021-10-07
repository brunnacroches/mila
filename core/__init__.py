
<<<<<<< Updated upstream
=======
   

>>>>>>> Stashed changes

# python get time and minute on GOOGLE
# https://stackoverflow.com/questions/30071886/how-to-get-current-time-in-python-and-break-up-into-year-month-day-hour-minu
# COPY : 
# import datetime
# now = datetime.datetime.now()
# print(now.year, now.month, now.day, now.hour, now.minute, now.second)

import datetime

# A class to return system info.
class SystemInfo: #nova classe adicioanda
    def __init__(self): # e essa classe vai retornar a hora
        pass

    # para fazer a instancia dessa classe : 
    @staticmethod
    def get_time():
        now = datetime.datetime.now()
        # estruturando uma resposta
        answer = 'São {} horas e {} minutos.'.format(now.hour, now.minute)
        return answer
