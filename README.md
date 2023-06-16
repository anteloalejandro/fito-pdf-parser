# Parser para PDFs de productos fitosanitarios.

Script hecho en python que extrae información de las tablas usando `py-pdf-parser`. Por el momento, `main.py` solo permite comprobar la diferencia entre los PDFs de dos directorios e imprimirlas o exportarlas en formato JSON.

# Dependencias

Para que funcione el script se han de instalar las siguientes dependencias.

```bash
pip install rich
pip install py-pdf-parser[dev]
```

# Método de uso

`main.py` sirve para comprobar las diferencias entre los PDF de dos directorios diferentes. Por defecto el script busca los directorios `new/` y `old/`, que deberán crearse y llenarse de PDFs.

Este código está pensado para comprobar cuando una versión nueva de los PDFs ha actualizado la información de su tabla, para lo que es necesario que ambos directorios tengan PDFs con el mismo nombre.

## Mostrar diferencias

```bash
python3 main.py
```

## Mostrar diferencias y exportar el resultado

**Sintaxis normal**

```bash
python3 main.py --out diffs.json
```

**Sintaxis acortada**

```bash
python3 main.py -o diffs.json
```

## Exportar sin mostrar nada por pantalla

**Sintaxis normal**

```bash
python main.py --silent --out diffs.json
```

**Sintaxis acortada**

```bash
python main.py -s -o diffs.json
```

## Cambiar directorios

```bash
python3 main.py --old v1 --new v2
```

## Resultado

Ambas acciones responden con un JSON con el siguiente resultado:

 ```json
[
    {
        "docname": "./new/bad.pdf",
        "changes": [
            {
                "msg": "El texto no coincide",
                "diff": {
                    "to": "Frutos cítricos; Penicilium, Penicillium spp.; 0,5 - 0,6 %",
                    "from": "Frutos cítricos; PUDRICIÓN; 0,5 - 0,6 %"
                }
            }
        ]
    }
]
 ```

# TO-DO

- [x] Opción para no imprimir el resultado
- [ ] Agrupar por fichero
- [ ] Separar diferencias por columna
- [ ] Mejorar rendimiento
- [ ] Añadir opción para exportar los PDFs en CSV
