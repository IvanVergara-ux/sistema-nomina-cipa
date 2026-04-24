"""
Pruebas unitarias del sistema de nómina.
Cobertura:
  - EmpleadoAsalariado
  - EmpleadoPorHoras
  - EmpleadoPorComision
  - EmpleadoTemporal
  - ServicioNomina
  - Validaciones y casos borde
"""

import sys
import os
import unittest

# Permite importar los módulos desde la raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoPorComision,
    EmpleadoTemporal,
)
from services import ServicioNomina


# ══════════════════════════════════════════════════════════════════════════════
# Empleado Asalariado
# ══════════════════════════════════════════════════════════════════════════════
class TestEmpleadoAsalariado(unittest.TestCase):

    def setUp(self):
        self.empleado = EmpleadoAsalariado(
            nombre="Ana Torres",
            id_empleado="E001",
            salario_mensual=3_000_000,
            anios_empresa=3,
        )
        self.empleado_senior = EmpleadoAsalariado(
            nombre="Luis Gómez",
            id_empleado="E002",
            salario_mensual=5_000_000,
            anios_empresa=7,
        )

    def test_tipo_correcto(self):
        self.assertEqual(self.empleado.tipo, "Asalariado")

    def test_salario_bruto(self):
        self.assertEqual(self.empleado.calcular_salario_bruto(), 3_000_000)

    def test_sin_bono_menos_de_5_anios(self):
        self.assertEqual(self.empleado.calcular_bonos(), 0.0)

    def test_bono_10_pct_mas_de_5_anios(self):
        bono = self.empleado_senior.calcular_bonos()
        self.assertAlmostEqual(bono, 5_000_000 * 0.10)

    def test_beneficio_alimentacion(self):
        self.assertEqual(self.empleado.calcular_beneficios(), 1_000_000)

    def test_deduccion_4_pct(self):
        self.assertAlmostEqual(self.empleado.calcular_deducciones(), 3_000_000 * 0.04)

    def test_salario_neto_sin_bono(self):
        nomina = self.empleado.calcular_nomina()
        esperado = 3_000_000 - (3_000_000 * 0.04)
        self.assertAlmostEqual(nomina.salario_neto, esperado)

    def test_salario_neto_con_bono(self):
        nomina = self.empleado_senior.calcular_nomina()
        bruto = 5_000_000
        bono = bruto * 0.10
        deduccion = bruto * 0.04
        esperado = bruto + bono - deduccion
        self.assertAlmostEqual(nomina.salario_neto, esperado)

    def test_error_salario_cero(self):
        with self.assertRaises(ValueError):
            EmpleadoAsalariado("X", "E999", 0)

    def test_error_nombre_vacio(self):
        with self.assertRaises(ValueError):
            EmpleadoAsalariado("   ", "E999", 1_000_000)


# ══════════════════════════════════════════════════════════════════════════════
# Empleado por Horas
# ══════════════════════════════════════════════════════════════════════════════
class TestEmpleadoPorHoras(unittest.TestCase):

    def setUp(self):
        self.empleado_normal = EmpleadoPorHoras(
            nombre="Pedro Ríos",
            id_empleado="E003",
            tarifa_hora=50_000,
            horas_trabajadas=40,
        )
        self.empleado_horas_extras = EmpleadoPorHoras(
            nombre="Sara Pérez",
            id_empleado="E004",
            tarifa_hora=50_000,
            horas_trabajadas=50,
        )
        self.empleado_con_fondo = EmpleadoPorHoras(
            nombre="Marco Silva",
            id_empleado="E005",
            tarifa_hora=60_000,
            horas_trabajadas=45,
            anios_empresa=2,
            acepta_fondo_ahorro=True,
        )

    def test_tipo_correcto(self):
        self.assertEqual(self.empleado_normal.tipo, "Por Horas")

    def test_salario_sin_extras(self):
        self.assertEqual(self.empleado_normal.calcular_salario_bruto(), 40 * 50_000)

    def test_salario_con_extras(self):
        # 40h normales + 10h extras a 1.5x
        esperado = (40 * 50_000) + (10 * 50_000 * 1.5)
        self.assertAlmostEqual(self.empleado_horas_extras.calcular_salario_bruto(), esperado)

    def test_sin_bonos(self):
        self.assertEqual(self.empleado_horas_extras.calcular_bonos(), 0.0)

    def test_fondo_ahorro_aplica(self):
        bruto = self.empleado_con_fondo.calcular_salario_bruto()
        fondo = self.empleado_con_fondo.calcular_fondo_ahorro()
        self.assertAlmostEqual(fondo, bruto * 0.02)

    def test_fondo_ahorro_no_aplica_sin_anios(self):
        e = EmpleadoPorHoras("X", "E006", 50_000, 40, anios_empresa=0, acepta_fondo_ahorro=True)
        self.assertEqual(e.calcular_fondo_ahorro(), 0.0)

    def test_fondo_ahorro_no_aplica_sin_aceptar(self):
        e = EmpleadoPorHoras("X", "E007", 50_000, 40, anios_empresa=2, acepta_fondo_ahorro=False)
        self.assertEqual(e.calcular_fondo_ahorro(), 0.0)

    def test_error_horas_negativas(self):
        with self.assertRaises(ValueError):
            EmpleadoPorHoras("X", "E008", 50_000, -5)

    def test_error_tarifa_cero(self):
        with self.assertRaises(ValueError):
            EmpleadoPorHoras("X", "E009", 0, 40)


