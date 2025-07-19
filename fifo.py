def fifo_page_replacement(reference_string, frame_size):
    queue = []
    frame_states = []  # Store each step's frames
    page_faults = 0
    
    for page in reference_string:
        if page not in queue:
            if len(queue) < frame_size:
                queue.append(page)
            else:
                queue.pop(0)
                queue.append(page)
            page_faults += 1
        
        frame_states.append(queue[:])  # Store current frame state
    
    return page_faults, frame_states
