# Итоговое задание № 1 - задача № 3  "Проверяем массив на его монотонность"
nums = list(map(int, input("Введите числа через пробел: ").split()))

is_monotonic = all(nums[i] <= nums[i+1] for i in range(len(nums)-1)) or \
               all(nums[i] >= nums[i+1] for i in range(len(nums)-1))

if is_monotonic:
    print("Массив монотонный.")
else:
    print("Массив не является монотонным.")
