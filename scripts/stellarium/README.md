# Dataset Stellarium para verificar las efemérides

Exportación independiente de Stellarium: diez cuerpos según [analysis_config.json](../analysis_config.json),
dos pares de coordenadas por fecha (J2000 y equinoccio de la fecha), grados decimales.
No se modifica TYCHOS ni se reemplaza el TXT de JPL. No se presentan coordenadas
Stellarium como si fueran datos astrométricos ICRF de Horizons.

El perfil de exportación usa Tierra, cálculo planetocéntrico (geocéntrico),
tiempo detenido, sin atmósfera, sin tiempo de luz y sin aberración. Esto es un
experimento geométrico, distinto de la vista observacional habitual de Stellarium.
Las RA/Dec de la fecha incluyen las convenciones de orientación de Stellarium;
no deben identificarse automáticamente con las coordenadas de TYCHOS.

## Ejecutar desde la raíz del repositorio

Este flujo pertenece al repositorio independiente `tychos-research`. Preparar
Python 3.11 o posterior y NumPy con los comandos del [README principal](../../README.md).
Stellarium debe estar instalado por separado; adaptar la ruta del ejecutable
al equipo utilizado. Los exports de TYCHOS se producen en el simulador externo.


Primero preparar un mes de prueba, con el paso y cuerpos del JSON de análisis:

```powershell
.venv/Scripts/python.exe -B scripts/stellarium/dataset.py prepare --stop "2000-07-21 00:00" --wait 0.2
# Alternativa: usar otro intervalo y un perfil separado.
.venv/Scripts/python.exe -B scripts/stellarium/dataset.py prepare --start "2025-06-21 00:00" --stop "2025-07-21 00:00" --wait 0.2 --profile scripts/stellarium/profile_2025
```

Abrir una instancia de Stellarium **con ventana visible** y perfil separado.
En esta instalación, la ejecución oculta devolvió coordenadas sin actualizar:
no usarla para producir referencias. El siguiente comando es para ejecución
interactiva por el usuario:

```powershell
$exportProfile = (Resolve-Path scripts/stellarium/profile).Path
& 'C:/Program Files/Stellarium/stellarium.exe' --user-dir $exportProfile --startup-script export.ssc --full-screen no
```

Si se usa `--profile`, pasar la misma carpeta al comando de Stellarium y a
`collect --profile`; el ejemplo siguiente usa el perfil predeterminado.

Esperar a que el script termine. Produce `profile/stellarium_export.jsonl` con
una marca final `complete`; la mera existencia del archivo no prueba una exportación
nueva. Antes de repetir, cerrar la instancia anterior y usar un perfil nuevo
(`--profile`) para conservar los resultados anteriores si son necesarios.

```powershell
.venv/Scripts/python.exe -B scripts/stellarium/dataset.py collect
```

La recolección valida cobertura exacta del intervalo solicitado, cuerpos, fechas,
coordenadas finitas, duplicados, opciones de cálculo y posiciones consecutivas
idénticas que indicarían falta de actualización. TYCHOS puede tener un intervalo
mayor, pero debe contener cada instante solicitado; no se interpola.

Se guardan en `data/stellarium/`:

- `stellarium_ephemerides.jsonl`: dataset con procedencia explícita y ambas referencias.
- `comparison.csv`: comparación con TYCHOS, diferencias RA/Dec y separación angular.
- `report.md`, `report.json`: métricas por cuerpo, configuración, hashes y fechas.
- `stellarium_log.txt`, `stellarium_config.ini`: versión, motores y opciones de la ejecución.

Para el intervalo completo, ejecutar `prepare` sin `--stop`; toma inicio, final
inclusivo y paso de `scripts/analysis_config.json`. Puede tardar bastante:
con 75.969 fechas (paso de 3 h) y espera de 0,2 s son al menos unas cuatro horas,
además del cálculo.
No reducir la espera sin verificar primero que las coordenadas se actualizan.
Comparar un piloto con dos esperas distintas ayuda a detectar resultados obsoletos.

**El menor error no establece qué referencia es correcta.** Esta prueba permite
comparar dos convenciones explícitas. El dataset no entra todavía en el pipeline
ML, que identifica sus etiquetas como JPL. Tampoco representa una observación
independiente: Stellarium calcula posiciones mediante sus propias efemérides,
que pueden compartir fuentes con JPL.

## Verificación

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s scripts/stellarium -p "test_*.py"
```

Referencias: [API de scripting](https://stellarium.org/doc/head/classStelMainScriptAPI.html)
(`getObjectInfo`, `setPlanetocentricCalculations`, `saveOutputAs`) y
[guía de Stellarium](https://stellarium.org/guide/) (perfil y script de inicio).
La preparación original se realizó con Stellarium 26.2.0; consultar el log
de cada exportación para identificar la versión realmente utilizada.
