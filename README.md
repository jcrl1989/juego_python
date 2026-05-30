# DIGIMON BATTLE

Proyecto final desarrollado en Python utilizando Pygame.

## Descripción

Digimon Battle es un videojuego RPG inspirado en las mecánicas clásicas de Pokémon y Digimon World.

El jugador selecciona un Digimon inicial, explora el Mundo Digital, combate contra Digimon salvajes, gana experiencia, obtiene monedas y compra objetos en una tienda para fortalecer a su compañero.

---

## Tecnologías utilizadas

* Python 3.12
* Pygame 2.6
* Git
* GitHub
* Ubuntu / WSL

---

## Características implementadas

### Sistema de Menús

* Menú principal
* Selección de Digimon inicial
* Navegación mediante teclado

### Digimon Iniciales

Actualmente disponibles:

* Agumon
* Gabumon
* Tentomon

Cada Digimon posee:

* HP
* Ataque
* Defensa
* Velocidad
* Nivel
* Experiencia

---

### Mundo Digital

El jugador puede desplazarse por un mapa compuesto por:

* Césped
* Caminos
* Árboles
* Rocas

Los árboles y rocas funcionan como obstáculos.

---

### Encuentros Aleatorios

Al caminar sobre césped existe una probabilidad de encontrar Digimon salvajes.

Las zonas del mundo determinan la dificultad de los enemigos.

Zonas disponibles:

1. Bosque Inicial
2. Cueva Digital
3. Montaña Binaria

---

### Sistema de Combate

Combate por turnos.

Acciones:

* Atacar
* Usar pociones

El daño depende de:

* Ataque
* Defensa

Cuando un Digimon pierde todo su HP es derrotado.

---

### Experiencia y Niveles

Al ganar una batalla:

* Se obtiene experiencia
* Se obtienen monedas

Al acumular suficiente experiencia:

* El Digimon sube de nivel
* Mejoran sus estadísticas

---

### Evoluciones

El sistema de evolución se encuentra implementado.

Ejemplo:

Agumon

* Nivel 8 → Greymon
* Nivel 16 → MetalGreymon

---

### Tienda

El jugador puede acceder a una tienda desde el mapa.

Objetos disponibles:

* Poción pequeña
* Poción mediana
* Poción grande

Las pociones restauran HP.

---

### Inventario

Cada jugador posee un inventario propio.

Ejemplo:

inventory = {
"small": 0,
"medium": 0,
"large": 0
}

---

### Sprites

El sistema carga sprites desde la carpeta:

assets/sprites/

Si un sprite no existe se muestra un marcador temporal.

---

## Estructura del Proyecto

juego_python/

├── assets/

│ └── sprites/

├── data/

│ └── digimon_data.py

├── scenes/

│ ├── battle_scene.py

│ ├── menu.py

│ ├── selection.py

│ └── shop_scene.py

├── systems/

│ ├── battle.py

│ ├── evolution.py

│ ├── leveling.py

│ ├── shop.py

│ └── world.py

├── utils/

│ ├── helpers.py

│ └── loader.py

├── config.py

├── main.py

├── requirements.txt

└── README.md

---

## Controles

### Menú

ENTER → Iniciar

ESC → Salir

---

### Selección

← → Cambiar Digimon

ENTER → Confirmar

---

### Mundo

W → Arriba

S → Abajo

A → Izquierda

D → Derecha

T → Abrir tienda

ESC → Volver al menú

---

### Tienda

↑ ↓ → Navegar

ENTER → Comprar

ESC → Salir

---

### Combate

ENTER → Atacar

P → Poción pequeña

O → Poción mediana

I → Poción grande

ESC → Salir

---

## Cómo ejecutar el proyecto

Activar entorno virtual:

source .venv/bin/activate

Instalar dependencias:

pip install -r requirements.txt

Ejecutar:

python main.py

---

