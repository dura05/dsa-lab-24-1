from triangle_func import IncorrectTriangleSides

class Triangle:
    def __init__(self, a: float, b: float, c: float):
        """
        Инициализирует треугольник с заданными сторонами.
        
        Args:
            a: Длина первой стороны
            b: Длина второй стороны
            c: Длина третьей стороны
            
        Raises:
            IncorrectTriangleSides: Если стороны не образуют треугольник
        """
        if a <= 0 or b <= 0 or c <= 0:
            raise IncorrectTriangleSides("Стороны должны быть положительными")
        if a + b <= c or a + c <= b or b + c <= a:
            raise IncorrectTriangleSides("Не выполняется неравенство треугольника")
        
        self.a = a
        self.b = b
        self.c = c
    
    def triangle_type(self) -> str:
        """
        Возвращает тип треугольника.
        
        Returns:
            "equilateral", "isosceles" или "nonequilateral"
        """
        if self.a == self.b == self.c:
            return "equilateral"
        elif self.a == self.b or self.a == self.c or self.b == self.c:
            return "isosceles"
        else:
            return "nonequilateral"
    
    def perimeter(self) -> float:
        """
        Вычисляет периметр треугольника.
        
        Returns:
            Сумма длин сторон треугольника
        """
        return self.a + self.b + self.c