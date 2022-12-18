import pygame
import random
from copy import deepcopy
from time import time

#ma być metaheurystycznie - fukcja ocena, fukncji kary, metoda ulosowiona zachłanna
#sposób I: stawianie I hetmana w I wierszu, potem wybieranie rozwiązania (?)
#sposób II: stawianie I hetmana randomowo 
#sposób III:

#może być tablica, ktora ma kol i wiersze zajęte już 
#figura cyrkiel, ktora bije okrąg. Trzeba też je rozstawić

#-------------------------------------------------------------------------------------------------------------------
#zmienne globalne-------------------------------
global chessboard_points
chessboard_points=[]
global ms
ms=0
global solution
solution=[]

#do wizualizacji
width = 800
height = 600
global text
surface = pygame.display.set_mode((width,height))
surface.fill((94,155,233))
pygame.init()
pygame.display.flip()
color = (0,0,0)
color2= (255,255,255)
color3=(24,23,133)


#----------------------------------------------------------------------------------------------------------------
#generowanie tablic-----------------------------------------------------------------------------------------------


def points_generator(chessboard):
    
    points_chessboard=deepcopy(chessboard)
    n=len(points_chessboard)
    g=[]
    for i in range(0, n):
        for j in range(0,len(points_chessboard[i])):
            x=random.randint(10,200)
            while(x in g): x=random.randint(10,200)
            points_chessboard[i][j]=x
            g.append(x)
    return points_chessboard


#przypisanie kolorów tablicy

def colored_chessboard_gen(chessboard,colors):
    
    n=len(chessboard)
    colored_chessboard=[]
    for i in range(0,n):
        colored_chessboard.append([])
        for j in range(0,len(chessboard[i])):
            colored_chessboard[i].append(colors[(i+j)%2])
            if chessboard[i][j]==-1: colored_chessboard[i][j]=colors[2]
    return colored_chessboard



def chessboard_generator(n,k):  

    chessboard = []
    for i in range(0,n):
        chessboard.append([])
        for j in range(0,k):
            chessboard[i].append(0)

    return chessboard
           
#----------------------------------------------------------------------------------------------------------------            
#Funkcje pomocnicze.
#----------------------------------------------------------------------------------------------------------------

#czy można postawić hetmana na danym polu
def check(row, column, board):    

    for j in range(0,len(board)):
        if j==column: continue
        if board[row][j] == 1: return False
    
    for i in range(0,len(board)):
        if i==row: continue
        if(len(board[i])>column):
            if board[i][column] == 1: return False
    
    x=column
    for k in range(row,len(board)):
        
        if x<len(board[k]):
            if board[k][x] == 1: return False
        x=x+1
    
    x=column
    for k in range(row, -1, -1):
        if x<len(board[k]):
            if board[k][x] == 1: return False
        x=x-1
        if x<0: break
    

    x=column
    for k in range(row, -1, -1):
        if x<len(board[k]):
            if board[k][x] == 1: return False
        x=x+1
        if x<0: break
           

    x=column
    for k in range(row,len(board)):
        if x<len(board[k]):
            if board[k][x] == 1: return False
        x=x-1
        if x<0: break
    
    return True

#-----------------------------------------------------
#funkcja zwracająca listę indeksów listy, ale w takiej kolejności, że elementy listy pierwotnej są posortowane
def sort_row(row):
    
    row_2=deepcopy(row)
    row_2.sort()
    id=[]
    for element in row_2:
        id.append(row.index(element))
    id.reverse()
    return id
    
#-----------------------------------------------------
#funkcja transponująca szachownicę, gdy liczba wierszy jest większa od liczby kolumn. 
#Wykorzystywana dla ułatwienia.
def transpose(chessboard, r, c):
    b = []
    for i in range(c):
        n=[]
        for j in range(r):
            n.append(chessboard[j][i])
        b.append(n)
    return b

#----------------------------------------------------
def sumit(x):
    s=0
    global chessboard_points
    for i in range(len(x)):
        id=x[i].index(1)
        s=s+chessboard_points[i][id]
    return s
#-----------------------------------------------------
#funkcja wypisująca tekst

def texts(t, cx, cy, s,color):
    font = pygame.font.Font('freesansbold.ttf', s)
    text= font.render(t, True,color)
    textRect = text.get_rect()
    textRect = text.get_rect()
    textRect.center = (cx,cy) 
    surface.blit(text, textRect)
    pygame.display.flip()
