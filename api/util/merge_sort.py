def merge_sort(arr, by_key):
    # base case: if the array has one or zero elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # split the array into two halves.
    mid = len(arr) // 2  # truncate the middle so no decimals
    left_half = merge_sort(arr[:mid], by_key)  # run algorithm again
    right_half = merge_sort(arr[mid:], by_key)

    # merge the two sorted halves and return the result.
    return merge(left_half, right_half, by_key)


def merge(left, right, by_key):
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


if __name__ == "__main__":
    # example
    array = [
        {"test": "hajdkbjsdak", "password": "hUIDJHU"},
        {"test": "zghaioknj", "password": "hUIDJHU"},
        {"test": "aha", "password": "hUIDJHU"},
        {"test": "aahan", "password": "hUIDJHU"},
    ]
    print("Original array:", array)
    sorted_array = merge_sort(array, "test")
    print("Sorted array:", sorted_array)
