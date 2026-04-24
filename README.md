# Sistema de Nómina — Actividad Unidad 3

## Descripción
Sistema de liquidación de nómina desarrollado con **Programación Orientada a Objetos** en Python 3.12+, aplicando los principios **SOLID**, código limpio, buenas prácticas y pruebas unitarias.

---

## Metodología de Desarrollo: SCRUM simplificado

| Sprint | Entregable |
|--------|-----------|
| 1 | Análisis de reglas de negocio + diseño de clases |
| 2 | Implementación del modelo base (`Empleado`) |
| 3 | Implementación de los 4 tipos de empleados |
| 4 | `ServicioNomina` + pruebas unitarias |
| 5 | Refactorización + documentación |

---

## Estructura del Proyecto

```
nomina/
├── models/
│   ├── empleado.py          # Clase abstracta base + ResultadoNomina
│   ├── tipos_empleados.py   # 4 tipos concretos de empleados
│   └── __init__.py
├── services/
│   ├── servicio_nomina.py   # Orquestador de nómina
│   └── __init__.py
├── tests/
│   └── test_nomina.py       # 41 pruebas unitarias
├── main.py                  # Punto de entrada / demo
└── README.md
```

---

## Principios SOLID Aplicados

### S — Single Responsibility Principle
Cada clase tiene **una única responsabilidad**:
- `Empleado`: define el contrato de un empleado.
- `EmpleadoAsalariado`, etc.: implementan las reglas de su tipo específico.
- `ServicioNomina`: orquesta el procesamiento de la nómina.
- `ResultadoNomina`: encapsula el resultado del cálculo (Value Object).

### O — Open/Closed Principle
Para agregar un nuevo tipo de empleado (ej. *Freelance*), solo se crea una nueva subclase de `Empleado`. **No se modifica** ningún código existente.

### L — Liskov Substitution Principle
Cualquier subclase de `Empleado` puede pasarse a `ServicioNomina.agregar_empleado()` sin romper el sistema. Las subclases cumplen todos los contratos de la clase base.

### I — Interface Segregation Principle
La clase abstracta `Empleado` expone únicamente los métodos que todos los empleados necesitan. No se fuerza a ninguna subclase a implementar métodos irrelevantes.

### D — Dependency Inversion Principle
`ServicioNomina` depende de la abstracción `Empleado`, **no** de clases concretas como `EmpleadoAsalariado`. Esto permite extender el sistema sin modificar el servicio.

---

## Buenas Prácticas Aplicadas

- **Código limpio**: nombres descriptivos, funciones pequeñas, sin magia numérica (constantes nombradas).
- **Comentarios de código**: docstrings en todas las clases y métodos públicos.
- **Validaciones**: entradas inválidas lanzan `ValueError` con mensajes claros.
- **Encapsulamiento**: atributos privados (`_nombre`, `_salario`), acceso vía propiedades.
- **Inmutabilidad**: `ResultadoNomina` es un dataclass que actúa como Value Object.
- **Separación de capas**: `models/` (dominio) vs `services/` (lógica de aplicación).

---

## Tipos de Empleados y Reglas

| Tipo | Salario | Bonos | Beneficios | Fondo Ahorro |
|------|---------|-------|-----------|--------------|
| Asalariado | Fijo mensual | 10% si > 5 años | Alimentación $1M | No |
| Por Horas | Tarifa × horas (extras 1.5×) | Ninguno | No | 2% si > 1 año y acepta |
| Por Comisión | Base + comisión | 3% si ventas > $20M | Alimentación $1M | No |
| Temporal | Fijo mensual | Ninguno | No | No |

**Deducciones**: 4% del salario bruto (Seguro Social + Pensión + ARL).

---

## Pruebas Unitarias

```bash
cd nomina
python -m pytest tests/test_nomina.py -v
```

**41 pruebas** que cubren:
- Cálculo correcto de cada tipo de empleado.
- Bonos y beneficios según condiciones.
- Deducciones obligatorias.
- Fondo de ahorro con sus condiciones.
- Validaciones de datos inválidos.
- `ServicioNomina`: agregar, remover, procesar y reportar.

---

## Ejecución

```bash
python main.py
```

---

## Tecnologías
- Python 3.12+
- `unittest` (pruebas unitarias)
- `pytest` (runner de pruebas)
- `abc` (clases abstractas)
- `dataclasses` (Value Objects)
