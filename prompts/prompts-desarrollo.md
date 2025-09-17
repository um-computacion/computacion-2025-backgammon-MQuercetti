# Prompt

¿Podrías ayudarme a realizar este código? Con las pautas que te di (SOLID y TDD).

## Respuesta

Se propuso una implementación de la clase Board para el juego de Backgammon, siguiendo los principios SOLID y el método TDD. La clase Board gestiona el estado del tablero, inicializa los puntos según la disposición estándar de Backgammon y permite mover fichas entre puntos. La implementación está preparada para ser testeada y extendida.

## Prompt

El tema es que se tiene que mover acorde a los dados porque depende de qué número toque en el tablero y si está ocupado no puede estar en ese lugar y que si el dado tiene ambos números iguales se duplican ambos dados.

## Respuesta

La lógica de movimiento en Backgammon depende del resultado de los dados y del estado de los puntos en el tablero. El jugador puede mover una ficha tantos puntos como indique cada dado, pero solo si el destino no está ocupado por más de una ficha del oponente. Si ambos dados muestran el mismo número (dobles), el jugador tiene cuatro movimientos en vez de dos.

Para cumplir con SOLID, la lógica de movimiento debe estar en el tablero, no en la ficha. La ficha solo conoce a su dueño. El tablero verifica si el movimiento es válido y ejecuta el movimiento.

A continuación se muestra una propuesta para la clase `Checkers` y la lógica de movimiento en el tablero:
