▎Match-3

▎Descripción

Este proyecto es una implementación del clásico juego Match-3, donde los jugadores pueden intercambiar fichas para formar combinaciones de tres o más fichas del mismo color. Esta versión incluye nuevas mecánicas de arrastre para mover las fichas, la generación de potenciadores y la reordenación del tablero cuando no hay combinaciones.

▎Objetivos

• Cambiar la forma de mover las fichas mediante arrastre en lugar de clics.

• Permitir el movimiento de fichas solo donde haya una combinación.

• Reorganizar el tablero mientras no haya combinaciones.

• Crear dos tipos de potenciadores con características especiales.

▎Características

1. Movimiento de Fichas por Arrastre: 

   • Las fichas se pueden arrastrar y soltar. Mientras se mantiene presionado el botón del ratón, la ficha seguirá al puntero del ratón. Al soltar, la ficha se moverá si se forma una combinación.

2. Combinaciones:

   • Solo se permite el movimiento de fichas donde se puede formar una combinación de tres o más fichas del mismo color.

3. Reorganización del Tablero:

   • Después de cada movimiento, se verifica si hay combinaciones. Si no hay, el tablero se reorganiza automáticamente hasta que se formen combinaciones.

4. Potenciadores:

   • Potenciador de 4 Fichas: Se genera un potenciador al formar una combinación de cuatro fichas. Este potenciador puede ser movido y activado. Al activarse, explota y destruye las fichas vecinas en vertical y horizontal.

   • Potenciador de 5 o Más Fichas: Se genera un potenciador al formar una combinación de cinco o más fichas. Este potenciador también puede ser movido y activado. Al activarse, explota y destruye todas las fichas del mismo color en el tablero.

▎Instalación

1. Clona este repositorio:
   
   git clone https://github.com/tu_usuario/match3.git
   cd match3
   

2. Crea un entorno virtual:
   
   python3 -m venv .venv
   

3. Activa el entorno virtual:
   
   source .venv/bin/activate  # En Linux/Mac
   .venvScriptsactivate     # En Windows
   

4. Instala las dependencias:
   
   pip install -r requirements.txt
   

5. Ejecuta el juego:
   
   python main.py
   

▎Cómo Jugar

• Arrastra las fichas para intercambiarlas y formar combinaciones.

• Observa cómo se generan potenciadores al formar combinaciones específicas.

• Activa los potenciadores haciendo clic sobre ellos para causar explosiones en el tablero.

▎Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar el juego, por favor abre un "issue" o envía un "pull request".

▎Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.