# ══════════════════════════════════════════════════════════════════════════════
# Empleado por Comisión
# ══════════════════════════════════════════════════════════════════════════════
class TestEmpleadoPorComision(unittest.TestCase):

    def setUp(self):
        self.empleado_bajo = EmpleadoPorComision(
            nombre="Laura Mora",
            id_empleado="E010",
            salario_base=2_000_000,
            porcentaje_comision=0.05,
            total_ventas=10_000_000,
        )
        self.empleado_alto = EmpleadoPorComision(
            nombre="Carlos Vega",
            id_empleado="E011",
            salario_base=2_000_000,
            porcentaje_comision=0.05,
            total_ventas=25_000_000,
        )

    def test_tipo_correcto(self):
        self.assertEqual(self.empleado_bajo.tipo, "Por Comisión")

    def test_salario_bruto_con_comision(self):
        esperado = 2_000_000 + (10_000_000 * 0.05)
        self.assertAlmostEqual(self.empleado_bajo.calcular_salario_bruto(), esperado)

    def test_sin_bono_ventas_bajas(self):
        self.assertEqual(self.empleado_bajo.calcular_bonos(), 0.0)

    def test_bono_ventas_altas(self):
        bono = self.empleado_alto.calcular_bonos()
        self.assertAlmostEqual(bono, 25_000_000 * 0.03)

    def test_beneficio_alimentacion(self):
        self.assertEqual(self.empleado_alto.calcular_beneficios(), 1_000_000)

    def test_error_ventas_negativas(self):
        with self.assertRaises(ValueError):
            EmpleadoPorComision("X", "E012", 2_000_000, 0.05, -1)

    def test_error_comision_cero(self):
        with self.assertRaises(ValueError):
            EmpleadoPorComision("X", "E013", 2_000_000, 0, 5_000_000)


# ══════════════════════════════════════════════════════════════════════════════
# Empleado Temporal
# ══════════════════════════════════════════════════════════════════════════════
class TestEmpleadoTemporal(unittest.TestCase):

    def setUp(self):
        self.empleado = EmpleadoTemporal(
            nombre="Rosa Lima",
            id_empleado="E014",
            salario_mensual=2_500_000,
            meses_contrato=6,
        )

    def test_tipo_correcto(self):
        self.assertEqual(self.empleado.tipo, "Temporal")

    def test_salario_bruto(self):
        self.assertEqual(self.empleado.calcular_salario_bruto(), 2_500_000)

    def test_sin_bonos(self):
        self.assertEqual(self.empleado.calcular_bonos(), 0.0)

    def test_sin_beneficios(self):
        self.assertEqual(self.empleado.calcular_beneficios(), 0.0)

    def test_sin_fondo(self):
        self.assertEqual(self.empleado.calcular_fondo_ahorro(), 0.0)

    def test_deduccion_4_pct(self):
        self.assertAlmostEqual(self.empleado.calcular_deducciones(), 2_500_000 * 0.04)

    def test_error_meses_cero(self):
        with self.assertRaises(ValueError):
            EmpleadoTemporal("X", "E015", 2_000_000, 0)


# ══════════════════════════════════════════════════════════════════════════════
# Servicio de Nómina
# ══════════════════════════════════════════════════════════════════════════════
class TestServicioNomina(unittest.TestCase):

    def setUp(self):
        self.servicio = ServicioNomina()
        self.emp1 = EmpleadoAsalariado("Ana", "E001", 3_000_000, 3)
        self.emp2 = EmpleadoTemporal("Rosa", "E002", 2_000_000, 4)

    def test_agregar_empleado(self):
        self.servicio.agregar_empleado(self.emp1)
        resultados = self.servicio.procesar_nomina()
        self.assertEqual(len(resultados), 1)

    def test_procesar_dos_empleados(self):
        self.servicio.agregar_empleado(self.emp1)
        self.servicio.agregar_empleado(self.emp2)
        resultados = self.servicio.procesar_nomina()
        self.assertEqual(len(resultados), 2)

    def test_total_nomina(self):
        self.servicio.agregar_empleado(self.emp1)
        self.servicio.agregar_empleado(self.emp2)
        total = self.servicio.total_nomina()
        self.assertGreater(total, 0)

    def test_remover_empleado(self):
        self.servicio.agregar_empleado(self.emp1)
        removido = self.servicio.remover_empleado("E001")
        self.assertTrue(removido)
        self.assertEqual(len(self.servicio.procesar_nomina()), 0)

    def test_remover_empleado_inexistente(self):
        removido = self.servicio.remover_empleado("XXXX")
        self.assertFalse(removido)

    def test_reporte_vacio(self):
        reporte = self.servicio.reporte_texto()
        self.assertIn("No hay empleados", reporte)

    def test_reporte_con_empleados(self):
        self.servicio.agregar_empleado(self.emp1)
        reporte = self.servicio.reporte_texto()
        self.assertIn("Ana", reporte)
        self.assertIn("SALARIO NETO", reporte)

    def test_error_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self.servicio.agregar_empleado("no soy un empleado")


# ══════════════════════════════════════════════════════════════════════════════
# Punto de entrada
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)
