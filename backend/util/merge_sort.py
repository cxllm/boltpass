def merge_sort(arr: list, by_key: str) -> list:
    """
    Sort a list using the merge sort algorithm

        Parameters:
            arr (list): The list to be sorted
            by_key (str): What key/attribute to sort the list by

        Returns:
            sorted (list): The sorted list

    """
    # base case: if the array has one or zero elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # split the array into two halves.
    mid = len(arr) // 2  # integer divide to find the middle so no decimals
    left_half = merge_sort(arr[:mid], by_key)  # run algorithm again on left
    right_half = merge_sort(arr[mid:], by_key)  # run algorithm again on right

    # merge the two sorted halves and return the result.
    return merge(left_half, right_half, by_key)


def merge(left: list, right: list, by_key: str) -> list:
    """
    Merge two arrays in merge sort so they become sorted

        Parameters:
            left (list): The left list to be merged
            right (list): The right list to be merged
            by_key (list): What key/attribute to sort the two lists by

        Returns:
            sorted (list): The merged and sorted list
    """
    sorted_array = []
    left_index, right_index = 0, 0

    # compare elements from both halves and add the smallest to the sorted array.
    while left_index < len(left) and right_index < len(right):
        if left[left_index][by_key] < right[right_index][by_key]:
            sorted_array.append(left[left_index])
            left_index += 1
        else:
            sorted_array.append(right[right_index])
            right_index += 1

    # add any remaining elements from the left half.
    sorted_array.extend(left[left_index:])
    # add any remaining elements from the right half.
    sorted_array.extend(right[right_index:])

    return sorted_array
