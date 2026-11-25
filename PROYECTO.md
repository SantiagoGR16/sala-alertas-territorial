# Sala de Alertas Territorial

MVP que cruza las alertas del fenómeno de El Niño con el seguimiento de las metas
del plan de desarrollo de un municipio colombiano pequeño. El objetivo es anticipar
qué metas están en riesgo y generar un memo ejecutivo con recomendaciones.

> **El sistema recomienda; la decisión es del funcionario.**

---

## 1. Problema

Los municipios de categoría 5 y 6 tienen equipos de planeación muy pequeños. Cuando
llega una alerta climática (por ejemplo, El Niño), nadie cruza de forma sistemática esa
alerta con las metas del plan de desarrollo. El resultado: las metas de agua, agro,
gestión del riesgo o salud se atrasan y la reacción llega tarde.

## 2. Usuarios

| Usuario | Qué necesita |
|---|---|
| Alcalde/sa | Saber en 30 segundos qué metas peligran y qué decidir |
| Secretario/a de planeación | Detalle por meta, con cifras y fuentes verificables |
| Profesional de apoyo | Datos rastreables para preparar informes y responder al concejo |

## 3. Municipio piloto

- **El Rosal, Cundinamarca** (Sabana Occidente, Altiplano Cundiboyacense).
- **Categoría 6ª** (vigencia 2025, Decreto 083 del 8 de octubre de 2024). Fuente F02 en
  `docs/fuentes.md`. Falta confirmar la vigencia 2026.

## 4. Alcance

### Beta (viernes 27 de noviembre de 2026)
- 10 a 15 metas reales del plan de desarrollo municipal 2024-2027.
- Avances de las metas **simulados** y marcados como `SIMULADO` en todas partes.
- Alerta climática nacional (índice ONI de NOAA) y regional (boletines IDEAM).
- Semáforo de riesgo calculado por código.
- Memo ejecutivo redactado por agentes LLM, con cada cifra citada a su fuente.
- Interfaz sencilla: JSON + HTML estático (ver sección 9).

### Fuera de la beta (versión 2)
- Dashboard en Angular.
- Estaciones IDEAM locales (precipitación y temperatura).
- Más metas y datos reales de seguimiento.
- Cruce con la contratación pública (SECOP): ¿los contratos que respaldan las metas
  en riesgo avanzan o están atrasados?

### Lo que el sistema NO hace
- No toma decisiones ni asigna presupuesto.
- No reemplaza los reportes oficiales del municipio.
- No publica avances simulados como si fueran cifras oficiales.

## 5. Reglas de diseño (no negociables)

1. **Los cálculos los hace código, nunca el LLM.** Avances, semáforos y cruces son
   determinísticos y tienen pruebas automáticas.
2. **Los agentes solo reciben resúmenes cortos** para interpretar y redactar.
3. **Trazabilidad total:** cada cifra del memo apunta a una fuente registrada
   (URL, fecha de consulta y archivo). La verificación de las citas la hace código.
4. **Un único punto de llamada al LLM:** el proveedor es Claude, y todas las llamadas
   pasan por una sola función en un solo módulo. Ahí se registran los tokens, se
   calcula el costo y se aplica el tope de gasto. Si en el futuro se cambia de
   proveedor, solo se modifica ese módulo.
5. **Presupuesto de API: USD 5 en total** para el MVP, con tope de gasto en código y
   registro de tokens por llamada.
6. **Seguridad:** las API keys van solo en `.env` (incluido en `.gitignore`). Nunca
   en el código, en logs ni en commits. El repositorio será público.

## 6. Arquitectura (pipeline)

```
Fuentes públicas ──► Ingesta ──► Base de datos (con tabla de fuentes)
                                        │
                                        ▼
                         Motor de reglas (semáforo, sin LLM)
                                        │
                                        ▼
                     Resumen corto ──► Agente intérprete (LLM)
                                        │
                                        ▼
                                  Agente redactor (LLM)
                                        │
                                        ▼
                 Verificador de citas (código) ──► JSON de salida
                                        │
                                        ▼
                                Memo + Dashboard
```

**Agentes LLM: solo 2.** Uno interpreta los riesgos ya calculados y el otro redacta el
memo. Más agentes subirían el costo y la dificultad de depuración sin mejorar el
resultado.

**Pieza crítica validada por una persona:** la tabla de correspondencia
*meta ↔ amenaza climática* (sequía, incendio forestal, desabastecimiento de agua,
pérdida de cosechas). No la genera el LLM en cada ejecución.

