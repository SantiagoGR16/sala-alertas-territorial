# Inventario de fuentes

Cada cifra del sistema debe apuntar a una fila de esta tabla.
Los archivos descargados se guardan en `datos/crudos/` sin modificarlos.

| ID | Fuente | Entidad | URL | Formato | Fecha de consulta | Archivo en `datos/crudos/` | Uso en el proyecto |
|---|---|---|---|---|---|---|---|
| F01 | Plan Municipal de Desarrollo "El Rosal Necesita el Cambio" (Acuerdo 003 del 31 de mayo de 2024) | Concejo Municipal de El Rosal | https://mapas.cundinamarca.gov.co/documents/3336682c835b49d4bb200dd8872c593c | PDF escaneado (81 páginas) | 2026-11-25 | `pdm_el_rosal_2024_2027.pdf` | Metas de producto (`datos/manuales/metas_seleccionadas.csv`) |
| F02 | Categorización de municipios, vigencia 2025 | Gobernación de Cundinamarca | https://www.cundinamarca.gov.co/wcm/connect/dd0c54ed-c7c8-443d-9292-fac80901a6f5/Categorizaci%C3%B3n+2025.pdf | PDF | 2026-11-25 | (no descargado) | Confirma que El Rosal es categoría 6ª (Decreto 083 del 8 de octubre de 2024) |

## Observaciones sobre las fuentes

- **F01:** el documento dice "2024-2028" en la portada y "Meta 2028" en las tablas, aunque
  el periodo de gobierno es 2024-2027. Se registra tal como aparece en la fuente; el valor
  se trata como meta del cuatrienio.
- **F01:** el PDF es un escaneo sin texto. Las metas se transcribieron a mano en
  `datos/manuales/metas_seleccionadas.csv`, indicando la página del PDF de cada una.
- **F02:** falta confirmar la categoría para la vigencia 2026.

## Archivos de `datos/manuales/`

| Archivo | Qué contiene | Naturaleza |
|---|---|---|
| `metas_seleccionadas.csv` | 15 metas transcritas del plan (F01) | **Hecho:** lo que dice la fuente |
| `exposicion_climatica.csv` | Amenaza y tipo de relación de cada meta con El Niño | **Juicio experto** validado por el equipo del proyecto |

Tipos de relación:
- `ejecucion`: El Niño dificulta cumplir la meta.
- `urgencia`: El Niño vuelve más urgente cumplir la meta.
