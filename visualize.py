from algorithms import dfs,bfs,krushkal,dijkstra

def start():
    log = """
Select the algorithm you want to visualize
1. Depth First Search
2. Breadth First Search
3. Dijkstra Algorithm
4. Krushkals Algorithm
5. Exit 
"""
    nodelog = 'Enter the node to start from between 0 to 18 '
    while True:
        choice = int(input(log))
        if choice == 1:
            node = int(input(nodelog))
            dfs.run(node)

        elif choice == 2:
            node = int(input(nodelog))
            bfs.run(node)

        elif choice == 3:
            node = int(input(nodelog))
            dijkstra.run(node)

        elif choice == 4:
            krushkal.run()

        elif choice == 5:
            print("Bye !!")
            exit(0)
        else:
            print("Please enter valid choice!") 
            exit(1)
        print('Success!')
start()

