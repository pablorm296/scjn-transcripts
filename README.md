# Proyecto de Extracción y Estandarización de Transcripciones de la SCJN

Este repositorio almacena el código y los recursos necesarios para la extracción, limpieza y estandarización de las transcripciones estenográficas de las sesiones de la Suprema Corte de Justicia de la Nación (SCJN).

- [1. Descripción](#1-descripción)
- [2. Configuración](#2-configuración)
- [3. Requisitos](#3-requisitos)
- [4. Uso](#4-uso)
- [5. Contenido del repositorio](#5-contenido-del-repositorio)
- [6. Estado del Proyecto](#6-estado-del-proyecto)
- [7. Contribuciones](#7-contribuciones)
- [8. Licencia](#8-licencia)

## 1. Descripción
El objetivo de este proyecto es desarrollar herramientas que permitan procesar de manera eficiente las transcripciones de la SCJN, asegurando que la información resultante sea clara, estructurada y utilizable para análisis posteriores. Esto incluye:
- **Extracción de datos** desde diferentes fuentes.
- **Limpieza y normalización** de los textos.
- **Estandarización del formato** para facilitar su análisis y visualización.

## 2. Configuración

Este proyecto utiliza **variables de entorno** y un archivo `.env.local` para gestionar la configuración.

El sistema de configuración está diseñado para que las **variables de entorno** tengan **preferencia** sobre el contenido del archivo `.env.local`. Esto significa que si una variable está definida tanto en el entorno del sistema como en el archivo `.env.local`, se utilizará la del entorno.

En el archivo `.env.example` se encuentran las variables de entorno necesarias para la configuración del proyecto, a saber:

```bash
# Archivo .env.example
EXTRACTOR_HOST="https://bj.scjn.gob.mx"             # Host de la API del buscador de la SCJN.
EXTRACTOR_PATH_SEARCH="/api/buscador/busqueda"      # Ruta del endpoint de búsqueda.
```

## 3. Requisitos

1. Este proyecto fue desarrollado y probado en Python 3.13. Se recomienda utilizar un entorno virtual para gestionar las dependencias y evitar conflictos con otros proyectos. Si no tienes instalado Python 3.13, puedes descargarlo desde la [página oficial](https://www.python.org/downloads/) o instalarlo a través de un gestor de versiones, como [pyenv](https://github.com/pyenv/pyenv) o [Anaconda](https://www.anaconda.com/products/distribution).

## 4. Uso

## 5. Contenido del repositorio

```plaintext
.
└── prototypes  # Prototipos y pruebas de concepto.
```

## 6. Estado del Proyecto
Este es un trabajo en progreso. Se están desarrollando y probando diferentes estrategias para optimizar la calidad de los datos procesados. Conforme se agreguen nuevas características y mejoras, este README será actualizado.

## 7. Contribuciones
Por el momento, el proyecto es de uso personal, pero en el futuro podrían abrirse oportunidades para contribuciones externas.

## 8. Licencia
Por definir.
