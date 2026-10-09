# Dataset Stellarium para verificar las efemérides

Exportación independiente de Stellarium: cuerpos e intervalo de
[analysis_config.json](../analysis_config.json), un único par RA/Dec aparente
en equinoccio de fecha por instante, en grados decimales. No se exporta J2000.

El perfil utiliza Tierra y cálculo geocéntrico, sin atmósfera, con tiempo de luz,
aberración (factor 1) y nutación activados. Estas opciones se registran y validan.
Stellarium conserva sus propias efemérides y convenciones: el perfil es el más
cercano disponible aquí a apparent-of-date de Horizons, no una garantía de
igualdad exacta. La [API de objetos](https://stellarium.org/doc/head/classStelObject.html)
define `ra` y `dec` en el marco de fecha; las propiedades de corrección están
documentadas en [StelCore](https://stellarium.org/doc/head/classStelCore.html).

Los perfiles y exports anteriores con tiempo de luz/aberración desactivados
se rechazan. Ejecutar `prepare`, exportar de nuevo y después ejecutar `collect`;
no basta con cambiar las etiquetas de un dataset existente.

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

- `stellarium_ephemerides.jsonl`: dataset con procedencia explícita y sólo la referencia aparente de fecha.
- `comparison.csv`: comparación con TYCHOS, diferencias RA/Dec y separación angular.
- `report.md`, `report.json`: métricas por cuerpo, configuración, hashes y fechas.
- `stellarium_log.txt`, `stellarium_config.ini`: versión, motores y opciones de la ejecución.

Para el intervalo completo, ejecutar `prepare` sin `--stop`; toma inicio, final
inclusivo y paso de `scripts/analysis_config.json`. Puede tardar bastante:
con 75.969 fechas (paso de 3 h) y espera de 0,2 s son al menos unas cuatro horas,
además del cálculo.
No reducir la espera sin verificar primero que las coordenadas se actualizan.
Comparar un piloto con dos esperas distintas ayuda a detectar resultados obsoletos.

**El menor error no establece qué referencia es correcta.** Esta prueba evalúa una convención aparente explícita. El dataset no entra todavía en el pipeline
ML, que identifica sus etiquetas como JPL. Tampoco representa una observación
independiente: Stellarium calcula posiciones mediante sus propias efemérides,
que pueden compartir fuentes con JPL.

## Verificación

## Full reusable reference: 2000–2026, every 3 hours

The full profile is prepared in `scripts/stellarium/profile_2000_2026_3h/`,
separately from the successful one-month pilot. It covers **2000-06-21 00:00 UTC
through 2026-06-21 00:00 UTC**, inclusive: 75,969 timestamps and 759,690 positions
across ten bodies. At `--wait 0.2`, the wait alone takes 4.22 hours, plus computation.

To regenerate the profile if the analysis configuration changes:

```powershell
.venv/Scripts/python.exe -B scripts/stellarium/dataset.py prepare --profile scripts/stellarium/profile_2000_2026_3h
```

Close any previous export instance, then launch the full export in a visible window:

```powershell
$exportProfile = (Resolve-Path scripts/stellarium/profile_2000_2026_3h).Path
& 'C:/Program Files/Stellarium/stellarium.exe' --user-dir $exportProfile --startup-script export.ssc --full-screen no
```

After Stellarium finishes, validate and save the reference independently of TYCHOS:

```powershell
.venv/Scripts/python.exe -B scripts/stellarium/dataset.py collect --reference-only --profile scripts/stellarium/profile_2000_2026_3h --output data/stellarium
```

The saved reference contains `stellarium_ephemerides.jsonl`, `manifest.json`,
`reference_provenance.json`, and the available Stellarium log/configuration.
`--reference-only` refuses to replace an existing reference dataset.
Keep these files together. Reuse this reference for subsequent TYCHOS exports;
there is no need to run Stellarium again when only the TYCHOS model changes.

The maintained reference now lives directly in `data/stellarium/`.
Its large `stellarium_ephemerides.jsonl` is shared separately and ignored by Git;
the manifest, provenance, log and configuration remain trackable. After cloning,
restore the JSONL to `data/stellarium/stellarium_ephemerides.jsonl` before running
analysis. Alternatively use `--stellarium path/to/stellarium_ephemerides.jsonl`,
with its matching `manifest.json` beside it. Metadata does not replace the positions.
The old one-month pilot and nested `baseline_2000_2026_3h/` layout are no longer
the maintained reference.

The standard analysis command now accepts Stellarium:

```powershell
.venv/Scripts/python.exe -B scripts/run_analysis.py --source stellarium --all --label "Current TYCHOS settings"
```

It reads the saved reference path from `analysis_config.json`, requires every
reference timestamp in the TYCHOS export, and writes per-body comparison CSVs,
RA/Dec/angular metrics, annual statistics, FFT diagnostics and reports to
`reports/stellarium/`. It records the dataset hashes and Stellarium settings.
The standard JPL command continues to write to `reports/`.

For a controlled before/after comparison against the same Stellarium reference:

```powershell
.venv/Scripts/python.exe -B scripts/run_analysis.py --source stellarium --all --tychos 00-binary-baseline/tychos_ephemerides.txt --out-dir reports/stellarium-baseline --label "Binary baseline"
.venv/Scripts/python.exe -B scripts/run_analysis.py --source stellarium --all --out-dir reports/stellarium --label "Author tweaks"
.venv/Scripts/python.exe -B scripts/compare_summary_metrics.py --baseline reports/stellarium-baseline --candidate reports/stellarium moon jupiter saturn
```

The comparison tool rejects comparisons between different reference sources.
Machine learning still uses JPL; this change adds Stellarium to ephemeris analysis.

## Checks

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s scripts/stellarium -p "test_*.py"
```

Referencias: [API de scripting](https://stellarium.org/doc/head/classStelMainScriptAPI.html)
(`getObjectInfo`, `setPlanetocentricCalculations`, `saveOutputAs`) y
[guía de Stellarium](https://stellarium.org/guide/) (perfil y script de inicio).
La preparación original se realizó con Stellarium 26.2.0; consultar el log
de cada exportación para identificar la versión realmente utilizada.
