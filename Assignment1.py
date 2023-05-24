from queue import Queue,PriorityQueue

# Common functions

def findPath(parent,dest):
    cx,cy = dest[0],dest[1]
    path=[]
    out=[]
    path.append((cx,cy))
    while parent[(cx,cy)]!=None:
        cx,cy=parent[(cx,cy)]
        path.append((cx,cy))
    path=(path[::-1])
    for i in path:
        a,b=i
        out.append(str(a)+','+str(b))
    output=(' '.join(out))
    return output

def writeFile(path,parent):
    with open('output.txt', 'w') as fp:
        for x in path:
            if path[x] == '':
                fp.write("FAIL\n")
            else:
                mypath = findPath(parent,x)
                fp.write(f"{mypath}\n")
    return


# BFS with single run

def isSafe(x,y,visited,w,h):
    if x>=0 and x<w and y>=0 and y<h and (x,y) not in visited:
        return True
    return False

def bfs(w,h,sx,sy,stamina,d,m):
    q = Queue()
    parent={}
    visited={}

    q.put((sx,sy))
    visited[(sx,sy)]=True
    parent[(sx,sy)]=None
    
    rows=[-1,-1,-1,0,0,1,1,1]
    cols=[-1,0,1,-1,1,-1,0,1]

    while not q.empty():
        cx,cy = q.get()
        
        if (cx,cy) in d:
            d[(cx,cy)] = '*'

        for k in range(8):
            x = cx+rows[k]
            y = cy+cols[k]
            if isSafe(x,y,visited,w,h):
                if m[y][x] <0:
                    if abs(m[cy][cx])>=abs(m[y][x]):
                        q.put((x,y))
                        visited[(x,y)]=True
                        parent[(x,y)]=(cx,cy)
                    else:
                        continue
                else:
                    if (abs(m[cy][cx])+stamina)>=m[y][x]:
                        q.put((x,y))
                        visited[(x,y)] = True
                        parent[(x,y)]=(cx,cy)
                    else:
                        continue
    
    writeFile(d,parent)


# Either use ucs_optimized or ucslikebfs2
class NodeUCS:
    def __init__(self,cost,pos):
        self.cost = cost
        self.pos = pos

    def __lt__(self, other):
        return self.cost < other.cost
    def __le__(self, other):
        return self.cost <= other.cost
    def __gt__(self, other):
        return self.cost > other.cost
    def __ge__(self, other):
        return self.cost >= other.cost
    def __eq__(self, other):
        return self.cost == other.cost

def isSafeUCS(x,y,visited,w,h):
    if x>=0 and x<w and y>=0 and y<h and (x,y) not in visited:
        return True
    return False

def ucs(w,h,sx,sy,stamina,d,m):
    pq = PriorityQueue()
    parent={}
    visited={}

    pq.put(NodeUCS(0,(sx,sy)))

    visited[(sx,sy)]=True
    parent[(sx,sy)]=None
    
    rows=[0,1,-1,0,-1,1,-1,1]
    cols=[1,0,0,-1,-1,1,1,-1]


    while not pq.empty():
        curr = pq.get()
        cst = curr.cost
        cx,cy = curr.pos[0],curr.pos[1]

        if (cx,cy) in d:
            d[(cx,cy)] = '*'

        for k in range(len(rows)):
            
            if(k<4):
                cst=cst+10
            elif(k>=4):
                cst=cst+14

            x = cx+rows[k]
            y = cy+cols[k]
            if isSafeUCS(x,y,visited,w,h):
                if m[y][x] <0:
                    if abs(m[cy][cx])>=abs(m[y][x]):
                        pq.put(NodeUCS(cst,(x,y)))
                        visited[(x,y)]=True
                        parent[(x,y)]=(cx,cy)
                    else:
                        continue
                else:
                    if (abs(m[cy][cx])+stamina)>=m[y][x]:
                        pq.put(NodeUCS(cst,(x,y)))
                        visited[(x,y)] = True
                        parent[(x,y)]=(cx,cy)
                    else:
                        continue
    
    writeFile(d,parent)

# A*

class Node:
    def __init__(self,pos,cost,f,momentum):
        self.pos = pos
        self.cost = cost
        self.f = f
        self.momentum = momentum

    def __lt__(self, next):
        return self.f < next.f
    def __le__(self, next):
        return self.f <= next.f
    def __gt__(self, next):
        return self.f > next.f
    def __ge__(self, next):
        return self.f >= next.f
    def __eq__(self, next):
        return self.pos == next.pos

def isSafeAstar(child,visited,w,h,curr_pos,m,stamina,momentum):
    if child[0]>=0 and child[0]<w and child[1]>=0 and child[1]<h:
        if m[child[1]][child[0]] <0:
            if abs(m[curr_pos[1]][curr_pos[0]])>=abs(m[child[1]][child[0]]): 
                return True
        elif (abs(m[curr_pos[1]][curr_pos[0]])+stamina+momentum)>=m[child[1]][child[0]]:
            return True
    return False

def calculateMomentum(m,cx,cy,x,y):
    return max(abs(m[cy][cx])-abs(m[y][x]),0)

