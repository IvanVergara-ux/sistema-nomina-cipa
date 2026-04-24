"""
Servicio de nómina.
Responsabilidad única (SRP): procesar y reportar la nómina de una lista de empleados.
No conoce los detalles de cálculo de cada tipo; delega en cada instancia.
"""

from typing import List
from models.empleado import Empleado, ResultadoNomina


class ServicioNomina:
    """
    Orquesta el procesamiento de nómina para un conjunto de empleados.
    Depende de la abstracción `Empleado`, no de clases concretas (DIP).
    """

    def __init__(self):
        self._empleados: List[Empleado] = []

    # ── Gestión de empleados ────────────────────────────────────────────────
    def agregar_empleado(self, empleado: Empleado) -> None:
        """Registra un empleado en el servicio."""
        if not isinstance(empleado, Empleado):
            raise TypeError("Solo se pueden agregar instancias de Empleado.")
        self._empleados.append(empleado)

    def remover_empleado(self, id_empleado: str) -> bool:
        """Elimina un empleado por su ID. Retorna True si fue encontrado."""
        antes = len(self._empleados)
        self._empleados = [e for e in self._empleados if e.id_empleado != id_empleado]
        return len(self._empleados) < antes

    # ── Procesamiento ───────────────────────────────────────────────────────
    def procesar_nomina(self) -> List[ResultadoNomina]:
        """
        Calcula la nómina de todos los empleados registrados.
        Los errores de un empleado se capturan y se reportan sin detener el proceso.
        """
        resultados = []
        for empleado in self._empleados:
            try:
                resultado = empleado.calcular_nomina()
                resultados.append(resultado)
            except ValueError as exc:
                print(f"[ERROR] Empleado '{empleado.nombre}': {exc}")
        return resultados

    # ── Reportes ────────────────────────────────────────────────────────────
    def total_nomina(self) -> float:
        """Suma de todos los salarios netos del período."""
        return round(
            sum(r.salario_neto for r in self.procesar_nomina()), 2
        )

    def reporte_texto(self) -> str:
        """Genera un reporte de texto con el detalle por empleado."""
        resultados = self.procesar_nomina()
        if not resultados:
            return "No hay empleados registrados en la nómina."

        lineas = ["=" * 60, "           REPORTE DE NÓMINA", "=" * 60]
        for r in resultados:
            lineas.append(f"\nEmpleado : {r.nombre}  ({r.tipo})")
            lineas.append(f"  Salario bruto   : ${r.salario_bruto:>15,.0f}")
            lineas.append(f"  Bonos           : ${r.bonos:>15,.0f}")
            lineas.append(f"  Beneficios      : ${r.beneficios:>15,.0f}")
            lineas.append(f"  Deducciones     : ${r.deducciones:>15,.0f}")
            lineas.append(f"  Fondo de ahorro : ${r.fondo_ahorro:>15,.0f}")
            lineas.append(f"  {'─' * 35}")
            lineas.append(f"  SALARIO NETO    : ${r.salario_neto:>15,.0f}")

        lineas.append("\n" + "=" * 60)
        lineas.append(f"  TOTAL NÓMINA    : ${self.total_nomina():>15,.0f}")
        lineas.append("=" * 60)
        return "\n".join(lineas)
