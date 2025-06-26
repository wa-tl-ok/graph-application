import heapq
from tkinter import *
import time

global Gl, Gs, N, holst
N = 0
dot = {}
num_node = {}
line = {}
Set = []
Q = []
n = 0
nodes = []
Graph = []
holst = 1

def is_two_integers(input_str):
    if input_str[0]==" " or input_str[-1]==" " or input_str=="":
        return False
    try:
        num1, num2 = map(int, input_str.split())
        for i in range(len(input_str)-1):
            if input_str[i]==" " and input_str[i+1]==" ":
                return False
        return True
    except ValueError:
        return False

def is_number(input_str):
    if input_str[0]==" " or input_str[-1]==" " or input_str=="":
        return False
    try:
        float(input_str)
        return True
    except ValueError:
        return False

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def get_kord_to_draw(x, y):
    global Gs, Gl, N
    global nodes
    x_start = (Gs-Gl)//2
    y_start = (Gs-Gl)//2
    now_x = 0
    now_y = 0
    while now_x < x:
        now_x += 1
        x_start += Gl
    while now_x > x:
        now_x -= 1
        x_start -= Gl
    while now_y < y:
        now_y += 1
        y_start -= Gl
    while now_y > y:
        now_y -= 1
        y_start += Gl
    X1 = (x_start + Gl // 10 + Gl)
    Y1 = (y_start + Gl // 10 + Gl)
    X2 = (x_start + Gl - Gl // 10 + Gl)
    Y2 = (y_start + Gl - Gl // 10 + Gl)
    return X1, Y1, X2, Y2

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def update_numbers_nodes():
    for i in range(0, 21):
        if i in num_node:
            canvas.delete(num_node[i])
    for i in range(len(nodes)):
        x = nodes[i][0]; y = nodes[i][1]
        X1, Y1, X2, Y2 = get_kord_to_draw(x, y)
        num_node[i] = canvas.create_text((X1 + X2)//2, (Y1 + Y2)//2, text=str(i + 1), font=('Courier', l//2), fill="red")

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def count_components(graph):
    n = len(graph)
    visited = [False] * n
    def dfs(v):
        visited[v] = True
        for u, _ in graph[v]:
            if not visited[u]:
                dfs(u)
    components = 0
    for v in range(n):
        if not visited[v]:
            dfs(v)
            components += 1
    return components

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def dijkstra(graph, start, end):
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == end:
            return dist[u]
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return -1

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def tsp(G): 
    if count_components(G) > 1: 
        return -1 
    n = len(G) + 1
    a = [[-1] * n for i in range(n)]
    for v in range(n - 1):
        for P in G[v]:
            u = P[0]
            w = P[1]
            a[u + 1][v + 1] = w
            a[v + 1][u + 1] = w

    for i in range(1, n):
        a[i][0] = 0
        a[0][i] = 0

    N = 1 << n
    dp = [[float('inf')] * n for _ in range(N)]
    pr = [[0] * n for _ in range(N)]

    dp[1][0] = 0
    pr[1][0] = -1

    for i in range(2, N):
        for j in range(n):
            for k in range(n):
                if j != k and (i >> j) & 1 == 1 and (i >> k) & 1 == 1:
                    if a[j][k] >= 0:
                        if dp[i][k] > dp[i ^ (1 << k)][j] + a[j][k]:
                            dp[i][k] = min(dp[i][k], dp[i ^ (1 << k)][j] + a[j][k])
                            pr[i][k] = j

    fg = 0
    for i in range(n):
        if dp[(1 << n) - 1][i] <= float('inf'):
            fg = 1

    if fg == 0:
        return -1

    ans = []
    A = float('inf')
    ms = (1 << n) - 1
    go = 0
    for i in range(n):
        if dp[ms][i] < dp[ms][go]:
            go = i

    A = dp[ms][go]
    return A

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def add_node():
    S = str(text_entry_2.get())
    if is_two_integers(S) == False:
        return;
    x, y = int(str(text_entry_2.get()).split(" ")[0]), int(str(text_entry_2.get()).split(" ")[1])
    if [x, y] in nodes:
        return;
    to_add_node(x, y)

def add_edge():
    global N
    S = str(text_entry_4.get())
    if is_two_integers(S) == False:
        return;    
    u, v = int(str(text_entry_4.get()).split(" ")[0]), int(str(text_entry_4.get()).split(" ")[1])
    if u>N or v>N:
        return;    
    x1 = nodes[u - 1][0]
    y1 = nodes[u - 1][1]
    x2 = nodes[v - 1][0]
    y2 = nodes[v - 1][1]
    to_add_edge(u, x1, y1, v, x2, y2)

def remove_node():
    global N
    global Graph
    S = str(text_entry_1.get())
    if is_number(S)==False:
        return;
    u = int(text_entry_1.get())
    if u > N:
        return;
    while Graph[u - 1]:
        v = Graph[u - 1][0][0] + 1
        erase_reference(u, v)
        to_remove_edge(u, v)
    to_remove_node(u)

def remove_edge():
    global N
    S = str(text_entry_3.get())
    if is_two_integers(S) == False:
        return;    
    u, v = int(str(text_entry_3.get()).split(" ")[0]), int(str(text_entry_3.get()).split(" ")[1])
    if u>N or v>N:
        return;     
    erase_reference(u, v)
    to_remove_edge(u, v)

def find_dist_u_v():
    S = str(text_entry_5.get())
    if is_two_integers(S) == False:
        return;    
    u, v = int(str(text_entry_5.get()).split(" ")[0]), int(str(text_entry_5.get()).split(" ")[1])     
    getans_u_v(u, v) 

def find_shortest_u_v():
    global N, Gl, Gs
    global Graph
    size = Gs
    l = Gl
    if len(Graph)==0:
        answer_dist = -1
    else:
        answer_dist=tsp(Graph)
        answer_dist = round(answer_dist, 3)
    if answer_dist==-1:
        canvas.create_rectangle(size + 8*l, size//2 + 6*l, size + 12*l, size//2 + 7*l, fill="old lace", outline="old lace")
        canvas.create_text(size + 10*l, size//2 + 6.5*l, text="No path", font=('Courier', l//2), fill="black") 
    else:
        canvas.create_rectangle(size + 8*l, size//2 + 6*l, size + 12*l, size//2 + 7*l, fill="old lace", outline="old lace")
        canvas.create_text(size + 10*l, size//2 + 6.5*l, text=str(answer_dist), font=('Courier', l//2), fill="black") 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def to_add_node(x, y):
    global Gl, Gs, N
    global Graph, nodes
    if N==20:
        return;
    else:
        if abs(x) > 10 or abs(y) > 10:
            return;
        else:
            nodes += [[x, y]]
            Graph += [[]]    
    X1, Y1, X2, Y2 = get_kord_to_draw(x, y)
    dot[N] = canvas.create_oval(X1, Y1, X2, Y2, fill="black", outline="black")
    num_node[N] = canvas.create_text((X1 + X2)//2, (Y1 + Y2)//2, text=str(N + 1), font=('Courier', l//2), fill="red") 
    N += 1
    count_edges_nodes_components()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def to_remove_node(delete_u):
    global N
    global Graph, nodes
    global Set
    if delete_u > N or len(Graph[delete_u - 1]) > 0:
        return;
    Det = []
    for i in range(len(Set)):
        u = Set[i][0]
        v = Set[i][1]
        Det += [[u, v]]
        Det += [[v, u]]
    while Set:
        to_remove_edge(Set[-1][0], Set[-1][1])    
    canvas.delete(dot[delete_u - 1])
    for i in range(delete_u - 1, N - 1):
        dot[i]=dot[i+1]
    delete_u -= 1
    del nodes[delete_u]
    for i in range(delete_u, N - 1):
        Graph[i] = Graph[i + 1].copy()
    N -= 1
    del Graph[-1]
    for i in range(N):
            ind = -1
            for j in range(len(Graph[i])):
                if Graph[i][j][0]==delete_u:
                    ind=j
            if ind != -1:
                del Graph[i][ind]
    for i in range(N):
        for j in range(len(Graph[i])):
            if Graph[i][j][0]>delete_u:
                Graph[i][j][0] -= 1
    delete_u += 1
    for i in range(len(Det)):
        u = Det[i][0]
        v = Det[i][1]
        a = u
        b = v
        if a >= delete_u:
            a -= 1
        if b >= delete_u:
            b -= 1
        Det[i][0] = a
        Det[i][1] = b
        u = a
        v = b
        x1 = nodes[u - 1][0]
        y1 = nodes[u - 1][1]
        x2 = nodes[v - 1][0]
        y2 = nodes[v - 1][1]
        to_add_edge(u, x1, y1, v, x2, y2)
    update_numbers_nodes()
    count_edges_nodes_components()
    peresroyka()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def to_add_edge(u, x1, y1, v, x2, y2):
    global Set
    if [u, v] in Set or [v, u] in Set:
        return;
    global N, Gs, Gl
    global Graph, nodes
    x_start1 = (Gs-Gl)//2
    y_start1 = (Gs-Gl)//2
    now_x1 = 0
    now_y1 = 0
    while now_x1 < x1:
        now_x1 += 1
        x_start1 += Gl
    while now_x1 > x1:
        now_x1 -= 1
        x_start1 -= Gl
    while now_y1 < y1:
        now_y1 += 1
        y_start1 -= Gl
    while now_y1 > y1:
        now_y1 -= 1
        y_start1 += Gl  
    x_start2 = (Gs-Gl)//2
    y_start2 = (Gs-Gl)//2
    now_x2 = 0
    now_y2 = 0
    while now_x2 < x2:
        now_x2 += 1
        x_start2 += Gl
    while now_x2 > x2:
        now_x2 -= 1
        x_start2 -= Gl
    while now_y2 < y2:
        now_y2 += 1
        y_start2 -= Gl
    while now_y2 > y2:
        now_y2 -= 1
        y_start2 += Gl 
    line[(u, v)] = canvas.create_line(x_start1 + l + Gl // 2, y_start1 + l + Gl // 2, x_start2 + Gl + l - Gl // 2, y_start2 + Gl + l - Gl // 2, fill="black", width=2)
    line[(v, u)] = canvas.create_line(x_start1 + l + Gl // 2, y_start1 + l + Gl // 2, x_start2 + Gl + l - Gl // 2, y_start2 + Gl + l - Gl // 2, fill="black", width=2)
    Set+=[[u,v]]
    Set+=[[v,u]]
    u -= 1; v -= 1;
    x1 = nodes[u][0]
    y1 = nodes[u][1]
    x2 = nodes[v][0]
    y2 = nodes[v][1]              
    Graph[u] += [[v, (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)]]
    Graph[v] += [[u, (((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5)]]  
    update_numbers_nodes()
    count_edges_nodes_components()
    u += 1; v += 1
    draw_reference(u, v)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def to_remove_edge(u, v):
    global Graph, nodes
    global Set
    if [u, v] in Set:
        del Set[Set.index([u, v])]
        canvas.delete(line[(u, v)])
        u -= 1
        v -= 1
        ind = -1
        for i in range(len(Graph[u])):
            if Graph[u][i][0]==v:
                ind = i
        if ind != -1:
            del Graph[u][ind]
        ind = -1
        for i in range(len(Graph[v])):
            if Graph[v][i][0]==u:
                ind = i
        if ind != -1:
            del Graph[v][ind]   
        u += 1
        v += 1
    if [v, u] in Set:
        del Set[Set.index([v, u])]
        canvas.delete(line[(v, u)])
        u -= 1
        v -= 1
        ind = -1
        for i in range(len(Graph[u])):
            if Graph[u][i][0]==v:
                ind = i
        if ind != -1:
            del Graph[u][ind]
        ind = -1
        for i in range(len(Graph[v])):
            if Graph[v][i][0]==u:
                ind = i
        if ind != -1:
            del Graph[v][ind]   
        u += 1
        v += 1
    count_edges_nodes_components()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def getans_u_v(u, v):
    global N, Gl, Gs
    size = Gs
    l = Gl
    if u > N or v > N:
        canvas.create_rectangle(size + 6*l, size//2 + 3.5*l, size + 14*l, size//2 + 4.5*l, fill="old lace", outline="old lace")
        canvas.create_text(size + 10*l, size//2 + 4*l, text="Nodes not found", font=('Courier', l//2), fill="black") 
    else:
        u -= 1; v -= 1
        ans = dijkstra(Graph, u, v)
        ans = round(ans, 3)
        if ans==-1:
            canvas.create_rectangle(size + 6*l, size//2 + 3.5*l, size + 14*l, size//2 + 4.5*l, fill="old lace", outline="old lace")
            canvas.create_text(size + 10*l, size//2 + 4*l, text="No path", font=('Courier', l//2), fill="black") 
        else:
            canvas.create_rectangle(size + 6*l, size//2 + 3.5*l, size + 14*l, size//2 + 4.5*l, fill="old lace", outline="old lace")
            canvas.create_text(size + 10*l, size//2 + 4*l, text=str(ans), font=('Courier', l//2), fill="black") 
    count_edges_nodes_components()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

def switch_canvas():
    global holst
    if canvas.winfo_viewable():
        holst = 2
        canvas.pack_forget()
        Instruction.pack_forget()
        reference_canvas.pack()
    else:
        holst = 1
        reference_canvas.pack_forget()
        canvas.pack()

def switch_canvas_instruction():
    global holst
    if canvas.winfo_viewable():
        holst = 3
        canvas.pack_forget()
        reference_canvas.pack_forget()
        Instruction.pack()
        type_text(S, text_id)
    else:
        holst = 1
        Instruction.pack_forget()
        canvas.pack()

def close_window():
    tk.destroy()

def get_button_width(button):
    return button.winfo_reqwidth()

def Make_1():
    tk.attributes('-fullscreen', False)

def Make_2():
    tk.attributes('-fullscreen', True)

def Make_clear():
    global N
    global Graph
    for u in range(N, 0, -1):
        while Graph[u - 1]:
            v = Graph[u - 1][0][0] + 1
            erase_reference(u, v)
            to_remove_edge(u, v)
        to_remove_node(u)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

tk = Tk()
tk.title('App')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.attributes('-fullscreen', True)

screen_width = tk.winfo_screenwidth() 
screen_height = tk.winfo_screenheight() 

canvas = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0, background='old lace')
canvas.pack()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

size = int(min(screen_width, screen_height) * 6 / 7) // 20 * 20
l = size // 20
Gl = l
Gs = size

text_entry_1 = Entry(canvas)
node_remove = canvas.create_window(size + 2.5*l, size//2, window=text_entry_1, anchor='nw')
button_node_remove = Button(canvas, text="Remove node (u)", command=remove_node)
button_window_node_remove = canvas.create_window(size + 2.5*l, size//2 + l, window=button_node_remove, anchor='nw')

text_entry_2 = Entry(canvas)
node_add = canvas.create_window(size + 2.5*l, size//2 - 3*l, window=text_entry_2, anchor='nw')
button_node_add = Button(canvas, text="Add node (x, y)", command=add_node)
button_window_node_add = canvas.create_window(size + 2.5*l, size//2 - 2*l, window=button_node_add, anchor='nw')

text_entry_3 = Entry(canvas)
edge_remove = canvas.create_window(size + 2.5*l, size//2 - 6*l, window=text_entry_3, anchor='nw')
button_edge_remove = Button(canvas, text="Remove edge (u, v)", command=remove_edge)
button_window_edge_remove = canvas.create_window(size + 2.5*l, size//2 - 5*l, window=button_edge_remove, anchor='nw')

text_entry_4 = Entry(canvas)
edge_add = canvas.create_window(size + 2.5*l, size//2 - 9*l, window=text_entry_4, anchor='nw')
button_edge_add = Button(canvas, text="Add edge (u, v)", command=add_edge)
button_window_edge_add = canvas.create_window(size + 2.5*l, size//2 - 8*l, window=button_edge_add, anchor='nw')

text_entry_5 = Entry(canvas)
dist_u_v = canvas.create_window(size + 2.5*l, size//2 + 3*l, window=text_entry_5, anchor='nw')
button_dist_u_v = Button(canvas, text="Dist between (u, v)", command=find_dist_u_v)
button_window_dist_u_v = canvas.create_window(size + 2.5*l, size//2 + 4*l, window=button_dist_u_v, anchor='nw')

button_shortest_u_v = Button(canvas, text="Shortest path", command=find_shortest_u_v)
button_window_shortest_u_v = canvas.create_window(size + 2.5*l, size//2 + 6*l, window=button_shortest_u_v, anchor='nw')

Cleaaar = Button(canvas, text="Clear", command=Make_clear)
button_window_shortest_u_v = canvas.create_window(size + 2.5*l, size//2 + 8*l, window=Cleaaar, anchor='nw')

reference_button = Button(canvas, text="Info", command=switch_canvas)
reference_button_window = canvas.create_window(size + 2.5*l, size//2 + 10*l, window=reference_button, anchor='nw')

Instruction = Button(canvas, text="❓", command=switch_canvas_instruction, width=int(0.25*l), height=int(0.1*l), bg='grey')
Insruction_button_window = canvas.create_window(screen_width - get_button_width(Instruction) - 0.2*l, screen_height - 2*l, window=Instruction, anchor='nw')

canvas.create_line(0, Gs//2+Gl, Gs+Gl*2, Gs//2+Gl, fill="red", width=2)
canvas.create_line(Gs+Gl*2, Gs//2+Gl, Gs+Gl+Gl*0.5, Gs//2+2*Gl-Gl*0.5, fill="red", width=2)
canvas.create_line(Gs+Gl*2, Gs//2+Gl, Gs+Gl+Gl*0.5, Gs//2+Gl*0.5, fill="red", width=2)
canvas.create_text(Gs+Gl*1.7, Gs//2+Gl*1.9, text=str(X), font=('Courier', l), fill="black") 
canvas.create_line(Gs//2+Gl, 0, Gs//2+Gl, Gs+Gl*2, fill="red", width=2)
canvas.create_line(Gs//2+Gl, 0, Gs//2+Gl+0.5*Gl, Gl*0.5, fill="red", width=2)
canvas.create_line(Gs//2+Gl, 0, Gs//2+Gl-0.5*Gl, Gl*0.5, fill="red", width=2)
canvas.create_text(Gs//2+Gl*0.2, 0.3*Gl, text=str(Y), font=('Courier', l), fill="black")

def clicked(event):
    global nodes, N
    click_x, click_y = event.x, event.y
    for x in range(-10, 11):
        for y in range(-10, 11):
            p1 = x + 10 + 1
            p2 = abs(y - 10) + 1
            x1 = p1 * l - 0.5 * l
            y1 = p2 * l - 0.5 * l
            x2 = p1 * l + 0.5 * l
            y2 = p2 * l + 0.5 * l
            if x1 <= click_x <= x2 and y1 <= click_y <= y2:
                if [x, y] not in nodes:
                    to_add_node(x, y)
                else:
                    for i in range(N):
                        if nodes[i][0] == x and nodes[i][1] == y:
                            u = i + 1
                            while Graph[u - 1]:
                                v = Graph[u - 1][0][0] + 1
                                erase_reference(u, v)
                                to_remove_edge(u, v)    
                            to_remove_node(u)
                            break

canvas.bind("<Button-1>", clicked)

global start_x
global start_y

def on_right_button_down(event):
    global start_x
    global start_y    
    start_x = event.x
    start_y = event.y

def on_right_button_drag(event):
    global start_x
    global start_y    
    canvas.delete("temp_line")
    canvas.create_line(start_x, start_y, event.x, event.y, tags="temp_line", fill="blue")

def on_right_button_up(event):
    global start_x
    global start_y    
    canvas.delete("temp_line")

    u1 = -1
    u2 = -1
    sx1 = -1
    sy1 = -1
    sx2 = -1
    sy2 = -1

    X1 = start_x
    Y1 = start_y
    X2 = event.x
    Y2 = event.y

    for x in range(-10, 11):
        for y in range(-10, 11):
            p1 = x + 10 + 1
            p2 = abs(y - 10) + 1
            x1 = p1 * l - 0.5 * l
            y1 = p2 * l - 0.5 * l
            x2 = p1 * l + 0.5 * l
            y2 = p2 * l + 0.5 * l
            if x1 <= X1 <= x2 and y1 <= Y1 <= y2:
                if [x, y] not in nodes:
                    pass
                else:
                    sx1 = x
                    sy1 = y
                    for i in range(N):
                        if nodes[i][0] == x and nodes[i][1] == y:
                            u1 = i + 1    

    for x in range(-10, 11):
        for y in range(-10, 11):
            p1 = x + 10 + 1
            p2 = abs(y - 10) + 1
            x1 = p1 * l - 0.5 * l
            y1 = p2 * l - 0.5 * l
            x2 = p1 * l + 0.5 * l
            y2 = p2 * l + 0.5 * l
            if x1 <= X2 <= x2 and y1 <= Y2 <= y2:
                if [x, y] not in nodes:
                    pass
                else:
                    sx2 = x
                    sy2 = y
                    for i in range(N):
                        if nodes[i][0] == x and nodes[i][1] == y:
                            u2 = i + 1 

    if u1 != -1 and u2 != -1:
        global Set
        if [u1, u2] in Set or [u2, u1] in Set:
            to_remove_edge(u1, u2)
        else:
            to_add_edge(u1, sx1, sy1, u2, sx2, sy2)

    start_x = None
    start_y = None

canvas.bind("<Button-3>", on_right_button_down)
canvas.bind("<B3-Motion>", on_right_button_drag)
canvas.bind("<ButtonRelease-3>", on_right_button_up)

for i in range(0, size + 1, size // 20):
    canvas.create_line(0 + l, i + l, size // 20 * 20 + l, i + l, fill="red")
    canvas.create_line(i + l, 0 + l, i + l, size // 20 * 20 + l, fill="red")

pp=10
for i in range(1, 22):
    if pp<=0:
        canvas.create_text(i*l, Gs//2+l, text=str(-pp), font=('Courier', l//2, 'bold'), fill="black")
    else:
        canvas.create_text(i*l, Gs//2+l, text=str(-pp)+" ", font=('Courier', l//2, 'bold'), fill="black")
    if pp!=0:
        if pp<0:
            canvas.create_text(Gs//2+l, i*l, text=str(pp)+" ", font=('Courier', l//2, 'bold'), fill="black") 
        else:
            canvas.create_text(Gs//2+l, i*l, text=str(pp), font=('Courier', l//2, 'bold'), fill="black") 
    pp-=1

nodesCopy = nodes.copy()
nodes=[]
for i in range(len(nodesCopy)):
    kords = nodesCopy[i]
    to_add_node(kords[0], kords[1])
for i in range(n):
    for j in range(n):
        if S[i][j] != 0:
            x1 = nodes[i][0]
            y1 = nodes[i][1]
            x2 = nodes[j][0]
            y2 = nodes[j][1]
            to_add_edge(i+1, x1, y1, j+1, x2, y2)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

reference_canvas = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0, background='old lace')
reference_canvas.pack()

button_window_2 = Button(reference_canvas, text="Finish", command=close_window, bg='red')
button_window_2.place(x=screen_width-get_button_width(button_window_2), y=0)

b1 = Button(reference_canvas, text="Window mode", command=Make_1, bg='red')
b1.place(x=screen_width - get_button_width(button_window_2) - l - get_button_width(b1), y=0)

b2 = Button(reference_canvas, text="Fullscrean", command=Make_2, bg='red')
b2.place(x=screen_width - get_button_width(button_window_2) - l - get_button_width(b1) - l - get_button_width(b2), y=0)

Button_switch_2 = Button(reference_canvas, text="To the main page", command=switch_canvas)
Button_switch_2.place(x=screen_width - get_button_width(button_window_2) - l - get_button_width(b1) - l - get_button_width(b2) - l - get_button_width(Button_switch_2), y=0)

#
# Main page start
#

BUTTON = Button(tk, text="Finish", command=close_window, bg='red')
button_window = canvas.create_window(screen_width, 0, window=BUTTON, anchor='ne') 

BUTTON = Button(tk, text="Window mode", command=Make_1, bg='red')
button_window = canvas.create_window(screen_width - get_button_width(button_window_2) - l, 0, window=BUTTON, anchor='ne') 

BUTTON = Button(tk, text="Fullscrean", command=Make_2, bg='red')
button_window = canvas.create_window(screen_width - get_button_width(button_window_2) - l - get_button_width(b1) - l, 0, window=BUTTON, anchor='ne') 

#
# Main page finish
#

reference_canvas.create_line(l, l, size // 20 * 20 + l*2, l, fill="red")
reference_canvas.create_line(l, l, l, size // 20 * 20 + l*2, fill="red")
for i in range(0, size + 1, size // 20):
    reference_canvas.create_line(0 + l, i + l*2, size // 20 * 20 + l*2, i + l*2, fill="red")
    reference_canvas.create_line(i + l*2, 0 + l, i + l*2, size // 20 * 20 + l*2, fill="red")

for i in range(1, 21):
    reference_canvas.create_text(1.5*l + i*l, 1.5*l, text=str(i), font=('Courier', l//2), fill="black") 
    reference_canvas.create_text(1.5*l, 1.5*l + i*l, text=str(i), font=('Courier', l//2), fill="black") 

def peresroyka():
    global Graph
    for u in range(1, 20):
        for v in range(u, 21):
            erase_reference(u, v)
    for i in range(len(Graph)):
        u = i+1
        for j in range(len(Graph[i])):
            v = Graph[i][j][0] + 1
            draw_reference(u, v)

def draw_reference(u, v):
    global Graph
    lenth_u_v = 0
    for i in range(len(Graph[u-1])):
        if Graph[u-1][i][0] + 1 == v:
            lenth_u_v = Graph[u-1][i][1]
    lenth_u_v = round(lenth_u_v, 1)
    reference_canvas.create_rectangle((u-1)*l + l*2, (v-1)*l + l*2, (u-1)*l + l*3, (v-1)*l + l*3, fill="pale green", outline="red")
    reference_canvas.create_text((((u-1)*l + l*2)+((u-1)*l + l*3))//2, (((v-1)*l + l*2)+((v-1)*l + l*3))//2, text=str(lenth_u_v), font=('Courier', l//3-1), fill="black")   
    reference_canvas.create_rectangle((v-1)*l + l*2, (u-1)*l + l*2, (v-1)*l + l*3, (u-1)*l + l*3, fill="pale green", outline="red")   
    reference_canvas.create_text((((v-1)*l + l*2)+((v-1)*l + l*3))//2, (((u-1)*l + l*2)+((u-1)*l + l*3))//2, text=str(lenth_u_v), font=('Courier', l//3-1), fill="black")   

def erase_reference(u, v):
    reference_canvas.create_rectangle((u-1)*l + l*2, (v-1)*l + l*2, (u-1)*l + l*3, (v-1)*l + l*3, fill="old lace", outline="red")
    reference_canvas.create_rectangle((v-1)*l + l*2, (u-1)*l + l*2, (v-1)*l + l*3, (u-1)*l + l*3, fill="old lace", outline="red")   

def count_edges_nodes_components():
    count_edges_reference()
    count_nodes_reference()
    count_components_reference()

def count_nodes_reference():
    global N, Gs, Gl
    reference_canvas.create_rectangle(Gs+Gl*9, Gs//2-Gl*3.5, Gs+Gl*12, Gs//2-Gl*1.5, fill="old lace", outline="old lace")
    reference_canvas.create_text(((Gs+Gl*9)+(Gs+Gl*12))//2, ((Gs//2-Gl*3.5)+(Gs//2-Gl*1.5))//2, text=str(N), font=('Courier', l//2), fill="black")     

reference_canvas.create_text(((Gs+Gl*6)+(Gs+Gl*9))//2-2.5*Gl, ((Gs//2-Gl*3.5)+(Gs//2-Gl*1.5))//2, text="Count nodes:", font=('Courier', l//2, 'bold'), fill="black") 

def count_edges_reference():
    global N, Gs, Gl
    global Graph
    k_edges = 0
    for i in range(len(Graph)):
        k_edges += len(Graph[i])
    k_edges = k_edges//2
    reference_canvas.create_rectangle(Gs+Gl*9, Gs//2-Gl*3.5+3*Gl, Gs+Gl*12, Gs//2-Gl*1.5+3*Gl, fill="old lace", outline="old lace")
    reference_canvas.create_text(((Gs+Gl*9)+(Gs+Gl*12))//2, ((Gs//2-Gl*3.5+3*Gl)+(Gs//2-Gl*1.5+3*Gl))//2, text=str(k_edges), font=('Courier', l//2), fill="black")

reference_canvas.create_text(((Gs+Gl*6)+(Gs+Gl*9))//2-2.5*Gl, ((Gs//2-Gl*3.5+3*Gl)+(Gs//2-Gl*1.5+3*Gl))//2, text="Count edges:", font=('Courier', l//2, 'bold'), fill="black")

def count_components_reference():
    global N, Gs, Gl
    global Graph
    k_components = count_components(Graph)
    reference_canvas.create_rectangle(Gs+Gl*9, Gs//2-Gl*3.5+6*Gl, Gs+Gl*12, Gs//2-Gl*1.5+6*Gl, fill="old lace", outline="old lace")
    reference_canvas.create_text(((Gs+Gl*9)+(Gs+Gl*12))//2, ((Gs//2-Gl*3.5+6*Gl)+(Gs//2-Gl*1.5+6*Gl))//2, text=str(k_components), font=('Courier', l//2), fill="black")

reference_canvas.create_text(((Gs+Gl*6)+(Gs+Gl*9))//2-2.5*Gl, ((Gs//2-Gl*3.5+6*Gl)+(Gs//2-Gl*1.5+6*Gl))//2, text="Components:", font=('Courier', l//2, 'bold'), fill="black")

count_edges_nodes_components()

Instruction = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0, background='old lace')
Instruction.pack()

Finish_instruction = Button(Instruction, text="Finish", command=close_window, bg='red')
Finish_instruction.place(x=screen_width-get_button_width(Finish_instruction), y=0)

p1 = Button(Instruction, text="Window mode", command=Make_1, bg='red')
p1.place(x=screen_width - get_button_width(Finish_instruction) - l - get_button_width(p1), y=0)

p2 = Button(Instruction, text="Fullscrean", command=Make_2, bg='red')
p2.place(x=screen_width - get_button_width(Finish_instruction) - l - get_button_width(p1) - l - get_button_width(p2), y=0)

Switch_instruction = Button(Instruction, text="To the main page", command=switch_canvas_instruction)
Switch_instruction.place(x=screen_width - get_button_width(Finish_instruction) - l - get_button_width(p1) - l - get_button_width(p2) - l - get_button_width(Switch_instruction), y=0)

def type_text(text, text_id, char_index=0):
    global holst
    if char_index < len(text) and holst == 3:
        Instruction.itemconfigure(text_id, text=text[:char_index+1])
        Instruction.update()
        Instruction.after(5, type_text, text, text_id, char_index+1)

S = "Инструкция по применению\n\nСписок доступных операций:\nAdd edge (u, v) - добавить ребро, соединяющие две вершины с номерами u и v\nRemove edge (u, v) - удалить ребро, соединяющие две вершины с номерами u и v\nAdd node (x, y) - добавить вершину с целочисленными координатами x, y (|x|<=10; |y|<=10)\nRemove node (u) - удалить вершину с номером u\nDist between (u, v) - найти кратчайший путь в графе между вершинами u и v\nShortest path - найти кратчайший гамильтонов путь в графе\nClear - очистить граф\nInfo - содержит дополнительную информацию о графе\n\nПримечание:\nПри добавлении и удалении ребра между вершинами u и v, должны существовать вершины с такими номерами\nПри удалении вершины из графа с номером u, должна существовать вершина с таким номером\nПри добавлении вершины u, число текущих вершин в графе должно быть строго меньше 20\nПри поиске кратчайшего пути между вершинами u и v, должны существовать вершины с такими номерами\nЕсли добавить уже существующее ребро или существующую вершину, то ничего не произойдет\nЕсли удалить несуществующую вершину или несуществующее ребро, то ничего не произойдет\nВводить все числа нужно через пробел без лишних символов\n\nДобавление и удаление вершин так же можно сделать при помощи ЛКМ\nДобавление и удаление ребер можно сделать, зажав ПКМ"

text_id = Instruction.create_text(l, 2*l, text="", font=("Lora", l//2), fill="black", anchor="nw")

tk.mainloop()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
