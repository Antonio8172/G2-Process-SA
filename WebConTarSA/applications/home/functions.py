import datetime

ahora = datetime.datetime.now()

class OperacionesFechas():
    def fecha_actual():
        fechaActual = ahora.date()
        return fechaActual

    def diferencia_dias(fechaFinal):
        diferenciaDias = fechaFinal - ahora.date()
        return diferenciaDias.days
    
    def porcentaje_actual(fechaInicio, fechaFinal):
        total = fechaFinal - fechaInicio  # 100 % en cantidad de días
        total = total.days
        actual = ahora.date() - fechaInicio # % actual en cantidad de días
        actual = actual.days
        if actual >= 0:
            if actual < total:
                porcActual = (actual*100)/total
            else:
                porcActual = 100
        else:
            porcActual = 0

        return int(porcActual)


class OperacionesPaginas():

    def calcular_indice_inicio(pagina):
        indicePagina = (pagina-1)*9
        return indicePagina
        
    def calcular_indice_final(pagina):
        indicePagina = (pagina)*9
        return indicePagina