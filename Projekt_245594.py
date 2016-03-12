# Projekt zaliczeniowy na modsym 2014/2015
# Autor: Adam S. Grzonkowski, 245594, UMK w Toruniu

##Zadanie:
##Może Pan to zrobić w 2D. Na ekranie jest cel, który może poruszać się w dowolny sposób np. być sterowany przez użytkownika, oraz wyrzutnia rakiet,
##które starają się trafić w cel. Mogą po prostu zmieniać kierunek tak, żeby mieć zawsze cel przed nosem lub stosować jakąś bardziej wyrafinowaną strategię
##np. celować w miejsce, w którym cel z bieżącą prędkością powinien być w momencie przecięcia trajektorii.
##Pozdrawiam
##JM

# Importujemy potrzebne moduly
import sys, pygame, math
from pygame.locals import *
from pygame.sprite import groupcollide  #potrzebne do wykrycia kolizji miedzy poszczegolnymi kulami

# Tworzymy stale - kolory
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
BROWN    = (139,  69,  19)
GREEN    = (34,  139,  34)
DARKGRAY = (128, 128, 128)
RED      = (255,   0,   0)
YELLOW   = (255, 255,   0)

BGCOLOR = GREEN #kolor tla ustawiamy na zielony

# Definiujemy okno gry, w pikselach (szerokosc i wysokosc)
WINDOWWIDTH = 640
WINDOWHEIGHT = 480 

# Ustawiamy wartosc FPS 
FPS = 30

# Przygotowujemy gre w pygame
pygame.init()
FPSCLOCK = pygame.time.Clock() #Okreslamy, jak czesto ekran sie odswieza
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #definiujemy rozmiar planszy
pygame.display.set_caption('Projekt_245594') #tytul wyswietlany na pasku tytulu okna


# Klasa tworzaca kule
class Bullet1(pygame.sprite.Sprite):
 
    def __init__(self, mouse):
        super(Bullet1, self).__init__()  #konstruktor rodzic
        self.image = pygame.image.load("cannonball.png") #graficzna reprezentacja kuli
        self.rect = self.image.get_rect(x=cannon1x, y=cannon1y) #poczatkowa pozycja w miejscu armaty
        self.shoot_sound = pygame.mixer.Sound('shooting.wav') #dzwiek wystrzalu
        self.shoot_sound.set_volume(.1)  #sciszamy dzwiek do 0.3 wartosci, bo jest za glosny.
        self.shoot_sound.play() #"wygraj" dzwiek wystrzalu
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]  #przechowaj info o pozycji myszy
        
    def update(self):
        #predkosc lotu kuli. Przyspiesza w trakcie gry
        if playtime < (1/5) * czas_gry:
            speed = 8.
        elif playtime < (2/5) * czas_gry:
            speed = 11.
        elif playtime < (3/5) * czas_gry:
            speed = 14.
        elif playtime < (4/5) * czas_gry:
            speed = 17.
        else:
            speed = 20.
        distance = [self.mouse_x-cannon1x, self.mouse_y-cannon1y] #obliczamy dystans armaty od gracza
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)   #normalizujemy przeciwprostokatna (dlugosc wektora)
        direction = [distance[0] / norm, distance[1 ] / norm]   #obliczamy kierunek wektora
        bullet_vector = [direction[0] * speed, direction[1] * speed] #otrzymujemy wektor kuli
        
        self.rect.x += bullet_vector[0]   #aktualizuj pozycje x
        self.rect.y += bullet_vector[1]   #aktualizuj pozycje y

class Bullet2(pygame.sprite.Sprite):

    def __init__(self, mouse):
        super(Bullet2, self).__init__()  #konstruktor rodzic
        self.image = pygame.image.load("cannonball.png") #graficzna reprezentacja kuli
        self.rect = self.image.get_rect(x=cannon2x, y=cannon2y) #poczatkowa pozycja w miejscu armaty
        self.shoot_sound = pygame.mixer.Sound('shooting.wav') #dzwiek wystrzalu
        self.shoot_sound.set_volume(.1)  #sciszamy dzwiek do 0.3 wartosci, bo jest za glosny.
        self.shoot_sound.play() #"wygraj" dzwiek wystrzalu
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]  #przechowaj info o pozycji myszy
        
    def update(self):
        #predkosc lotu kuli. Przyspiesza w trakcie gry
        if playtime < (1/5) * czas_gry:
            speed = 8.
        elif playtime < (2/5) * czas_gry:
            speed = 11.
        elif playtime < (3/5) * czas_gry:
            speed = 14.
        elif playtime < (4/5) * czas_gry:
            speed = 17.
        else:
            speed = 20.
        distance = [self.mouse_x-cannon2x, self.mouse_y-cannon2y] #obliczamy dystans armaty od gracza
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)   #normalizujemy przeciwprostokatna (dlugosc wektora)
        direction = [distance[0] / norm, distance[1 ] / norm]   #obliczamy kierunek wektora
        bullet_vector = [direction[0] * speed, direction[1] * speed] #otrzymujemy wektor kuli
        
        self.rect.x += bullet_vector[0]   #aktualizuj pozycje x
        self.rect.y += bullet_vector[1]   #aktualizuj pozycje y 
        
