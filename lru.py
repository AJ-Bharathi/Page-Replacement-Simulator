def lru_page_replacement(reference_string, frame_size):
    frames = []
    frame_states = []
    page_faults = 0
    
    for page in reference_string:
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                frames.pop(0)  # Remove least recently used
                frames.append(page)
            page_faults += 1
        else:
            frames.remove(page)
            frames.append(page)
        
        frame_states.append(frames[:])
    
    return page_faults, frame_states