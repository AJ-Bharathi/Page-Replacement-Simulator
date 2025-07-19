import matplotlib.pyplot as plt
import fifo
import lru
import optimal

def show_results(reference_string, frame_size):
    algorithms = ["FIFO", "LRU", "Optimal"]
    page_faults = [
        fifo.fifo_page_replacement(reference_string, frame_size)[0],
        lru.lru_page_replacement(reference_string, frame_size)[0],
        optimal.optimal_page_replacement(reference_string, frame_size)[0]
    ]

    colors = ['red', 'blue', 'green']
    
    print(f"Algorithms: {algorithms}")
    print(f"Page Faults: {page_faults}")
    #print(f"Colors: {colors}")

    plt.bar(algorithms, page_faults, color=colors)
    plt.xlabel("Algorithm")
    plt.ylabel("Page Faults")
    plt.title("Page Faults Comparison")
    plt.show()