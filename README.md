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

Luego abre `http://localhost:5000` en tu navegador. Podrás seleccionar un día y ver los ejercicios con casillas para marcar cada uno como realizado. El estado se guarda en `state.txt`.

La página muestra un contador con el tiempo total transcurrido y botones para iniciar un cronómetro de descanso de 1 minuto o 1 minuto y 30 segundos.

Al comenzar la rutina puedes pulsar **Finalizar Rutina** para detener el contador. Se mostrará el porcentaje de ejercicios completados y el tiempo total invertido y se reiniciará el estado del día.
