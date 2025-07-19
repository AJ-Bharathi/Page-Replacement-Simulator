def optimal_page_replacement(reference_string, frame_size):
    frames = []
    frame_states = []
    page_faults = 0
    
    for i, page in enumerate(reference_string):
        if page not in frames:
            if len(frames) < frame_size:
                frames.append(page)
            else:
                future_uses = {frame: (reference_string[i+1:].index(frame) if frame in reference_string[i+1:] else float('inf')) for frame in frames}
                frame_to_replace = max(future_uses, key=future_uses.get)
                frames.remove(frame_to_replace)
                frames.append(page)
            page_faults += 1
        
        frame_states.append(frames[:])
    
    return page_faults, frame_states
