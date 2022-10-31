# Proyecto Hilos
Proyecto de Hilos para la materia de Programación de Sistemas

# Introducción
## Cinepolis busca una solución para que los empleados de sus sucursales puedan mostrar las portadas de las peliculas dentro del cine.  El programa deberá cumplir con los siguientes requisitos.
- Permitir buscar varias películas al mismo tiempo.
- Tiene que funcionar a través de una interfaz gráfica sencilla.
- Para realizar la busqueda se tiene que hacer uso de hilos para agilizar los tiempos.
- Debera mostrar varios resultados por cada nombre de película ingresada para que el empleado pueda escoger el adecuado.
- Además al mostrar las imagenes de las películas si se da clic en ella, se deberán mostrar algunos datos relevantes de la película.

# Metodología
#### Programación Concurrente
Para definirla correctamente, debemos diferencias entre programa
y proceso.
- Programa: Conjunto de sentencias/instrucciones que se ejecutan
secuencialmente. Se asemeja al concepto de clase dentro de la POO.
Es por tanto un concepto estático.
- Proceso: Básicamente, se puede definir como un programa en
ejecución. Líneas de código en ejecución de manera dinámica. Se
asemeja al concepto de objeto en POO.

Se utilizara programación concurrente para realizar los procesos de las consultas en un menor tiempo. Para obtener velocidad en la ejecución del programa

La concurrencia aparece cuando dos o más procesos son contemporáneos. Un caso particular es el paralelismo (programación paralela).

La programación concurrente se encarga del estudio de las nociones de ejecución concurrente, así como sus problemas de comunicación
y sincronización.

#### Aspectos teoricos de hilos
Un hilo es un proceso del sistema operativo con características distintas de las de un proceso normal:

- Los hilos existen como subconjuntos de los procesos.
- Los hilos comparten memoria y recursos.
- Los hilos ocupan una dirección diferente en la memoria
##### Creación de hilos
Para la utilización de hilos en **Python** primero se debe de crear el hilo o la lista de hilos en cuestión. 

  **Hilo**. 

  ```python
     thread = threading.Thread(target=foo, args=(7, 'Hello World'))
     thread.start()
     thread.join()
  ```
  
  
  **Lista de hilos**. 
  
  
  ```python
  thread_lst = [threading.Thread(target=foo) for i in range(5)]

  for i in thread_lst:
    i.start()

  for i in thread_lst:
    i.join()
    print('return')
  ```
