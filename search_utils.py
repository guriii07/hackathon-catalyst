# search_utils.py

def binary_search_theme(sorted_list, target_name):
    """
    Performs a Binary Search (O(log N)) on a list of objects 
    (like Theme objects) assumed to be sorted by their 'name' attribute.
    """
    low = 0
    high = len(sorted_list) - 1
    
    while low <= high:
        mid = (low + high) // 2
        mid_theme_name = sorted_list[mid].name
        
        # Check if target is present at mid
        if mid_theme_name == target_name:
            return sorted_list[mid] 
        
        # If target is greater, discard the left half
        elif mid_theme_name < target_name:
            low = mid + 1
        
        # If target is smaller, discard the right half
        else:
            high = mid - 1
            
    return None # Element not found