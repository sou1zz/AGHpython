from multiprocessing import Pool
from typing import List
import random
import time
import matplotlib.pyplot as plt


# 1. Klasa liczb zespolonych z przeciążeniem operatorów
class ComplexNumber:
    def __init__(self, real: float, imag: float):
        self.real = real
        self.imag = imag

    def __add__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real + other.real, self.imag + other.imag)
        raise TypeError("Dodawanie możliwe tylko dla liczb zespolonych.")

    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
            return ComplexNumber(self.real - other.real, self.imag - other.imag)
        raise TypeError("Odejmowanie możliwe tylko dla liczb zespolonych.")

    def __str__(self):
        return f"{self.real} + {self.imag}i"


# 2. Równoległe sortowanie z multiprocessing
def parallel_sort(numbers: List[int], num_processes: int) -> List[int]:
    
    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

    with Pool(num_processes) as pool:
        sorted_chunks = pool.map(sorted, chunks)

    # Łączenie posortowanych części
    while len(sorted_chunks) > 1:
        sorted_chunks.append(merge(sorted_chunks.pop(0), sorted_chunks.pop(0)))

    return sorted_chunks[0]


def merge(left: List[int], right: List[int]) -> List[int]:
    """Łączy dwie posortowane listy w jedną posortowaną."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# 3. Testy i analiza wydajności sortowania
def benchmark_sorting():
    
    sizes = [10_000, 50_000, 100_000, 500_000]
    processes = [2, 4, 8]
    results = []

    for size in sizes:
        numbers = [random.randint(0, 1_000_000) for _ in range(size)]
        for proc in processes:
            start_time = time.time()
            parallel_sort(numbers, proc)
            elapsed_time = time.time() - start_time
            results.append((size, proc, elapsed_time))
            print(f"Rozmiar: {size}, Procesy: {proc}, Czas: {elapsed_time:.2f}s")

    # Rysowanie wykresu
    plot_results(results)


def plot_results(results):
    
    sizes = sorted(set(result[0] for result in results))
    processes = sorted(set(result[1] for result in results))

    for proc in processes:
        times = [result[2] for result in results if result[1] == proc]
        plt.plot(sizes, times, label=f'Liczba procesów: {proc}')

    plt.xlabel('Rozmiar danych')
    plt.ylabel('Czas [s]')
    plt.title('Porównanie wydajności sortowania równoległego')
    plt.legend()
    plt.grid()
    plt.show()


# 4. Iterator Fibonacciego
class Fibonacci:
    
    def __init__(self, steps: int):
        self.steps = steps
        self.current_step = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_step >= self.steps:
            raise StopIteration
        self.current_step += 1
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result


if __name__ == "__main__":
    # Zadanie 1: Liczby zespolone
    c1 = ComplexNumber(3, 4)
    c2 = ComplexNumber(1, -2)
    print("Dodawanie:", c1 + c2)
    print("Odejmowanie:", c1 - c2)

    # Zadanie 2: Sortowanie równoległe
    numbers = [random.randint(0, 100) for _ in range(20)]
    print("Liczby:", numbers)
    print("Posortowane:", parallel_sort(numbers, 4))

    # Zadanie 3: Benchmarking
    benchmark_sorting()

    # Zadanie 4: Fibonacci
    fib = Fibonacci(steps=10)
    print("Ciąg Fibonacciego:")
    for num in fib:
        print(num)
