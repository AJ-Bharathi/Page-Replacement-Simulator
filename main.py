import matplotlib.pyplot as plt
import pygame
import fifo
import lru
import optimal
import visualize

def main():
    pygame.mixer.init()
    print("\nPage Replacement Algorithm Simulator\n")
    print("1. First-In-First-Out (FIFO)")
    print("2. Least Recently Used (LRU)")
    print("3. Optimal Page Replacement\n")
    
    choice = input("Choose an algorithm (1-3): ")
    reference_string = list(map(int, input("Enter the reference string (space-separated): ").split()))
    frame_size = int(input("Enter the number of frames: "))
    
    faults = 0
    if choice == '1':
        faults = fifo.fifo_page_replacement(reference_string, frame_size)
        print(f"\nFIFO Page Faults: {faults}")
    elif choice == '2':
        faults = lru.lru_page_replacement(reference_string, frame_size)
        print(f"\nLRU Page Faults: {faults}")
    elif choice == '3':
        faults = optimal.optimal_page_replacement(reference_string, frame_size)
        print(f"\nOptimal Page Faults: {faults}")
    else:
        print("Invalid choice! Please enter 1, 2, or 3.")
        return
    
    visualize.show_results(reference_string, frame_size)  # Visualizing results

if __name__ == "__main__":
    main()
