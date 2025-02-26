# Proyecto de Extracción y Estandarización de Transcripciones de la SCJN

Este proyecto tiene como objetivo la creación de un corpus de transcripciones estenográficas de las sesiones de la Suprema Corte de Justicia de la Nación (SCJN), con el fin de facilitar su análisis y exploración.

- [1. Descripción](#1-descripción)
- [2. Instalación](#2-instalación)
  - [2.1. Configuración de bases de datos](#21-configuración-de-bases-de-datos)
- [3. Uso](#3-uso)
  - [3.1. Recolección de transcripciones](#31-recolección-de-transcripciones)
- [4. Detalles técnicos](#4-detalles-técnicos)
  - [4.1. Extracción](#41-extracción)
- [5. Estado del Proyecto](#5-estado-del-proyecto)
- [6. Contribuciones](#6-contribuciones)
- [7. Licencia](#7-licencia)

## 1. Descripción

El proyecto tiene como objetivo principal la creación de un corpus de transcripciones estenográficas de las sesiones de la SCJN. Este repositorio contiene el código necesario para la extracción, limpieza y estandarización de las transcripciones.

El proyecto implementa las siguientes características:
1. Extracción de transcripciones de la SCJN: Se extraen las transcripciones de las sesiones de la SCJN usando la API del buscador jurídico de la SCJN.
2. Limpieza de transcripciones: Su contenido se almacena en texto plano, usando Markdown para facilitar su lectura y análisis.

## 2. Instalación

Para instalar este paquete desde el repositorio, puedes usar el siguiente comando:

```bash
pip install git+https://github.com/pablorm296/scjn-transcripts.git
```

### 2.1. Configuración de bases de datos

El proyecto utiliza una base de datos MongoDB para almacenar las transcripciones y una base de datos Redis como caché para saber qué documentos ya han sido procesados y poder recuperar el ciclo de extracción en caso de un error inesperado.

Para configurar la conexión a las bases de datos, el proyecto usa un archivo `.env.local`. Puedes encontrar un ejemplo de este archivo en `.env.example`.

Si deseas usar una base de datos local, se incluye un archivo `docker-compose.yml` para configurarlo. Puedes iniciar los servicios de MongoDB y Redis con el siguiente comando:

```bash
docker-compose up -d
```

Asegúrate de configurar las variables de entorno en tu archivo `.env.local` para que apunten a las instancias locales de MongoDB y Redis.

## 3. Uso

### 3.1. Recolección de transcripciones

Para iniciar el proceso de recolección (_scrapping_) de transcripciones, puedes utilizar el comando `collect` proporcionado por la interfaz de línea de comandos (CLI). A continuación se muestra un ejemplo de cómo usar este comando:

```bash
scjn_transcripts collect --verbose --ignore-page-cache
```

Opciones disponibles:
- `--verbose` o `-v`: Aumenta la verbosidad del registro para obtener más detalles durante la ejecución.
- `--ignore-page-cache` o `-i`: Ignora la caché de la última página solicitada y comienza desde la primera página.

## 4. Detalles técnicos

### 4.1. Extracción

El proceso de extracción de las versiones estenográficas de la SCJN se implementa en `scjn_transcripts.collector.transcripts`, específicamente en `ScjnSTranscriptsCollector.collect`. A continuación se presenta un diagrama de flujo que detalla el algoritmo de descarga de los documentos:

```mermaid
graph TD
    A[Inicio] --> B[Inicializar clientes de DB y cache]
    B --> C[Obtener página de búsqueda desde cache]
    C --> D[Inicializar variables del colector]
    D --> E[Solicitar página de búsqueda]
    E --> F[Parsear respuesta de búsqueda]
    F --> G{¿Primera página?}
    G -- Sí --> H[Establecer total de ítems y páginas]
    H --> I[Iterar sobre resultados de búsqueda]
    G -- No --> I[Iterar sobre resultados de búsqueda]
    I --> J[Obtener detalles del documento]
    J --> K[Verificar y establecer transcripción]
    K --> L{¿Documento existe en DB?}
    L -- No --> M[Guardar documento en DB]
    M --> N[Guardar digest en cache]
    N --> S[Incrementar página y solicitudes]
    L -- Sí --> O{¿Documento ha cambiado?}
    O -- No --> P[Continuar]
    P --> S[Incrementar página y solicitudes]
    O -- Sí --> Q[Actualizar documento en DB]
    Q --> R[Actualizar digest en cache]
    R --> S[Incrementar página y solicitudes]
    S --> T{¿Última página?}
    T -- No --> E
    T -- Sí --> U[Fin]
```

## 5. Estado del Proyecto
Este es un trabajo en progreso. Se están desarrollando y probando diferentes estrategias para optimizar la calidad de los datos procesados. Conforme se agreguen nuevas características y mejoras, este README será actualizado.

## 6. Contribuciones
Por el momento, el proyecto es de uso personal, pero en el futuro podrían abrirse oportunidades para contribuciones externas.

## 7. Licencia
Por definir.
