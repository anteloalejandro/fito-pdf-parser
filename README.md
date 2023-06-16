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

```bash
python3 main.py --out diffs.json
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
        "msg": "La cantidad de elementos no coincide",
        "diff": null
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "CebadaMonocotiledóneas anuales1,5 - 3 l/ha1200 - 400  l/haAplicar antes de la siembra (pre-emergencia).",
            "from": "BerenjenaMildiu de la patata y el \ntomate, Phytophthora \ninfestans0,2 - 0,3 l/ha37200-1500 l/ha (Ver cond.)"
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "Dicotiledóneas anuales",
            "from": "CalabacínMildiu de las cucurbitáceas, \nPseudoperonospora \ncubensis0,2 - 0,25 l/ha37200-1250 l/ha (Ver cond.)"
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "CítricosMonocotiledóneas anuales1,5 - 4,7 l/ha1200 - 600  l/haAplicar solo en la línea del cultivo.\nSe deben tener en cuenta las medidas de aplicación para evitar todo posible contacto de los frutos con \nel producto o con el suelo tratado.\nNo labrar el suelo tras la aplicación.\nAplicar de septiembre-noviembre hasta BBCH 85.",
            "from": "CebollaMildiu de la cebolla, \nPeronospora destructor0,2 l/ha37200-1000 l/ha"
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "Dicotiledóneas anuales",
            "from": "LechugaMildiu de la lechuga, Bremia \nlactucae0,15 l/ha2 ver cond.7200-1000 l/ha"
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "Frutales de huesoMonocotiledóneas anuales1,5 - 4,7 l/ha1200 - 600  l/haAplicar solo en la línea del cultivo.\nAsegurarse de que no hay frutos maduros en el suelo o en las plantas tratadas.\nNo labrar el suelo tras la aplicación.\nAplicar de febrero-abril hasta BBCH 69. \nAplicar solo en la línea del cultivo.\nAsegurarse de que no hay frutos maduros en el suelo o en las plantas tratadas.\nNo labrar el suelo tras la aplicación.\nAplicar de febrero-abril hasta BBCH 69.",
            "from": "MelónMildiu de las cucurbitáceas, \nPseudoperonospora \ncubensis0,2 - 0,25 l/ha37200-1250 l/ha (Ver cond.)"
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "Dicotiledóneas anuales",
            "from": "PatataMildiu de la patata y el \ntomate, Phytophthora \ninfestans\nMildiu de las cucurbitáceas, \nPseudoperonospora \ncubensis0,15 l/ha47300-1000 l/haAplicar al aire libre a un BBCH 10 hasta el plazo de seguridad. Aplicar una dosis fija (15 g sa/ha, \nindependientemente del volumen de caldo a utilizar)."
        }
    },
    {
        "docname": "./new/bad.pdf",
        "msg": "El texto no coincide",
        "diff": {
            "to": "Frutales de pepitaMonocotiledóneas anuales1,5 - 4,7 l/ha1200 - 600  l/ha",
            "from": "TomateMildiu de la patata y el \ntomate, Phytophthora \ninfestans0,2 - 0,3 l/ha37200-1500 l/ha (Ver cond.)"
        }
    }
]

 ```
