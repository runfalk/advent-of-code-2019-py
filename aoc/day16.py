from itertools import cycle, islice

from .common import lines_from_file


def iter_pattern(pattern, element_repetitions):
    if not element_repetitions:
        return []
    for p in islice(cycle(pattern), 1, None):
        for _ in range(element_repetitions):
            yield p


def slice_cycled_list(l, start, stop):
    l_len = len(l)
    return [l[i % l_len] for i in range(start, stop)]


def calc_fft(digits, phase):
    digits = split_digits(digits)
    pattern = [0, 1, 0, -1]
    for _ in range(phase):
        for i in range(len(digits)):
            sum_with_pattern = sum(
                d * p
                for d, p in zip(
                    islice(digits, i, None), cycle(iter_pattern(pattern, i + 1))
                )
            )
            digits[i] = abs(sum_with_pattern) % 10
    return join_digits(digits)[:8]


def calc_fast_fft(digits, phase):
    digits = split_digits(digits)
    offset = int(join_digits(digits[:7]))
    total_len = len(digits) * 10_000

    if offset < total_len // 2:
        raise ValueError("It is not possible to run fast FFT for this input")

    # Only run the algorithm for values after the offset we're interested in
    interesting_digits = slice_cycled_list(digits, offset, total_len)
    for _ in range(phase):
        # No multiplication since the second item of the pattern is 1
        sum_by_pattern = sum(d for d in interesting_digits)
        for i in range(len(interesting_digits)):
            curr = interesting_digits[i]
            interesting_digits[i] = abs(sum_by_pattern) % 10
            sum_by_pattern -= curr

    return join_digits(interesting_digits)[:8]


def split_digits(s):
    return list(map(int, s))


def join_digits(digits):
    return "".join(str(d) for d in digits)


def solve(path):
    digits = next(lines_from_file(path))
    return (calc_fft(digits, 100), calc_fast_fft(digits, 100))
