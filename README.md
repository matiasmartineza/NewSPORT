# Rutina de Ejercicios

Aplicación web sencilla para visualizar y marcar como realizados los ejercicios de la rutina definida en `rutina.json`.

## Requisitos

- Python 3
- Flask (ver `requirements.txt`)

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación con:

```bash
python app.py
```

Luego abre `http://localhost:5000` en tu navegador. Al ingresar se te pedirá un nombre de usuario. Cada nombre mantiene su propio progreso en `state.txt` y no afecta al de otros usuarios. Después de identificarte podrás seleccionar un día y ver los ejercicios con casillas para marcar cada uno como realizado.

La página muestra un contador con el tiempo total transcurrido y botones para iniciar un cronómetro de descanso de 1 minuto o 1 minuto y 30 segundos.

Al finalizar la rutina pulsa **Finalizar Rutina**. Se mostrará una pantalla de
resumen con tu nombre, el tiempo invertido y el porcentaje completado junto a
un gráfico de los grupos musculares trabajados. El gráfico incluye su leyenda
para una lectura clara y está generado con Chart.js.

No es necesario instalar nada adicional para el gráfico ya que Chart.js se
carga desde una CDN.

## Concurrencia

Las lecturas y escrituras sobre `state.txt` usan un bloqueo de archivo
(`filelock`) para evitar corrupciones cuando hay múltiples peticiones.
Si despliegas la aplicación en varias instancias debes asegurarte de que
comparten el mismo sistema de archivos y el archivo de bloqueo; de lo
contrario cada copia podría sobrescribir los datos de otra.