#-----------------------------------------------------
#funkcja rysujca
def drawing(chessboard):
    global chessboard_points
    recx=40
    recy=40
    colors=["white","black"]
    chessboard_width=len(chessboard)*recx
    chessboard_height=len(chessboard[0])*recy
    x=width//2-chessboard_width
    y=height//2-chessboard_height//2
    color="white"
    
    for i in range(0,len(chessboard)):
        for j in range(0,len(chessboard[i])):
            pygame.draw.rect(surface, colors[(i+j)%2], pygame.Rect(x, y, recx, recy))
            texts(str(chessboard_points[i][j]),x+12,y+12, 12,color3)
            if chessboard[i][j]==1:
                pygame.draw.circle(surface,(255,0,0),(x+recx//2,y+recy//2),4) 
            x=x+recx
        y=y+recy
        x=width//2-chessboard_width
          
    pygame.display.flip()


#------------------------------------------------------------------------------------------------------------
#rozwiązania problemu
#------------------------------------------------------------------------------------------------------------
#I sposób - przegląd rozwiązań, algorytm bruteforce, znajdywanie rozwiązywania optymalnego
    

def bruteforce(chessboard, row,skip, s): 
    global solution, chessboard_points, ms
    
    if row>=len(chessboard):
        if ms<s:
            ms=s
            solution=deepcopy(chessboard)
        return chessboard 

    if row==skip: 
        bruteforce(chessboard, row+1,skip,s)
        return chessboard
    
    for j in range(0, len(chessboard[row])):
        
        if check(row, j, chessboard):
            chessboard[row][j]=1
        
            s=s+chessboard_points[row][j]
            bruteforce(chessboard, row+1, skip, s)
            s=s-chessboard_points[row][j]
            chessboard[row][j]=0
            
    return chessboard


def brute_solve(chessboard):
    global chessboard_points,solution,ms
    solution=[]
    ms=0
    start = time()
    for i in range(len(chessboard)): #wybór początkowego pola, postawienie pierwszego hetmana
        for j in range(len(chessboard[i])):
            chessboard[i][j]=1
            s=chessboard_points[i][j]
            bruteforce(chessboard,0,i,s)
            chessboard[i][j]=0
    end=time()
    duration=round(end-start,3)
    result=[deepcopy(solution), ms, duration]
    return result
    

#-------------------------------------------------------------------------------------------------------------------------------------------------
#II sposób - wyszukiwanie dostępnego pola o najwyższym punktowaniu w danym wierszu. 
# szukanie pola o maksymalnej wartości rozwiązanie pół na pół, bo można 
# wybrać maksymalną, ale suma innych w pozostałych wierszach, którą blokuje wybrana kolumna -metaheurystyka

    
def max_in_row(chessboard, row, skip, s):
    global solution, chessboard_points,ms

    if row>=len(chessboard): 
        if ms<s:
            ms=s
            solution=deepcopy(chessboard)
        return chessboard 
    
    if row==skip: 
        max_in_row(chessboard,row+1,skip,s)
        return chessboard

    id=sort_row(chessboard_points[row])
    for j in range(0, len(chessboard[row])):
        
        if check(row, id[j], chessboard):
            chessboard[row][id[j]]=1
            s=s+chessboard_points[row][id[j]]
            x=max_in_row(chessboard, row+1, skip, s)
            if x!=False: return chessboard
            chessboard[row][id[j]]=0
            s=s-chessboard_points[row][id[j]]

    return False    


def max_solve(chessboard): 
    global solution,ms,chessboard_points
    solution=[]
    ms=0
    start = time()
    for i in range(0,len(chessboard)):
        id=sort_row(chessboard[i])
        chessboard[i][id[0]]=1
        s=chessboard_points[i][id[0]] #początkowa liczba punktów, za rostawienie pierwszego hetmana
        max_in_row(chessboard, 0,i,s)
        chessboard[i][id[0]]=0
    end= time()
    duration=round(end-start,3)
    result=[deepcopy(solution), ms, duration]    
    return result


#---------------------------------------------------------------------------------------------------------------------------
#III. Sposób - max_on_board

def find_max(chessboard, sorted, visited, rows): # sorted tablica posortowanych indeksow
    global chessboard_points
    
    max_i=-1
    max_j=-1
    m=0
    for i in range(0,len(chessboard)):
        if i in rows: continue
        j=0
        while j<len(sorted[i]):
            
            c=sorted[i][j]
            if [i,c] in visited: #juz sprawdzano jako max jesli jest w visited
                j=j+1
                continue
            if m<chessboard_points[i][c]:
                max_i=i
                max_j=c
                m=chessboard_points[i][c]
                break
            j=j+1
    visited.append([max_i,max_j])
    return [max_i, max_j]



def max_search(chessboard,sorted,visited,rows,h):
    global chessboard_points, solution
    old_len=len(visited)
    n=len(chessboard)
    k=len(chessboard[0])
    if h==len(chessboard)-1: 
        solution=chessboard
        return chessboard
    
    while len(visited)<n*k: #jesli do visited dodano wszystkie pola, wtedy nie ma co sprawdzac, n*k to ilosc pol 
        l=find_max(chessboard, sorted,visited,rows)
        i=l[0]
        j=l[1]
        if check(i,j,chessboard):
            chessboard[i][j]=1
            h=h+1
            rows.append(i)
            x=max_search(chessboard,sorted,visited,rows,h)
            if x: return chessboard
            h=h-1
            del rows[-1] #jesli sie nie powiodlo, usuwamy wiersz, bo nie ma juz w nim hetmana
            chessboard[i][j]=0
            id=visited.index([i,j]) #jesli nie udalo sie wypelnic szachownicy to usuwamy 
            visited=visited[0:id+1]
            
    visited=visited[0:old_len] #jesli nic nie zostalo wstawione to usuwamy wszystkie odwiedzone pola
    return False
    


def max_on_board(chessboard):
    global chessboard_points, ms, solution
    solution=[]
    ms=0
    sorted=[]
    for i in range(0,len(chessboard)):
        sorted.append(sort_row(chessboard_points[i]))
    
    start=time()
    max_search(chessboard, sorted,[],[],0)
    end=time()
    ms=sumit(solution)
    duration=round(end-start,3)
    result=[deepcopy(solution), ms, duration]
    return result
    

#---------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

def main():
    results=[]
    global chessboard_points, ms, solution
    n=11
    k=9
    
    while(n<=4 or k<=4):
        print("Wrong data (n>4, k>4):")
    
    
    transp=False
    if n>k:
        transp=True
        pom=n
        n=k
        k=pom
        

    chessboard=chessboard_generator(n,k)
    chessboard_points=points_generator(chessboard)

      


    results.append(brute_solve(chessboard))
    results.append(max_solve(chessboard))
    results.append(max_on_board(chessboard))

    if transp:
        results[0][0]=transpose(results[0][0],n,k)
        results[1][0]=transpose(results[1][0],n,k)
        results[2][0]=transpose(results[2][0],n,k)
        chessboard_points=transpose(chessboard_points, n, k)
    print("---------------------------------------")  
    print("Chessboard with points:")        
    print(chessboard_points)
    print("---------------------------------------")    
    print("Optimal solution (Bruteforce method):")
    print(results[0][0])
    print("Total points :", results[0][1])
    print("Time: ", results[0][2])
    print("---------------------------------------")
    print("Optimal solution (Max-in-row method):")
    print(results[1][0])
    print("Total points :", results[1][1])
    print("Time: ", results[1][2])
    print("---------------------------------------")
    print("Optimal solution (Max-on-board method):")
    print(results[2][0])
    print("Total points :", results[2][1])
    print("Time: ", results[2][2])
    print("---------------------------------------") 
    
    names=["Method: Bruteforce", "Method: Max-in-row", "Method: Max-on-board"]
    
    pygame.init()
    running=True
    choice=0
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            if event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT: 
                surface.fill((94,155,233)) 
                if choice>=2: choice=2 #wybor metody przesuwa sie strzalka
                else: choice=choice+1
                texts(names[choice], width/2,60,25,color2)
                texts('Time [s]: '+str(results[choice][2]),width/2,85,20,color2)
                texts('Points: '+str(results[choice][1]),width/2,105,20,color2)
                drawing(results[choice][0])
            elif event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT:  
                surface.fill((94,155,233))
                if choice<=0: choice=0 #wybor metody przesuwa sie strzalka
                else: choice=choice-1
                texts(names[choice], width/2,60,32,color2)
                texts('Time [s]: '+str(results[choice][2]),width/2,85,20,color2)
                texts('Points: '+str(results[choice][1]),width/2,105,20,color2)
                drawing(results[choice][0])
                

    
   
if __name__=="__main__":
    main()
