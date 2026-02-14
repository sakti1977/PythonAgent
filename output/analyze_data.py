def analyze_data(numbers):
    """
    Analyze a list of numbers and return statistical information.
    
    Args:
        numbers: A list of numeric values
        
    Returns:
        A dictionary containing mean, median, min, max, and count.
        Returns a dictionary with None values if the list is empty.
    """
    # Handle empty list
    if not numbers or len(numbers) == 0:
        return {
            'mean': None,
            'median': None,
            'min': None,
            'max': None,
            'count': 0
        }
    
    try:
        # Convert to list if needed and ensure all elements are numeric
        numbers = [float(x) for x in numbers]
        
        # Calculate count
        count = len(numbers)
        
        # Calculate mean
        mean = sum(numbers) / count
        
        # Calculate median
        sorted_numbers = sorted(numbers)
        if count % 2 == 0:
            median = (sorted_numbers[count // 2 - 1] + sorted_numbers[count // 2]) / 2
        else:
            median = sorted_numbers[count // 2]
        
        # Calculate min and max
        min_val = min(numbers)
        max_val = max(numbers)
        
        return {
            'mean': mean,
            'median': median,
            'min': min_val,
            'max': max_val,
            'count': count
        }
    
    except (ValueError, TypeError):
        raise ValueError("All elements in the list must be numeric values")


# Example usage and testing
if __name__ == "__main__":
    # Test with normal list
    print(analyze_data([1, 2, 3, 4, 5]))
    
    # Test with empty list
    print(analyze_data([]))
    
    # Test with single element
    print(analyze_data([42]))
    
    # Test with floats
    print(analyze_data([1.5, 2.5, 3.5, 4.5]))