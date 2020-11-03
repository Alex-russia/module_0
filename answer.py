import numpy as np
import math


def game_core_v2(number):
    '''Сначала устанавливаем любое random число, а потом уменьшаем или 
       увеличиваем его в зависимости от того, больше оно или меньше
       нужного. Функция принимает загаданное число и возвращает число
       попыток'''

    count = 1
    predict = np.random.randint(1, 101)

    while number != predict:
        count+=1

        if number>predict: 
            predict += 1
        elif number<predict: 
            predict -= 1

    return(count) # выход из цикла, если угадали


def game_core_v3(number):
    '''Изначально устанавливаем начальное и конечное значение за
        пределами выборки, т.е 0 и 101, среднее значение берем 50 и
        откидывая по половие ищем загаданное число. В откидываемой
        половине искомого числа нет.'''

    count = 1
    start_number = 0
    end_number = 101
    predict = 50

    while number != predict:
        count += 1

        if end_number-start_number == 2:
            predict = end_number-1
        elif number>predict:
            start_number = predict
            predict = predict + int((end_number - predict)/2)
        else:
            end_number = predict
            predict = start_number + int((predict - start_number)/2)

    return(count) # выход из цикла, если угадали


def game_core_v4(number):
    '''Подход похож на использванный в функции game_core_v3, с той лишь
        разницей, что тут идет разеление области поиска по принципу
        "Золотое сечение"'''

    count = 1
    start_number = 0
    end_number = 101
    predict = int(start_number + (end_number - start_number)*0.61803)

    while number != predict:
        count += 1

        if end_number-start_number == 2:
            start_number = end_number+2
            predict = int((end_number - start_number)/2)
        elif number>predict:
            start_number = predict
            predict = predict + int((end_number - predict)*0.61803)
        else:
            end_number = predict
            predict = start_number + int((predict - start_number)*0.61803)

    return(count) # выход из цикла, если угадали


def game_core_v5(number):
    '''Модификация функции game_core_v4, тут "Золотое сечение"
        отсчитывается попеременно, то с начала, то с конца, для этой
        цели служит флаг countdown'''

    count = 1
    start_number = 0
    end_number = 101
    predict = int(start_number + (end_number - start_number)*0.61803)
    count_down = False

    while number != predict:
        count += 1

        if end_number-start_number==2:
            start_number = end_number+2
            predict = int((end_number - start_number)/2)
        elif number>predict:
            start_number = predict

            if count_down:
                predict = predict + int((end_number - predict)*0.61803)
                count_down = False
            else:
                predict = end_number - int((end_number - predict)*0.61803)
                count_down = True
        else:
            end_number = predict

            if count_down:
                predict = start_number + int((predict - start_number)*0.61803)
                count_down = False
            else:
                predict = predict - int((predict - start_number)*0.61803)
                count_down = True

    return(count) # выход из цикла, если угадали


def game_core_v6(number):
    '''Отсчитываем "Золотое сечение" с двух сторон с начала, и с конца,
    определяем в каком из интервалов находится число, далее повторяем
    действие до победного результата'''

    count = 1
    start_number = 0
    end_number = 101
    first_predict = int(end_number
        - (end_number - start_number)*0.61803)
    second_predict = int(start_number
        + (end_number - start_number)*0.61803)

    while number!=first_predict and number!=second_predict:
        count += 1

        if end_number-start_number==3:
            second_predict = start_number + 2
            first_predict = start_number + 1
        elif number>second_predict:
            start_number = second_predict

            second_predict = int(start_number
                + (end_number - start_number)*0.61803)
            first_predict = int(end_number
                - (end_number - start_number)*0.61803)  
        elif number<first_predict:
            end_number = first_predict
            
            second_predict = int(start_number
                + (end_number - start_number)*0.61803)
            first_predict = int(end_number
                - (end_number - start_number)*0.61803)
        else:
            start_number = first_predict
            end_number = second_predict

            second_predict = int(start_number
                + (end_number - start_number)*0.61803)
            first_predict = int(end_number
                - (end_number - start_number)*0.61803)

    # Одно из двух чисел будет нужноe, для его выбора еще прибавляем один шаг
    count += 1

    return(count) # выход из цикла, если угадали


def game_core_v7(number):
    '''Функция применима для частных случаев (в зависимости от способа
        расчета попыток))). Первоначально делим область поиска на "n" равных
        частей (ну или почти равных))), далее определяем в какой из этих
        частей находится, угадываемое число, далее применить какую нибудь
        из функций выше.'''

    start_number = 0
    end_range = end_number = 101
    n = 10
    step = int((end_number - start_number)/n)
    is_current_number = False

    for i in range(1, n + 1):
        if i!=n:
            end_number = int(step * i)
            start_number = int(end_number - step)
        else:
            start_number = int(step*n - step)
            end_number = end_range

        if number==end_number or number==start_number:
            is_current_number = True
            break
        elif number>start_number and number<end_number:
            break

    count = 1
    
    if is_current_number:
        return(count)

    predict = start_number + int((end_number - start_number)/2)
            
    while number != predict:
        count += 1

        if end_number-start_number == 2:
            predict = end_number - 1
        elif number>predict:
            start_number = predict
            predict = predict + int((end_number - predict)/2)
        else:
            end_number = predict
            predict = start_number + int((predict - start_number)/2)

    return(count) # выход из цикла, если угадали


def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы
        узнать, как быстро игра угадывает число'''

    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED
    random_array = np.random.randint(1, 101, size=(1000))

    for number in random_array:
        count_ls.append(game_core(number))

    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")

    return(score)


# запускаем
score_game(game_core_v2)
score_game(game_core_v3)
score_game(game_core_v4)
score_game(game_core_v5)
score_game(game_core_v6)
score_game(game_core_v7)