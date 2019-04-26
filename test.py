def find_least_operation(l, s):
    if l < s:
        l, s = s, l
    _delta = l - s
    _num_5 = _delta // 5
    _num_2 = (_delta - _num_5 * 5) // 2
    _num_1 = (_delta - _num_5 * 5 - _num_2 * 2)
    return _num_1 + _num_2 + _num_5

print(find_least_operation(1, 17))