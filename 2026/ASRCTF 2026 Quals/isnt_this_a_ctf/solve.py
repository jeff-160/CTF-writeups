def merge_count(arr):
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, left_inv = merge_count(arr[:mid])
    right, right_inv = merge_count(arr[mid:])
    
    merged = []
    inversions = left_inv + right_inv
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions

def solve(input_text):
    tokens = input_text.split()
    idx = 0
    T = int(tokens[idx]); idx += 1
    
    total = 0
    results = []
    for _ in range(T):
        N = int(tokens[idx]); idx += 1
        arr = list(map(int, tokens[idx:idx+N])); idx += N
        _, inv = merge_count(arr)
        results.append(inv)
        total += inv
    
    for r in results:
        print(r)
    
    print(f"\nSum of all answers: {total}")
    print(f"Flag: ASRCTF{{{total}}}")

with open('input.txt', 'r') as f:
    data = f.read()

solve(data)