"""
Módulo base para el sistema de nómina.
Define la clase abstracta Empleado y sus contratos (interfaces).
Principio SOLID aplicado:
  - SRP: cada clase tiene una sola responsabilidad.
  - OCP: abierto para extensión, cerrado para modificación.
  - LSP: las subclases pueden reemplazar a la base sin romper el sistema.
  - ISP: interfaces pequeñas y específicas.
  - DIP: dependemos de abstracciones, no de implementaciones concretas.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# ── Constantes de negocio ───────────────────────────────────────────────────
PORCENTAJE_SEGURO_PENSION = 0.04   # 4 % del salario bruto
BONO_ALIMENTACION = 1_000_000      # $1.000.000 / mes (empleados permanentes)
PORCENTAJE_FONDO_AHORRO = 0.02     # 2 % del salario (empleados por horas > 1 año)
HORAS_NORMALES_SEMANA = 40         # Umbral para horas extras
FACTOR_HORA_EXTRA = 1.5            # Multiplicador de horas extras
BONO_ANTIGUEDAD_PCTG = 0.10        # 10 % bono para asalariados > 5 años
UMBRAL_VENTAS_BONO = 20_000_000    # $20.000.000 en ventas
BONO_VENTAS_PCTG = 0.03            # 3 % bono sobre ventas altas


# ── Value Object: resultado del cálculo de nómina ──────────────────────────
@dataclass
class ResultadoNomina:
    """Encapsula el desglose completo del pago de un empleado."""
    nombre: str
    tipo: str
    salario_bruto: float
    bonos: float
    beneficios: float
    deducciones: float
    fondo_ahorro: float
    salario_neto: float

    def resumen(self) -> dict:
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "salario_bruto": self.salario_bruto,
            "bonos": self.bonos,
            "beneficios": self.beneficios,
            "deducciones": self.deducciones,
            "fondo_ahorro": self.fondo_ahorro,
            "salario_neto": self.salario_neto,
        }


# ── Clase abstracta base ────────────────────────────────────────────────────
class Empleado(ABC):
    """
    Clase base abstracta para todos los tipos de empleados.
    Define el contrato que deben cumplir las subclases.
    """

    def __init__(self, nombre: str, id_empleado: str, anios_empresa: int = 0):
        if not nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío.")
        if anios_empresa < 0:
            raise ValueError("Los años en la empresa no pueden ser negativos.")

        self._nombre = nombre.strip()
        self._id = id_empleado
        self._anios_empresa = anios_empresa

    # ── Propiedades ─────────────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def id_empleado(self) -> str:
        return self._id

    @property
    def anios_empresa(self) -> int:
        return self._anios_empresa

    # ── Métodos abstractos (contrato) ────────────────────────────────────────
    @abstractmethod
    def calcular_salario_bruto(self) -> float:
        """Calcula el salario bruto antes de bonos y deducciones."""

    @abstractmethod
    def calcular_bonos(self) -> float:
        """Calcula el total de bonos del empleado."""

    @abstractmethod
    def calcular_beneficios(self) -> float:
        """Calcula los beneficios adicionales cubiertos por la empresa."""

    @abstractmethod
    def calcular_fondo_ahorro(self) -> float:
        """Calcula el aporte al fondo de ahorro (si aplica)."""

    @property
    @abstractmethod
    def tipo(self) -> str:
        """Retorna el tipo de empleado como cadena descriptiva."""

    # ── Comportamiento compartido ────────────────────────────────────────────
    def calcular_deducciones(self) -> float:
        """
        Deducciones obligatorias: Seguro Social + Pensión (4 % del bruto).
        ARL se asume incluida en el 4 % para simplificar el modelo;
        puede extraerse a su propio método si las tasas difieren.
        """
        return round(self.calcular_salario_bruto() * PORCENTAJE_SEGURO_PENSION, 2)

    def calcular_nomina(self) -> ResultadoNomina:
        """
        Orquesta el cálculo completo de la nómina.
        Valida que el salario neto no sea negativo.
        """
        bruto = self.calcular_salario_bruto()
        bonos = self.calcular_bonos()
        beneficios = self.calcular_beneficios()
        deducciones = self.calcular_deducciones()
        fondo = self.calcular_fondo_ahorro()

        neto = bruto + bonos - deducciones - fondo

        if neto < 0:
            raise ValueError(
                f"El salario neto de {self._nombre} resultó negativo: ${neto:,.0f}. "
                "Verifique los datos ingresados."
            )

        return ResultadoNomina(
            nombre=self._nombre,
            tipo=self.tipo,
            salario_bruto=round(bruto, 2),
            bonos=round(bonos, 2),
            beneficios=round(beneficios, 2),
            deducciones=round(deducciones, 2),
            fondo_ahorro=round(fondo, 2),
            salario_neto=round(neto, 2),
        )
