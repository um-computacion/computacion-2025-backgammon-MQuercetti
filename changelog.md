# Changelog

- Se inició el desarrollo siguiendo los principios SOLID y el método TDD, documentando cada prompt y respuesta.
- Se propuso e implementó la clase Board, encargada de gestionar el estado del tablero y la lógica de movimiento de fichas según las reglas de Backgammon.
- Se detalló la lógica para que los movimientos dependan de los dados y de la ocupación de los puntos, incluyendo el manejo de dobles.
- Se documentó y mejoró la clase Checkers, asegurando que solo represente la ficha y su propietario, manteniendo la lógica de movimiento en Board.
- Se analizaron y explicaron los errores de importación y de métodos, corrigiendo nombres de clases y firmas de métodos para asegurar la correcta ejecución de los tests.
- Se implementaron y documentaron los tests unitarios para Board, Dice, Checkers y Player, siguiendo TDD.
- Se explicó y desarrolló la clase AIPlayer en ai.py, permitiendo que la IA lance los dados, genere movimientos válidos y seleccione la mejor secuencia.
- Se mejoró la IA agregando el método _copy_board para simular movimientos y la función _evaluate_sequence para tomar decisiones más inteligentes.
- Se mantuvo la trazabilidad de todos los cambios y mejoras en este archivo, facilitando el mantenimiento y la evolución del proyecto.

## [Unreleased]

### Agregado

- Implementación inicial del tablero de juego de Backgammon (clase `Board`) con seguimiento de puntos, bar y fuera del tablero.
- Jugador IA (`AIPlayer` class) con lógica básica de turno.
- Clases Player y Checkers para entidades del juego.
- Funcionalidad de lanzamiento de dados (`roll_dice`).
- Pruebas unitarias para módulos Board, AI, Player, Checkers y Dice.
- Integración de IA en el Board para juego automatizado.

### Cambiado

- Refactorización del método `move_piece` en `Board` para manejar movimientos desde el bar, bear-off, golpes y movimientos normales correctamente.
- Actualización de `is_valid_move` para priorizar movimientos desde el bar y validar destinos.
- Modificación de `play_turn` de IA para funcionar sin argumentos externos almacenando referencias de board y player.

### Corregido

- Problemas de importación circular entre `ai.py` y `board.py` usando referencias forward y TYPE_CHECKING.
- Fallos en tests `test_ai_play_turn`, `test_is_valid_move_bar_priority_white`, `test_move_piece_bear_off`, `test_move_piece_hit` y `test_move_piece_normal` corrigiendo lógica y configuraciones de tests.
- Llamadas de tests de IA para coincidir con la firma de método actualizada.
- Lógica de bear-off para incrementar correctamente el contador `off_board` sin agregar piezas a puntos inválidos.

### Removido

- Importaciones no utilizadas y código redundante en varios módulos.
