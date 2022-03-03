import pygame 
import random 
import math 
pygame.init()

class DrawInformation:
    BLACK = (0, 0, 0)
    WHITE = (250, 250, 250)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BACKGROUND_COLOR = WHITE 

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('corbel', 25)
    LARGE_FONT = pygame.font.SysFont('corbel', 40)
    SIDE_PAD = 100 # padding on left and right 
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithms Visualizer")
        self.set_lst(lst)
    
    def set_lst(self, lst):
        self.lst = lst 
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2




def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - In {'Ascending' if ascending else 'Descending'} Order", 1, draw_info.BLUE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | ENTER - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | H - Heap Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    draw_list(draw_info)
    pygame.display.update()




def draw_list(draw_info, color_positions={}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i*draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()




def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst



def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst) -1 - i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j:draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    
    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current 
            draw_list(draw_info, {i-1: draw_info.GREEN, i:draw_info.RED}, True)
            yield True
    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for step in range(len(lst)):
        min_idx = step

        for i in range(step+1, len(lst)):
            if ascending:
                if lst[i] < lst[min_idx]:
                    min_idx = i 
            else:
                if lst[i] > lst[min_idx]:
                    min_idx = i 
            draw_list(draw_info, {step: draw_info.GREEN, min_idx: draw_info.RED}, True)
            yield True 
        
        lst[step], lst[min_idx] = lst[min_idx], lst[step]
    
    return lst 




def max_heapify(lst, n, i):
    largest = i 
    l = 2*i + 1
    r = 2*i + 2

    if l < n and lst[i] < lst[l]:
        largest = l 
    
    if r < n and lst[largest] < lst[r]:
        largest = r 
    
    if largest != i:
        lst[i], lst[largest] = lst[largest], lst[i]
        max_heapify(lst, n, largest)

# def min_heapify(lst, n, i):
#     smallest = i 
#     l = 2*i + 1
#     r = 2*i + 2

#     if l < n and lst[l] < lst[smallest]:
#         smallest = l  
    
#     if r < n and lst[r] < lst[smallest]:
#         smallest = r 
    
#     if smallest != i:
#         lst[i], lst[smallest] = lst[smallest], lst[i]
    
#     min_heapify(lst, n, smallest)

def heap_sort(draw_info, ascending = True):
    lst = draw_info.lst
    n = len(lst)

    if ascending or not ascending:
        for i in range(n//2, -1, -1):
            max_heapify(lst, n, i)
            draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
            yield True
        
        for i in range(n-1, 0, -1):
            lst[i], lst[0] = lst[0], lst[i]
            max_heapify(lst, i ,0)
            draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
            yield True
    # else:
    #     for i in range(int(n/2) -1, -1, -1):
    #         min_heapify(lst, n, i)
    #         draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
    #         yield True
    #     for i in range(n-1, -1, -1):
    #         lst[i], lst[0] = lst[0], lst[i]
    #         min_heapify(lst, i ,0)
    #         draw_list(draw_info, {i: draw_info.GREEN, 0: draw_info.RED}, True)
    #         yield True
    
    return lst 



def main():
    run = True 
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False 
    ascending = True 

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None 

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_lst(lst)
                sorting = False

            elif event.key == pygame.K_RETURN and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
                
            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"

            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algorithm_name = "Heap Sort"
            

    
    pygame.quit()


if __name__ == "__main__":
    main()