# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Agregado

- Inicialización del proyecto con estructura de carpetas y archivos básicos.
- Clase `Player` con atributos `name` y `color`.
- Clase `Checkers` con atributo `owner`.
- Clase `Board` con inicialización de puntos, bar, off_board, y métodos básicos.
- Clase `AIPlayer` con lógica básica para movimientos válidos y evaluación.
- CLI básico con menú para Humano vs IA y Humano vs Humano.
- Tests iniciales para `Board`, `Player`, `Checkers`.
- Lógica de movimientos normales, hits, bar priority.
- Lógica de bear-off para retirar fichas.
- Soporte para dados con `roll_dice`.
- IA que elige movimientos básicos.
- Opción para posiciones iniciales randomizadas o estándar en `Board.__init__` con parámetro `random_positions`.
- Opción "retirar" en CLI para humanos, permitiendo elegir ficha para bear-off desde las últimas 6 casillas.
- Feedback en CLI para movimientos de IA y confirmación de fichas retiradas.
- Lógica exacta para bear-off: el dado debe ser exactamente la distancia requerida para retirar.
- Soporte completo para bear-off en IA y humanos, con verificación de victoria al retirar 15 fichas.

### Cambiado

- `roll_dice` en `Board` para devolver exactamente 2 dados en lugar de importar de `core.dice`.
- `_get_valid_moves` en `AIPlayer` para incluir movimientos de bear-off.
- `_play_human_turn` en CLI para manejar opción "retirar" y calcular bear-off automáticamente.

### Corregido

- Tests para usar `random_positions=False` en `Board` para posiciones estándar.
- `is_valid_move` para bear-off exacto (`die == required_die`) en lugar de `die >= required_die`.
- `test_roll_dice` para esperar 2 dados.
- `test_is_valid_move_bar_priority_white` para usar dado válido para bar.
- Importaciones en `test_board.py` agregando `import unittest`.
- Lógica de `__deepcopy__` en `DummyBoard` para tests de IA.

### Removido

- Dependencia de `core.dice` en `board.py`, usando `random` directamente.
