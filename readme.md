# Proyecto Integragrador MLOps . Sistema de Recomendación para Usuarios de la plataforma de videojuegos Steam


## Descripcion de la problematica :

La presente investigación aborda la problemática de implementar un modelo de recomendación de videojuegos en un entorno real. El ciclo de vida de este proyecto, caracterizado por su complejidad, involucra etapas que van desde la adquisición y preprocesamiento de datos hasta el entrenamiento, evaluación y despliegue del modelo, con el objetivo de superar los desafíos inherentes a la traducción de un sistema de recomendación de un entorno controlado a un contexto dinámico y en constante evolución."

## contexto :

Nuestro estudio se centra en el desarrollo de un sistema de recomendación de videojuegos personalizado para la plataforma Steam, con el fin de optimizar la experiencia del usuario y fomentar el descubrimiento de nuevos títulos.

## Rol a Desarrollar :

En este proyecto, asumimos el rol dual de Data Scientist y MLOps Engineer para llevar a cabo una transformación integral de los datos no estructurados de Steam. Nuestro objetivo principal consiste en diseñar y desarrollar un sistema de recomendación robusto y eficiente, partiendo desde una base de datos sin procesar.

## Descripción del proyecto :

#### Trabajamos con los siguientes conjuntos de datos obtenidos:

*Reseñas de usuarios australianos

*elementos_de_usuarios_australianos

*salida_de_juegos_de_steam

#### Tranformaciones :

Durante la fase de transformación del proceso ETL, se llevó a cabo una desnormalización de los datos. Ciertas columnas, que originalmente contenían estructuras anidadas como diccionarios o listas, fueron expandidas para obtener una representación tabular más plana. Esta transformación fue necesaria para facilitar las posteriores consultas a las APIs, las cuales requieren datos estructurados en un formato específico.

En la etapa de transformación del proceso ETL, se llevó a cabo un análisis exhaustivo de la calidad de los datos en las columnas 'title' y 'app_name'. Este análisis consistió en un conteo de los registros que presentaban valores nulos en dichas columnas, así como en la localización precisa de aquellos registros donde el valor de 'app_name' era nulo. Tras esta evaluación, se procedió a la eliminación de las primeras 88.310 filas del DataFrame, debido a que se constató que todos los registros en este rango contenían valores nulos en todas sus columnas, lo cual comprometía la integridad y confiabilidad de los datos subsiguientes.

Se realizó tambien una transformación de los datos de tipo fecha a formato datetime, con el propósito de facilitar la extracción del año como una unidad de análisis independiente.

#### Analisis de Sentimientos :

Se llevó a cabo un análisis de sentimiento utilizando técnicas de Procesamiento del Lenguaje Natural (PLN) sobre la columna 'user_reviews'. Los resultados de este análisis se emplearon para crear una nueva columna denominada 'sentiment_analysis', la cual reemplazó a la original. La escala utilizada para clasificar los sentimientos fue la siguiente: negativo (0), neutral (1) y positivo (2).

#### Desarrollo de la API :

Se ha implementado una interfaz de programación de aplicaciones (API) basada en el framework FastAPI para facilitar el acceso y la consulta de los datos corporativos. A través de esta API, se exponen las siguientes operaciones de consulta:

#### Desarrollador:

Retorna la cantidad total de elementos y el porcentaje de contenido gratuito por año, filtrados por una determinada empresa desarrolladora.

#### Usuario:

Proporciona información detallada sobre un usuario específico, incluyendo el gasto total, el porcentaje de recomendación basado en las reseñas y la cantidad de artículos adquiridos.

#### Género: 

Identifica al usuario con mayor tiempo de juego acumulado para un género dado, así como una lista detallada de las horas jugadas por año de lanzamiento.

#### Mejor desarrollador por año:

Determina los tres principales desarrolladores cuyos juegos han recibido las mejores valoraciones por parte de los usuarios en un año específico.

#### Análisis de sentimiento por desarrollador:

Proporciona un resumen de las reseñas de usuarios para una desarrolladora determinada, categorizando las opiniones en positivas y negativas.

#### Exhibicion :

Se emplea la plataforma Render para desplegar la API, permitiendo así su acceso y consumo a través de solicitudes web.

#### Analisis Exploratorio de los Datos :

Se aplicaron técnicas de análisis exploratorio de datos (EDA) al conjunto de datos con el fin de visualizar, describir y resumir la información contenida en él, permitiendo así identificar patrones, tendencias y anomalías.

#### Modelo de Aprendizaje :

Se diseñó e implementó un modelo de recomendación de tipo ítem-ítem en un contexto de aprendizaje automático. Con el fin de adecuar el modelo a las restricciones de la API, se procedió a una reducción del conjunto de datos, limitando la matriz de interacción a un 20% de su tamaño original. A continuación, se calculó una matriz de similitud basada en características como la fecha de lanzamiento y los géneros de los juegos, con el objetivo de identificar aquellos títulos más afines. Finalmente, se desarrolló una función de recomendación que, a partir del identificador de un juego determinado, retorna una lista de cinco títulos similares, seleccionados en función de los resultados obtenidos en la matriz de similitud.

## Datos y Fuentes :

Los datos empleados en este proyecto fueron obtenidos del conjunto de datos propuesto.

## Requisitos :

*Python 3.7 o superior.

*fastapi.

*uvicorn.

*scikit-learn.

## Autora :

Este proyecto fue realizado por: Nadia Scolese .
