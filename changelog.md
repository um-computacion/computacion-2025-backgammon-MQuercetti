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