# Klasa tworzaca gracza - alegorycznie do kuli
class Target(pygame.sprite.Sprite):
    def __init__(self, mouse):
        super(Target, self).__init__()
        self.image = pygame.image.load("Trollface.png")
        self.mouse_x, self.mouse_y = mouse[0], mouse[1]
        self.rect = self.image.get_rect(x= self.mouse_x, y = self.mouse_y)
        self.effect = pygame.mixer.Sound('ouch.wav')
        
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.rect.topleft = self.pos
        

# Zwraca liczbe stopni, o ile armata (x1, y1) musi sie obrocic, zeby miec gracza-myszke (x2, y2) na przeciwsko siebie
def getAngle(x1, y1, x2, y2):
    # Wartosci zwracane: 0 - prawo, 90 - gora, 180 - lewo, 270 - dol. Wszystkie wartosci pomiedzy 0, a 360 stopni.
    dy = y1 - y2                # zmiana w y
    dx = x1 - x2                # zmiana w x
    angle = math.atan2(dx, dy)  # obliczanie kata w radianach. 
    angle = math.degrees(angle) # konwersja radianow na stopnie
    angle = (angle + 90) % 360  # dostosuj kat, zeby byl na wprost gracza
    return angle


# Tworzenie grup spriteow
all_sprites_list = pygame.sprite.Group()
bullet1_list = pygame.sprite.Group() #grupa kul wystrzelonych z armaty 1
bullet2_list = pygame.sprite.Group() #grupa kul wystrzelonych z armaty 2
bullets_list = pygame.sprite.Group() #grupa wszystkich kul, do wykrywania kolizji z graczem

# Zmienne globalne
playtime = 0   #czas gry
hits = 0       #ilosc trafien (ilosc kolizji miedzy graczem, a kulami)
bullet_hits = 0#ilosc kolizji miedzy kula, a kula
koniec = 0     #zmienna pomocnicza okreslajca koniec gry
ilosc_zyc = 5  #ilosc zyc gracza - maksymalna ilosc mozliwych kolizji miedzy graczem, a kula
czas_gry = 16  #maksymalny czas gry

# Tworzymy obrazek armaty
cannonSurf = pygame.Surface((100, 100))  #rysujemy w przestrzeni 100x100 pikseli
cannonSurf.fill(GREEN)                 #przestrzen wypelniamy kolorem tla
pygame.draw.circle(cannonSurf, DARKGRAY, (20, 50), 20) # rysujemy lewy koniec
pygame.draw.circle(cannonSurf, DARKGRAY, (80, 50), 20) # rysujemy prawy koniec
pygame.draw.rect(cannonSurf, DARKGRAY, (20, 30, 60, 40)) # rysujemy wlasciwa lufe
pygame.draw.circle(cannonSurf, BLACK, (80, 50), 15) # otwor lufy
pygame.draw.circle(cannonSurf, BLACK, (80, 50), 20, 1) # obwodka lufy
pygame.draw.circle(cannonSurf, BROWN, (30, 70), 20) # podstawa (kolo)
pygame.draw.circle(cannonSurf, BLACK, (30, 70), 20, 1) # obwodka podstawy

# Interwal pomiedzy poszczegolnymi strzalami
RELOAD_SPEED = 600 #czas opoznienia (w milisekundach, 300 = 0,3 sek)). Zmniejsza sie w trakcie gry - patrz obsluge eventow.
reloaded_event = pygame.USEREVENT + 1 #przydzielamy numer eventu, 32+1 = 33
reloaded = True     #poczatkowa wartosc na True, czyli gotowy do strzalu

# Zdarzenie samoczynnego strzalu
SHOOT = 100 # czas opoznienia pomiedzy poszczegolnymi strzalami w ms. 
shoot_event = pygame.USEREVENT + 2 
pygame.time.set_timer(shoot_event, SHOOT)

# Muzyka w tle
pygame.mixer.music.load('Intense_Epic_Music_-_Battlefield.ogg')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(2,0.0)

# Współrzędne armat - w tym miejscu pojawia sie strzelajace armaty
cannon1x, cannon1y =  50, 100
cannon2x, cannon2y =  500, 50


