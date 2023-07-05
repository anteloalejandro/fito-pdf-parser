# Parser para PDFs de productos fitosanitarios.

Script hecho en python que extrae información de las tablas usando `py-pdf-parser`. Por el momento, `main.py` solo permite comprobar la diferencia entre los PDFs de dos directorios e imprimirlas o exportarlas en formato JSON.

# Dependencias

Todas las dependencias de los archivos de este repositorio se encuentran listadas en el archivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

# Método de uso

`main.py` sirve para comprobar las diferencias entre los PDF de dos directorios diferentes.

Este código está pensado para comprobar cuando una versión nueva de los PDFs ha actualizado la información de su tabla, para lo que es necesario que ambos directorios tengan PDFs con el mismo nombre.

## Ejecutar

Por defecto el script compara los PDFs de los directorios `new/` y `old/` y exporta todas las diferencias un archivo `diffs.json`. Además, genera los archivos de log `warnings.log`, `errors.log` y `changes.log` y les añade información precedida por la fecha actual.

```bash
python3 main.py
```

## Especificar el archivo al que se exporta

**Sintaxis normal**

```bash
python3 main.py --out my_file.json
```

**Sintaxis acortada**

```bash
python3 main.py -o my_file.json
```

## Ejecutar sin mostrar nada por pantalla

**Sintaxis normal**

```bash
python main.py --silent
```

**Sintaxis acortada**

```bash
python main.py -s
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
                    "from": "Frutos cítricos; PUDRICIÓN; 0,5 - 0,6 %"
                    "to": "Frutos cítricos; Penicilium, Penicillium spp.; 0,5 - 0,6 %",
                }
            }
        ]
    }
]
 ```

# TO-DO

- [x] Opción para no imprimir el resultado
- [x] Agrupar por fichero
- [x] Separar diferencias por columna
- [ ] Mostrar los contenidos de la tabla 'Condiciones Generales de Uso'
- [ ] Mejorar rendimiento
- [ ] Añadir opción para exportar los PDFs en CSV
