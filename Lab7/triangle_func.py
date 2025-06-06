class IncorrectTriangleSides(Exception):
    pass

def get_triangle_type(a: float, b: float, c: float) -> str:
    """
    Определяет тип треугольника по длинам его сторон.
    
    Args:
        a: Длина первой стороны
        b: Длина второй стороны
        c: Длина третьей стороны
    
    Returns:
        Строка с типом треугольника: "equilateral", "isosceles" или "nonequilateral"
    
    Raises:
        IncorrectTriangleSides: Если стороны не образуют треугольник
    """
    # Проверка корректности сторон
    if a <= 0 or b <= 0 or c <= 0:
        raise IncorrectTriangleSides("Стороны должны быть положительными")
    if a + b <= c or a + c <= b or b + c <= a:
        raise IncorrectTriangleSides("Не выполняется неравенство треугольника")
    
    # Определение типа треугольника
    if a == b == c:
        return "equilateral"
    elif a == b or a == c or b == c:
        return "isosceles"
    else:
        return "nonequilateral"