##########################
# GLOWNA PETLA APLIKACJI #
##########################
while True:
 
    # Wypelnij ekran kolorem tla
    DISPLAYSURF.fill(BGCOLOR)
    # 30 klatek na sekunde (30 wykonan petli na sekunde)
    milliseconds = FPSCLOCK.tick(FPS)
    # Sekundy od ostatniej ramki
    seconds = milliseconds / 1000
    playtime += seconds
    
    # Petla definiujaca zdarzenia (wcisniecie klawisza lub przycisku myszy)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        # Strzelanie LPM - odkomentuj ten fragment i zakomentuj automatyczne strzelanie, aby strzelac mysza!
##        elif event.type == pygame.MOUSEBUTTONDOWN:
##            if koniec == 0 and reloaded == True:
##                reloaded = False  # Po oddaniu strzalu, trzeba przeladowac
##                pygame.time.set_timer(reloaded_event, RELOAD_SPEED) # Ustaw licznik na wartosc zachowana pod zmienna RELOAD_SPEED
##                bullet = Bullet1(pygame.mouse.get_pos())   #inicjujemy obiekt klasy Bullet
##                all_sprites_list.add(bullet)              #dodajemy obiekt do ogolnej listy spriteow
##                bullet_list.add(bullet)
##                bullet2 = Bullet2(pygame.mouse.get_pos())
##                all_sprites_list.add(bullet2)              
##                bullet_list.add(bullet2)
        elif event.type == shoot_event:
            if koniec == 0 and reloaded == True:
                reloaded = False  # Po oddaniu strzalu, trzeba przeladowac
                if playtime > (1/2) * czas_gry:   # Po uplywie polowy czasu gry, ustaw predkosc przeladowania na 1/3 wartosci poczatkowej
                    pygame.time.set_timer(reloaded_event, int((1/3) * RELOAD_SPEED)) 
                elif playtime > (1/4) * czas_gry: # Po uplywie 1/4 czasu gry, ustaw predkosc przeladowania na 2/3 wartosci poczatkowej
                    pygame.time.set_timer(reloaded_event, int((2/3) * RELOAD_SPEED))
                else:
                    pygame.time.set_timer(reloaded_event, RELOAD_SPEED) # Przez pierwsze 1/4 czesc gry, ustaw predkosc przeladowania na wartosc poczatkowa RELOAD_SPEED

                #Kula z armaty 1 (cannon1x, cannon1y)
                bullet = Bullet1(pygame.mouse.get_pos())   #inicjujemy obiekt klasy Bullet1
                all_sprites_list.add(bullet)              #dodajemy obiekt do ogolnej listy spriteow
                bullet1_list.add(bullet)
                bullets_list.add(bullet)

                #Kula z armaty 2 (cannon2x, cannon2y)
                bullet2 = Bullet2(pygame.mouse.get_pos())
                all_sprites_list.add(bullet2)              
                bullet2_list.add(bullet2)
                bullets_list.add(bullet2)
                 
        # Przeladowanie gotowe - mozliwosc oddania strzalu
        elif event.type == reloaded_event:  # Kiedy licznik reload dobiegnie konca, zresetuj go - armata moze wtedy strzelac
            reloaded = True
            pygame.time.set_timer(reloaded_event, 0) #wartosc 0 - armata moze strzelac

    # Pobieramy informacje o aktualnym polozeniu myszki   
    mousex, mousey = pygame.mouse.get_pos()
    
    # Jezeli gra trwa, to:
    if koniec == 0:
        for cannonx, cannony in ((cannon1x, cannon1y), (cannon2x,cannon2y)):
            degrees = getAngle(cannonx, cannony, mousex, mousey)# Obliczamy kat obrotu armaty wzgledem gracza
    # Narysuj armate - obroc kopie obrazka armaty i wyrysuj ja na ekranie
            rotatedSurf = pygame.transform.rotate(cannonSurf, degrees) #obracamy przestrzen cannonSurf o liczbe stopni obliczona za pomoca getAngle. Uwaga! Wylaczajac obrot o 90 stopni, przestrzen bedzie powiekszana, zeby zmiescic caly obraz.
            rotatedRect = rotatedSurf.get_rect()                       #pobieramy info o wspolrzednych obroconej armaty
            rotatedRect.center = (cannonx, cannony)                    #punkt centralny armaty ustawiamy na zdefiniowany pod zmiennymi cannonx i cannony
            DISPLAYSURF.blit(rotatedSurf, rotatedRect)                     #wyswietlamy obrocona armate
        
    # Tworzenie gracza, dodanie go do listy spriteow
        player = Target(pygame.mouse.get_pos())
        all_sprites_list.add(player)
        
    # Sprawdzanie kolizji gracz <-> kula
        hit_list = pygame.sprite.spritecollide(player, bullets_list, True) #w hit_list przechowaj sprity kolizyjne. Wartosc True oznacza, ze znikna z ekranu po kolizji.
        for bullet in hit_list:    #dla wszystkich kul armatnich, ktore trafily w gracza
            hits += 1              #zwieksz wartosc zmiennej hits o 1
            openChannel_A = pygame.mixer.find_channel() #znajdz wolny kanal
            if openChannel_A:                           #jezeli kanal jest wolny
                openChannel_A.play(player.effect)   #odegraj dzwiek odgrywany po zderzeniu

    # Sprawdzanie kolizji kula <-> kula
    if groupcollide(bullet1_list, bullet2_list, True, True):
        boom = pygame.mixer.Sound('bomb.wav')
        boom.set_volume(.5)
        openChannel_B = pygame.mixer.find_channel()
        if openChannel_B:
            openChannel_B.play(boom)

    # Rysujemy ramke planszy o grubosci 1
    pygame.draw.rect(DISPLAYSURF, BLACK, (0, 0, WINDOWWIDTH, WINDOWHEIGHT), 1)

    # Rysujemy wszystkie obiekty Sprite - kule armatnie i gracza
    if koniec == 0:
        all_sprites_list.draw(DISPLAYSURF)

    # Wyswietlamy instrukcje dla gracza w dolnej czesci ekranu
    if koniec == 0:
        myfont2 = pygame.font.Font(None, 18)
        instrukcja = myfont2.render("Unikaj kul armatnich przez " + str(czas_gry) + " sekund i zbierz jak najwiecej punktow!", 1, (WHITE))
        DISPLAYSURF.blit(instrukcja, (120, 460))
    else:
        myfont2 = pygame.font.Font(None, 20)
        instrukcja = myfont2.render("Nacisnij klawisz ESC, aby opuscic gre.", 1, (WHITE))
        DISPLAYSURF.blit(instrukcja, (190, 400))
        
    # Wyswietlenie ilosci punktow (nietrafionych strzalow) - elementy bullet_list
    myfont = pygame.font.Font(None, 26)
    tekst = myfont.render("Punkty:  " + str(len(bullets_list)), 1, (WHITE))
    DISPLAYSURF.blit(tekst, (0, 0))

    # Wyswietlenie pozostalego czasu gry - odliczanie w dol
    if koniec == 0:
        czas = myfont.render("Pozostalo:  %.1f"  % abs((czas_gry - playtime)) + "s", 1, (WHITE))
    DISPLAYSURF.blit(czas, (270, 0))

    # Wyswietlenie ilosci zyc (wartosc 5 pomniejszona o ilosc kolizji)
    if hits < (1/3) * ilosc_zyc:
        wynik = myfont.render("Zycia: " + str(ilosc_zyc-hits) + "/" + str(ilosc_zyc) , 1, (WHITE))  #dla trafien w ilosci mniej niz 1/3 ilosci zyc gracza wyswietl na bialo
    elif hits < (2/3) * ilosc_zyc:
        wynik = myfont.render("Zycia: " + str(ilosc_zyc-hits) + "/" + str(ilosc_zyc) , 1, (YELLOW)) #dla trafien w ilosci mniej niz 2/3 ilosci zyc gracza wyswietl na zolto
    else:
        wynik = myfont.render("Zycia: " + str(ilosc_zyc-hits) + "/" + str(ilosc_zyc) , 1, (RED))    #w pozostalych przypadkach wyswietl na czerwono
    DISPLAYSURF.blit(wynik, (560, 0))

    # Koniec gry - przegrana
    if hits >= ilosc_zyc:
        koniec = 1   #zmienna pomocnicza ustawiona na 1 - namierzanie armaty, strzelanie i sprite gracza wylaczone
        czcionka = pygame.font.Font(None, 60)
        game_over = czcionka.render("Przegrana...", 1, (WHITE))
        DISPLAYSURF.blit(game_over, (320, 240))
       
    # Koniec gry - wygrana
    elif playtime > czas_gry and hits < ilosc_zyc:
        koniec = 1    #zmienna pomocnicza ustawiona na 1 - namierzanie armaty, strzelanie i sprite gracza wylaczone
        czcionka = pygame.font.Font(None, 60)
        game_over = czcionka.render("Wygrales!", 1, (WHITE))
        DISPLAYSURF.blit(game_over, (320, 240))
        
    # Zaktualizuj wyswietlana gre
    all_sprites_list.update()  #zaktualizuj parametry spritow

    # Wyrysuj wszystko
    pygame.display.flip()

# Wyswietlenie czasu gry w chwili jej zakonczenia - poza petla, wartosc niezmienna
czas = myfont.render("Czas gry:  %.1f" % playtime + "s", 1, (WHITE))
