# NLP Tweets Sentiment Analysis DL Models

## Descripción

Este proyecto implementa un sistema de análisis de sentimientos utilizando modelos de Deep Learning para clasificar reseñas de películas de IMDB. El proyecto incluye preprocesamiento de texto, entrenamiento de múltiples arquitecturas de redes neuronales y evaluación de modelos.

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd NLP-Tweets-Sentiment-Analysis-DL-Models
```

### 2. Estructura de datos
Asegúrate de que existan las carpetas necesarias:
```
data/
workspace/data/
workspace/models/
workspace/models/checkpoint/
workspace/models/final/
```

### 3. Ejecutar con Docker

Para ejecutar el entrenamiento
```
docker-compose up --build
```

Eso abre un servidor en http://localhost:8888 donde puedes ver los notebooks de Jupyter. Ejecutar `app.ipnyb` con todas sus celdas.
Puede que los directorios de los datos den error, ajustar según sea necesario.

## Uso

### Acceder a Jupyter Notebook

1. Una vez iniciado el contenedor, abre tu navegador en: `http://localhost:8888`
2. Abre el notebook `app.ipynb`
3. Ejecuta las celdas secuencialmente

### Workflow del Proyecto

1. **Carga de datos**: Descarga automática del dataset IMDB si no existe
2. **Preprocesamiento**: Limpieza y normalización de texto
3. **Vectorización**: Conversión de texto a representación numérica con TF-IDF
4. **Entrenamiento**: Entrena múltiples modelos con diferentes arquitecturas
5. **Evaluación**: Compara métricas de rendimiento de los modelos
6. **Guardado**: Los modelos entrenados se guardan en `workspace/models/`

### Probar los Modelos Entrenados

Para probar los modelos con tus propias reseñas, puedes usar el script `test.py` dentro del mismo contenedor de Docker:

1. **Edita el archivo de pruebas**: Abre `workspace/user_test_reviews.txt` y escribe las reseñas que quieres analizar (una por línea)

2. **Ejecuta el script de prueba**: Accede al contenedor y ejecuta:
   ```bash
   docker exec -it <container_name> python workspace/test.py
   ```
   
   O si ya estás dentro del contenedor:
   ```bash
   cd workspace
   python test.py
   ```

3. **Resultados**: El script cargará cada modelo entrenado (baseline, model1, model2, model3) y predecirá el sentimiento (positivo/negativo) de cada línea del archivo `user_test_reviews.txt`

## Estructura del Proyecto

```
NLP-Tweets-Sentiment-Analysis-DL-Models/
├── docker-compose.yml          # Configuración de Docker Compose
├── Dockerfile                  # Imagen Docker con TensorFlow GPU
├── README.md                   # Este archivo
├── requirements.txt            # Dependencias de Python
├── data/                       # Datos originales
│   ├── raw.csv                # Dataset IMDB sin procesar
│   └── processed.csv          # Dataset preprocesado
└── workspace/                  # Directorio de trabajo
    ├── app.ipynb              # Notebook principal
    ├── test.py                # Script para probar modelos
    ├── user_test_reviews.txt  # Archivo con reseñas de prueba
    ├── data/                  # Enlace a datos
    └── models/                # Modelos entrenados
        ├── baseline.h5        # Modelo baseline
        ├── model1.h5          # Modelo 1
        ├── model2.h5          # Modelo 2
        ├── tfidf_vectorizer.joblib  # Vectorizador TF-IDF
        ├── checkpoint/        # Mejores modelos durante entrenamiento
        │   ├── best_baseline.h5
        │   ├── best_model1.h5
        │   ├── best_model2.h5
        │   └── best_model3.h5
        └── final/             # Modelos finales
            └── model3.h5
```

## Dependencias Principales

- **TensorFlow 2.15.0**: Framework de Deep Learning con soporte GPU
- **pandas**: Manipulación de datos
- **scikit-learn**: Vectorización TF-IDF y métricas
- **nltk**: Procesamiento de lenguaje natural
- **spaCy**: Lematización y tokenización avanzada
- **contractions**: Expansión de contracciones en inglés
- **datasets**: Carga del dataset IMDB de HuggingFace

Ver `requirements.txt` para la lista completa.

## Modelos Implementados

### Baseline Model
- Arquitectura simple con capas densas
- Entrada: Vector TF-IDF
- Salida: Clasificación binaria (positivo/negativo)

### Modelos Avanzados
- Embeddings de palabras
- Capas recurrentes (LSTM/GRU)
- Dropout para regularización
- Early stopping y model checkpointing

## Preprocesamiento de Texto

El pipeline de preprocesamiento incluye:
1. Normalización de codificación (unidecode)
2. Conversión a minúsculas
3. Expansión de contracciones ("don't" → "do not")
4. Eliminación de HTML tags y URLs
5. Eliminación de puntuación (conservando ! y ?)
6. Lematización con SpaCy
7. Eliminación de stopwords
8. Limpieza de espacios en blanco

