class OneSampler:
    def make_sample(self, _n: int, d: int) -> list:
        result = []
        for _ in range(_n):
            samples = [0.5 for _ in range(d)]
            result.append(samples)

        return result
