from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color

class Brique(Widget):
    pass

class Balle(Widget):
    vx = NumericProperty(5)
    vy = NumericProperty(-5)

    def move(self):
        self.x += self.vx
        self.y += self.vy

class Raquette(Widget):
    pass

class CasseBriquesGame(Widget):
    balle = ObjectProperty(None)
    raquette = ObjectProperty(None)
    score = NumericProperty(0)
    niveau = NumericProperty(1)
    briques = []

    # Modèles avec beaucoup plus de briques
    niveaux = [
        [[1] * 10 for _ in range(5)],  # Niveau 1 : grille pleine de briques
        [[(i + j) % 2 for j in range(10)] for i in range(5)],  # Niveau 2 : motif alterné
        [[1 if i == j or i + j == 9 else 0 for j in range(10)] for i in range(5)],  # Niveau 3 : diagonales
        [[1] * 10] * 7,  # Niveau 4 : grille dense
        [[(i * j) % 3 == 0 for j in range(10)] for i in range(6)],  # Niveau 5 : motif complexe
        [[1] * (10 - i) + [0] * i for i in range(10)],  # Niveau 6 : pyramide inversée
        [[0 if (i + j) % 3 == 0 else 1 for j in range(10)] for i in range(6)],  # Niveau 7 : losanges
        [[1 if j < i else 0 for j in range(10)] for i in range(10)],  # Niveau 8 : triangle
    ]

    def reset_game(self):
        self.balle.center = self.center
        self.raquette.center_x = self.center_x
        self.generate_briques(self.niveau)
        self.niveau += 1
        if self.niveau > len(self.niveaux):
            self.niveau = 1

    def generate_briques(self, niveau):
        # Nettoyage de l'ancien canvas et suppression des briques
        self.briques.clear()
        self.canvas.clear()

        # Dimensions ajustées pour plus de briques
        largeur_brique = self.width / 10
        hauteur_brique = 25

        # Dessiner les briques basées sur le modèle du niveau
        for i, ligne in enumerate(self.niveaux[niveau - 1]):
            for j, valeur in enumerate(ligne):
                if valeur == 1:
                    with self.canvas:
                        Color(0, 1, 0, 1)  # Vert pour les briques
                        x = j * largeur_brique
                        y = self.height - (i + 1) * hauteur_brique
                        rect = Rectangle(pos=(x, y), size=(largeur_brique, hauteur_brique))
                        self.briques.append(rect)

    def update(self, dt):
        self.balle.move()

        # Collision avec les murs
        if self.balle.x <= 0 or self.balle.right >= self.width:
            self.balle.vx *= -1
        if self.balle.y >= self.height:
            self.balle.vy *= -1

        # Si la balle tombe en bas, réinitialiser
        if self.balle.y <= 0:
            self.reset_game()

        # Collision avec la raquette
        if self.balle.collide_widget(self.raquette):
            self.balle.vy *= -1

        # Collision avec les briques
        for brique in self.briques[:]:
            if self.balle.x < brique.pos[0] + largeur_brique and \
               self.balle.x + self.balle.width > brique.pos[0] and \
               self.balle.y < brique.pos[1] + hauteur_brique and \
               self.balle.y + self.balle.height > brique.pos[1]:
                self.briques.remove(brique)
                self.canvas.remove(brique)
                self.balle.vy *= -1
                self.score += 10

    def on_touch_move(self, touch):
        self.raquette.center_x = touch.x

class CasseBriquesApp(App):
    def build(self):
        game = CasseBriquesGame()
        game.generate_briques(1)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    CasseBriquesApp().run()