import pygame
import math

pygame.init()

width, height = 720, 720
janela = pygame.display.set_mode((width,height))
pygame.display.set_caption('Simulação Planetária')

branco = (255,255,255)
amarelo = (255,255,0)
azul = (0,0,205)
vermelho = (188,39,50)
cinza_escuro = (80,78,81)
fonte = pygame.font.SysFont('comicsans', 16)

class Planeta:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    ESCALA = 220/AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 dia

    def __init__(self, x,y, raio, cor, massa):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.massa = massa

        self.orbita = []
        self.sun = False
        self.distancia_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def desenhar(self, jane):
        x = self.x * self.ESCALA + width/2
        y = self.y * self.ESCALA + height/2

        if len(self.orbita) > 2:
            update_pontos = []
            for ponto in self.orbita:
                x,y = ponto
                x = x * self.ESCALA + width / 2
                y = y * self.ESCALA + height / 2
                update_pontos.append((x,y))

            pygame.draw.lines(jane, self.cor, False, update_pontos, 2)

        pygame.draw.circle(jane, self.cor, (x,y), self.raio)

        #if not self.sun:
         #   distancia_texto = fonte.render(f'{round(self.distancia_sun / 1000, 1)}km', 1, branco)
         #  jane.blit(distancia_texto, (x - distancia_texto.get_width() / 2, y - distancia_texto.get_height() / 2))


    def atracao(self, outro):
        outro_x , outro_y = outro.x, outro.y
        distancia_x = outro_x - self.x
        distancia_y = outro_y - self.y
        distancia = math.sqrt(distancia_x**2 + distancia_y**2)

        if outro.sun:
            self.distancia_sun = distancia

        forca = self.G * self.massa * outro.massa / distancia**2
        teta = math.atan2(distancia_y,distancia_x)
        forca_x = math.cos(teta)*forca
        forca_y = math.sin(teta) * forca
        return forca_x, forca_y

    def update_posicao(self, planetas):
        total_fx = total_fy = 0
        for planeta in planetas:
            if self == planeta:
                continue

            fx,fy = self.atracao(planeta)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.massa*self.TIMESTEP
        self.y_vel += total_fy / self.massa * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbita.append((self.x,self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sol = Planeta(0,0,30,amarelo,1.98892*10**30)
    sol.sun = True

    terra = Planeta(-1* Planeta.AU,0,16,azul,5.9742*10**24)
    terra.y_vel = 29.783*1000

    marte = Planeta(-1.524* Planeta.AU, 0, 12, vermelho, 6.39*10**23)
    marte.y_vel = 24.077*1000

    mercurio = Planeta(0.387*Planeta.AU,0,8, cinza_escuro, 3.3*10**23)
    mercurio.y_vel = -47.4*1000

    venus = Planeta(0.723* Planeta.AU,0,14,branco, 4.8685*10**24)
    venus.y_vel = -35.02*1000

    estrelas = [sol, terra, marte, mercurio, venus]

    while run:
        clock.tick(60)
        janela.fill((0,0,0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                run = False

        for star in estrelas:
            star.update_posicao(estrelas)
            star.desenhar(janela)

        pygame.display.update()

    pygame.quit()

# simulando a orbita de alguns planetas do sistema solar
main()