def calculateHeuristic(y1,x1,y2,x2):
    # Diagonal Distance
    return 10*max(abs(y1-y2),abs(x1-x2))+(14-10)*min(abs(y1-y2),abs(x1-x2))

def astar(w,h,start,stamina,d,m):
    openq = PriorityQueue()
    openq.put(((Node(start,0,0,0)),(None,None,start)))
    closeq = []
    
    parent={}
    parent[(None,None,start)]=(None,None,None)

    rows=[-1,1,-1,1,0,1,-1,0]
    cols=[-1,1,1,-1,1,0,0,-1]

    found=False

    while not openq.empty():
        temp = openq.get()
        curr = temp[0]
        parent_list=temp[1]
        
        curr_pos = curr.pos
        cst = curr.cost
        momentum = curr.momentum
        
        # Calculate Path
        if curr_pos == d:
            found=True
            output_path = parent_list
            break

        for k in range(8):
            x = curr.pos[0]+rows[k]
            y = curr.pos[1]+cols[k]
            cst = curr.cost

            if(k<4):
                cst+=14
            else:
                cst+=10

            o,c=False,False

            if isSafeAstar((x,y),closeq,w,h,(curr_pos[0],curr_pos[1]),m,stamina,momentum):
                
                elevation_cost = 0
                elevation_diff = abs(m[y][x])-abs(m[curr_pos[1]][curr_pos[0]])

                if elevation_diff>momentum:
                    elevation_cost = max(0,elevation_diff-momentum)
                
                cst+=elevation_cost

                newh = calculateHeuristic(curr_pos[0],curr_pos[1],x,y)
                newm = calculateMomentum(m,curr_pos[0],curr_pos[1],x,y)
                fcost = newh+cst

                for i in openq.queue:
                    if (x,y) == i[0].pos:
                        o=True
                        op,opt = i
                        break
                for i in closeq:
                    if (x,y) == i[0].pos:
                        c=True
                        cl,clt = i
                        break
                
                if not o and not c:
                    openq.put((((Node((x,y),cst,fcost,newm)),(parent_list[1],(curr.pos[0],curr.pos[1]),(x,y)))))
                    parent[((parent_list[1]),(curr.pos[0],curr.pos[1]),(x,y))]=parent_list
                elif o:
                    if op.f > fcost:
                        openq.queue.remove((op,opt))
                        openq.put(((Node((x,y),cst,fcost,newm)),(parent_list[1],(curr.pos[0],curr.pos[1]),(x,y))))
                        parent[((parent_list[1]),(curr.pos[0],curr.pos[1]),(x,y))]=parent_list
                    elif op.momentum < newm:
                        openq.put(((Node((x,y),cst,fcost,newm)),(parent_list[1],(curr.pos[0],curr.pos[1]),(x,y))))
                        parent[((parent_list[1]),(curr.pos[0],curr.pos[1]),(x,y))]=parent_list
                elif c:
                    if cl.f > fcost:
                        closeq.remove((cl,clt))
                        openq.put(((Node((x,y),cst,fcost,newm)),(parent_list[1],(curr.pos[0],curr.pos[1]),(x,y))))
                        parent[((parent_list[1]),(curr.pos[0],curr.pos[1]),(x,y))]=parent_list
                    elif cl.momentum < newm:
                        openq.put(((Node((x,y),cst,fcost,newm)),(parent_list[1],(curr.pos[0],curr.pos[1]),(x,y))))
                        parent[((parent_list[1]),(curr.pos[0],curr.pos[1]),(x,y))]=parent_list
        
        closeq.append((curr,parent_list))

    if not found:
        output = "FAIL\n"
    else:
        path=[d,output_path[1]]
        while output_path[0]!=None:
            path.append(output_path[0])
            output_path=parent[output_path]
        path.reverse()
        out = []
        for i in path:
            a,b = i
            out.append(str(a)+','+str(b))
        output = (' '.join(out))+'\n'
    return output


if __name__ == '__main__':

    with open('input.txt', 'r') as f:
        extracted_data = f.readlines()

    data = [x.strip() for x in extracted_data]

    algo = data[0]
    w,h = data[1].split(' ')
    sx,sy = data[2].split(' ')
    s = data[3]
    n = int(data[4])
    sx = int(sx)
    sy = int(sy)
    w = int(w)
    h = int(h)
    s = int(s)
    q={}
    m=[]

    l=0
    while(l<n):
        t = data[5+l].split(' ')
        q[(int(t[0]),int(t[1]))]=""
        l+=1

    l+=5
    k=0
    while(k<h):
        t = data[l+k].split(' ')
        m.append([int(x) for x in t])
        k+=1 

    if(algo == 'BFS'):
        bfs(w,h,sx,sy,s,q,m)
    if(algo == 'UCS'):
        ucs(w,h,sx,sy,s,q,m)
    if(algo == 'A*'):
        final_path=""
        for d in q:
            final_path += astar(w,h,(sx,sy),s,d,m)
        
        with open('output.txt', 'w') as fp:
            fp.write(f"{final_path}")
