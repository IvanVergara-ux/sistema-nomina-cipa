"""
Implementaciones concretas de los tipos de empleados.
Cada clase extiende Empleado y aplica sus propias reglas de negocio.
"""

from .empleado import (
    Empleado,
    BONO_ALIMENTACION,
    BONO_ANTIGUEDAD_PCTG,
    BONO_VENTAS_PCTG,
    FACTOR_HORA_EXTRA,
    HORAS_NORMALES_SEMANA,
    PORCENTAJE_FONDO_AHORRO,
    UMBRAL_VENTAS_BONO,
)


# ── 1. Empleado Asalariado ──────────────────────────────────────────────────
class EmpleadoAsalariado(Empleado):
    """
    Salario fijo mensual.
    Bono del 10 % si lleva más de 5 años en la empresa.
    Recibe bono de alimentación ($1.000.000) por ser permanente.
    """

    ANIOS_PARA_BONO = 5

    def __init__(self, nombre: str, id_empleado: str, salario_mensual: float,
                 anios_empresa: int = 0):
        super().__init__(nombre, id_empleado, anios_empresa)
        if salario_mensual <= 0:
            raise ValueError("El salario mensual debe ser mayor a cero.")
        self._salario_mensual = salario_mensual

    @property
    def tipo(self) -> str:
        return "Asalariado"

    def calcular_salario_bruto(self) -> float:
        return self._salario_mensual

    def calcular_bonos(self) -> float:
        """Bono del 10 % si tiene más de 5 años en la empresa."""
        if self._anios_empresa > self.ANIOS_PARA_BONO:
            return round(self._salario_mensual * BONO_ANTIGUEDAD_PCTG, 2)
        return 0.0

    def calcular_beneficios(self) -> float:
        """Bono de alimentación cubierto por la empresa (no descuenta del neto)."""
        return BONO_ALIMENTACION

    def calcular_fondo_ahorro(self) -> float:
        return 0.0


# ── 2. Empleado por Horas ───────────────────────────────────────────────────
class EmpleadoPorHoras(Empleado):
    """
    Pago por horas trabajadas.
    Horas extras (> 40 h) se pagan a 1.5x la tarifa normal.
    Con más de 1 año, puede acceder al fondo de ahorro (2 %).
    """

    ANIOS_PARA_FONDO = 1

    def __init__(self, nombre: str, id_empleado: str, tarifa_hora: float,
                 horas_trabajadas: float, anios_empresa: int = 0,
                 acepta_fondo_ahorro: bool = False):
        super().__init__(nombre, id_empleado, anios_empresa)
        if tarifa_hora <= 0:
            raise ValueError("La tarifa por hora debe ser mayor a cero.")
        if horas_trabajadas < 0:
            raise ValueError("Las horas trabajadas no pueden ser negativas.")

        self._tarifa_hora = tarifa_hora
        self._horas_trabajadas = horas_trabajadas
        self._acepta_fondo_ahorro = acepta_fondo_ahorro

    @property
    def tipo(self) -> str:
        return "Por Horas"

    def calcular_salario_bruto(self) -> float:
        """Calcula pago con horas normales + extras si aplica."""
        horas_normales = min(self._horas_trabajadas, HORAS_NORMALES_SEMANA)
        horas_extras = max(0.0, self._horas_trabajadas - HORAS_NORMALES_SEMANA)

        pago_normal = horas_normales * self._tarifa_hora
        pago_extras = horas_extras * self._tarifa_hora * FACTOR_HORA_EXTRA

        return round(pago_normal + pago_extras, 2)

    def calcular_bonos(self) -> float:
        """Los empleados por horas no reciben bonos."""
        return 0.0

    def calcular_beneficios(self) -> float:
        return 0.0

    def calcular_fondo_ahorro(self) -> float:
        """
        Si tiene más de 1 año y aceptó el fondo, se descuenta el 2 %
        del salario bruto mensualmente.
        """
        if self._anios_empresa > self.ANIOS_PARA_FONDO and self._acepta_fondo_ahorro:
            return round(self.calcular_salario_bruto() * PORCENTAJE_FONDO_AHORRO, 2)
        return 0.0


# ── 3. Empleado por Comisión ────────────────────────────────────────────────
class EmpleadoPorComision(Empleado):
    """
    Salario base + porcentaje de comisión sobre ventas.
    Bono adicional del 3 % si las ventas superan $20.000.000.
    Recibe bono de alimentación por ser empleado permanente.
    """

    def __init__(self, nombre: str, id_empleado: str, salario_base: float,
                 porcentaje_comision: float, total_ventas: float,
                 anios_empresa: int = 0):
        super().__init__(nombre, id_empleado, anios_empresa)
        if salario_base < 0:
            raise ValueError("El salario base no puede ser negativo.")
        if not (0 < porcentaje_comision <= 1):
            raise ValueError("El porcentaje de comisión debe estar entre 0 y 1.")
        if total_ventas < 0:
            raise ValueError("Las ventas no pueden ser menores a $0.")

        self._salario_base = salario_base
        self._porcentaje_comision = porcentaje_comision
        self._total_ventas = total_ventas

    @property
    def tipo(self) -> str:
        return "Por Comisión"

    def calcular_salario_bruto(self) -> float:
        """Salario base + comisión sobre ventas."""
        comision = self._total_ventas * self._porcentaje_comision
        return round(self._salario_base + comision, 2)

    def calcular_bonos(self) -> float:
        """Bono del 3 % sobre ventas si superan $20.000.000."""
        if self._total_ventas > UMBRAL_VENTAS_BONO:
            return round(self._total_ventas * BONO_VENTAS_PCTG, 2)
        return 0.0

    def calcular_beneficios(self) -> float:
        """Bono de alimentación cubierto por la empresa."""
        return BONO_ALIMENTACION

    def calcular_fondo_ahorro(self) -> float:
        return 0.0


# ── 4. Empleado Temporal ────────────────────────────────────────────────────
class EmpleadoTemporal(Empleado):
    """
    Salario fijo mensual con contrato de duración definida.
    No aplican bonos ni beneficios adicionales.
    """

    def __init__(self, nombre: str, id_empleado: str, salario_mensual: float,
                 meses_contrato: int, anios_empresa: int = 0):
        super().__init__(nombre, id_empleado, anios_empresa)
        if salario_mensual <= 0:
            raise ValueError("El salario mensual debe ser mayor a cero.")
        if meses_contrato <= 0:
            raise ValueError("La duración del contrato debe ser al menos 1 mes.")

        self._salario_mensual = salario_mensual
        self._meses_contrato = meses_contrato

    @property
    def tipo(self) -> str:
        return "Temporal"

    @property
    def meses_contrato(self) -> int:
        return self._meses_contrato

    def calcular_salario_bruto(self) -> float:
        return self._salario_mensual

    def calcular_bonos(self) -> float:
        return 0.0

    def calcular_beneficios(self) -> float:
        return 0.0

    def calcular_fondo_ahorro(self) -> float:
        return 0.0
