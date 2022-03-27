
#apriamo il file della cassylab ed inseriamo i dati nella variabile raw_data
with open("db3.txt", "r", encoding="utf-8-sig") as f:
        raw_data = f.read()

#divido in un array ogni riga del file dati
lines_array = raw_data.split("\n")

x_array = []
y_array = []
#divido i dati di ogni riga rispetto al tab space (\t)
for line in lines_array:
    value = line.split("\t")

    #elimino gli spazi vuoti di scarto e la colonna delle intensità
    del value[len(value)-2: len(value)]

    #inserisco i valori delle due colonne in due array 
    if len(value) == 2:
        x_array.append(value[0])
        y_array.append(value[1])

#definisco una funzione per convertire dalle virgole ai punti
#successivamente converto i valori da stringhe a numeri decimali(float)
def clean_array(input_array):
    output_array = []
    for item in input_array:
        item = item.replace(',', '.')
        item = float(item)
        output_array.append(item)
    return output_array

x_array, y_array = clean_array(x_array), clean_array(y_array)

#con x - t0 poniamo lo 0 quando incomincia la scarica del condensatore
t0 = min(x_array)
for index in range(len(x_array)):
    x_array[index] = x_array[index] - t0

########################################################################################################################################

import math
from scipy.optimize import curve_fit

#creo un nuovo array in cui ad ogni valore di y corrisponde ln(y)
work_array = []
for item in y_array:
    work_array.append(math.log(item))
    
#definisco la funzione che ipotiziamo aprossimi meglio i dati
#la trasformiamo in forma lineare appplicando il logaritmo naturale ad entrambi i membri
def fit_function(x, a, b):
    return b*(x) + math.log(a)

#troviamo i parametri con la funzione di SciPy curve_fit() in base ai dati laboratoriali
parameters, _ = curve_fit(fit_function, x_array, work_array)
a, b = parameters

########################################################################################################################################

import math
import matplotlib.pyplot as plt

#traccio il grafico dei dati laboratoriali
plt.plot(x_array, y_array, label = "dati laboratoriali")

#creo un array secondo la funzione trovata
y_fit = []
for x in x_array:
    y = a* ((math.e)**(b*x))
    y_fit.append(y)

#traccio il grafico della funzione trovata
plt.plot(x_array, y_fit, '--', color='red', label = f"esponenziale: a = {round(a, 5)}; b = {round(b, 5)}")

#modifiche grafiche
plt.xlim(min(x_array), max(x_array))
plt.ylim(0)
plt.grid()
plt.xlabel('tempo (s)')
plt.ylabel('differenza di potenziale (V)')
plt.title('Scarica di un condensatore')
plt.legend()
 
plt.show()

########################################################################################################################################

import numpy
import matplotlib.pyplot as plt
import matplotlib as ax

#creo un array con gli errori assoluti della funzione trovata rispetto a i dati laboratoriali
errors = []
for index in range(len(y_array)):
    error = y_fit[index] - y_array[index]
    errors.append(error)

#traccio il grafico dell'errore al passare del tempo
plt.plot(x_array, errors,'.', label = "errori")

#traccio la linea dello zero
plt.axhline(y = 0, color = 'black', linestyle = '--')

#traccio la linea della media
avarage = numpy.mean(errors)
plt.axhline(y = avarage, color = 'green', linestyle='--', label = f"errore medio: +{round(avarage, 5)}")

#modifiche grafiche
plt.xlim(min(x_array), max(x_array))
plt.ylim(-0.1, 0.5)
plt.yticks(list(plt.yticks()[0]) + [avarage])
plt.grid()
plt.xlabel('tempo (s)')
plt.ylabel('errori sulla differenza di potenziale (V)')
plt.title('Errori scarica di un condensatore')
plt.legend()

plt.show()

########################################################################################################################################

for i in range(len(x_array)):
    print(round(x_array[i], 5), round(y_array[i],5), sep="\t")

max_perc_err = (max(errors)/y_fit[errors.index(max(errors))])*100

print(f"Funzione: {a} * e ^ {b} * x")
print(f"Errore massimo : {max(errors)}")
print(f"Errore medio: {avarage}")
print(f"Errore percentuale massimo: {max_perc_err}%")