"""
Punto de entrada principal del sistema de nómina.
Demuestra el uso del sistema con empleados de ejemplo.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from models import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoPorComision,
    EmpleadoTemporal,
)
from services import ServicioNomina


def main():
    servicio = ServicioNomina()

    # ── Empleados de ejemplo ─────────────────────────────────────────────────
    servicio.agregar_empleado(
        EmpleadoAsalariado("Ana Torres", "E001", salario_mensual=3_500_000, anios_empresa=6)
    )
    servicio.agregar_empleado(
        EmpleadoPorHoras("Pedro Ríos", "E002", tarifa_hora=55_000,
                         horas_trabajadas=48, anios_empresa=2, acepta_fondo_ahorro=True)
    )
    servicio.agregar_empleado(
        EmpleadoPorComision("Laura Mora", "E003", salario_base=2_000_000,
                            porcentaje_comision=0.05, total_ventas=22_000_000)
    )
    servicio.agregar_empleado(
        EmpleadoTemporal("Rosa Lima", "E004", salario_mensual=2_200_000, meses_contrato=6)
    )

    print(servicio.reporte_texto())


if __name__ == "__main__":
    main()