## 7. Fuentes de datos (candidatas)

| Fuente | Uso | Estado |
|---|---|---|
| Plan de desarrollo El Rosal 2024-2027 | Metas e indicadores | Por ubicar |
| TerriData (DNP) | Contexto municipal | Por revisar |
| Índice ONI (NOAA) | Alerta El Niño nacional/global | Por revisar |
| Boletines IDEAM | Alerta regional | Por revisar |
| datos.gov.co | Datos complementarios | Por revisar |

## 8. Plan por fases

| Cuándo | Fase | Entregable |
|---|---|---|
| Mié 25 nov | 1. Cimientos y datos | Repo seguro, base de datos con metas y clima con fuentes |
| Jue 26 nov (mañana) | 2. Motor de reglas | Semáforo con pruebas automáticas |
| Jue 26 nov (tarde) | 3. Capa LLM | Módulo único de llamadas a Claude, con registro de tokens y tope de gasto |
| Vie 27 nov (mañana) | 4. Agentes y memo | Memo con citas verificadas por código |
| Vie 27 nov (tarde) | 5. Interfaz beta | JSON de salida + interfaz |
| Después | v2 | Angular y datos locales |

## 9. Decisiones tomadas

| Fecha | Decisión | Elegida | Por qué |
|---|---|---|---|
| 25 nov 2026 | Interfaz de la beta | **JSON + HTML estático** | Un solo lenguaje y llega a tiempo. El JSON es el contrato de datos que reutilizará Angular en la v2 |
| 25 nov 2026 | Base de datos | **SQLite** | Viene con Python, es un solo archivo y sus llaves foráneas garantizan que ninguna cifra quede sin fuente |
| 25 nov 2026 | Entorno de Python | **`.venv` + pip** | Ya funciona; no es semana para estrenar herramientas |
| 25 nov 2026 | Datos crudos | **Se versionan en GitHub** (`datos/crudos/`); la base SQLite no | Cualquiera puede reproducir y verificar cada cifra aunque la fuente original cambie o desaparezca |
| 25 nov 2026 | Proveedor LLM | **Solo Claude, con un único punto de llamada** | Sin trabajo extra para DeepSeek; el punto único permite controlar el presupuesto y cambiar de proveedor tocando un solo archivo |

Alternativas descartadas: Streamlit (no se reutiliza al pasar a Angular), Angular desde ya
(alto riesgo para el plazo), DuckDB y CSV con pandas.

## 10. Lo que NO delego a una IA

> Sección para completar por mí. Preguntas guía:
> - ¿Qué decisiones tienen consecuencias para personas reales del municipio?
> - ¿Qué parte, si sale mal, nadie la notaría a tiempo?
> - ¿Dónde necesito criterio propio para poder defender el resultado ante un alcalde?


- **No delego las reglas del semáforo** porque decidir cuándo una meta está
  "en riesgo" es un juicio de política pública: un umbral mal puesto puede
  llevar a la alcaldía a mover presupuesto hacia lo equivocado. Las reglas
  las defino y documento yo; la IA solo puede proponerme opciones. Esto
  incluye la tabla meta ↔ amenaza climática: decidir qué meta es sensible
  a la sequía o a los incendios es un juicio experto del que depende todo
  el semáforo. La IA sí puede sugerirme correspondencias para que yo las
  valide una por una.

- **No delego la verificación de las cifras ni del cruce de datos** porque
  un error al unir metas, SECOP e IDEAM se propaga en silencio y nadie lo
  notaría a tiempo. Los cálculos los hace el código, yo reviso la lógica,
  y ninguna cifra entra al memo sin su fuente y fecha de corte.

- **No delego la decisión final ni cómo se comunica** porque señalar
  rezagos de una administración tiene consecuencias para la comunidad y
  costo político. El sistema recomienda; el funcionario decide, y yo
  respondo por cómo se presenta cada alerta. La IA sí puede proponerme
  redacciones alternativas del memo y señalar frases ambiguas.

- **No delego la seguridad de las API keys ni qué datos salen hacia el
  modelo** porque una filtración no se puede deshacer. Las claves viven
  solo en el .env y la IA no lo lee ni lo muestra. La IA sí puede revisar
  el código y los commits para detectar secretos expuestos por error.

## 11. Riesgos conocidos

- Los datos reales de seguimiento de metas no son públicos: se usan avances simulados.
- El plazo de la beta es corto: se prioriza el motor y la trazabilidad sobre la estética.
- La relación entre El Niño y cada meta es un juicio experto y debe revisarlo una persona.
