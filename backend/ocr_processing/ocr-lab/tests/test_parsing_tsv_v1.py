from ocr_app.parsing import TicketParser, parsear_a_productos_json, parsear_a_tsv


def test_no_descartar_lineas_cortas_validas() -> None:
    ticket_parser = TicketParser()
    lineas_ocr = [
        "MERCADONA",
        "MANZANA",
        "kg",
        "2,15",
        "TOTAL",
        "2,15",
    ]

    productos_extraidos = ticket_parser.extraer_productos(lineas_ocr)

    assert productos_extraidos
    assert productos_extraidos[0].nombre == "MANZANA KG"
    assert productos_extraidos[0].precio_total == 2.15


def test_total_con_total_eur_y_lineas_iva() -> None:
    ticket_parser = TicketParser()
    lineas_ocr = [
        "MERCADONA",
        "IVA 10% 10,00 1,00",
        "TOTAL IVA 1,00",
        "TOTAL (€)",
        "11,00",
    ]

    total_extraido = ticket_parser.extraer_total_por_contexto(lineas_ocr)

    assert total_extraido == 11.00


def test_extraer_producto_nombre_y_precio_en_lineas_separadas() -> None:
    ticket_parser = TicketParser()
    lineas_ocr = [
        "MERCADONA",
        "LECHE ENTERA",
        "1,35",
        "TOTAL",
        "1,35",
    ]

    productos_extraidos = ticket_parser.extraer_productos(lineas_ocr)

    assert len(productos_extraidos) == 1
    assert productos_extraidos[0].nombre == "LECHE ENTERA"
    assert productos_extraidos[0].precio_total == 1.35


def test_genera_tsv_v1_formato_exacto() -> None:
    texto_ocr = "\n".join(
        [
            "MERCADONA",
            "FECHA 13/02/2026 10:22",
            "PAN",
            "0,80",
            "TOTAL",
            "0,80",
        ]
    )

    tsv_generado = parsear_a_tsv(texto_ocr)

    tsv_esperado = "\n".join(
        [
            "VER\t1",
            "H\tMERCADONA\t\t\t\t\t2026-02-13T10:22\t\t\tEUR",
            "L\tPAN\t\t\t0.80\t",
            "T\t0.80",
        ]
    )

    assert tsv_generado == tsv_esperado


def test_total_se_ajusta_con_iva_para_cliente_final() -> None:
    ticket_parser = TicketParser()
    lineas_ocr = [
        "MERCADONA",
        "IVA 10% 1,95 0,20",
        "TOTAL",
        "1,95",
    ]

    datos_parseados = ticket_parser.parsear(lineas_ocr)

    assert datos_parseados["total"] == 2.15


def test_json_productos_solo_name_price_y_sin_envio_iva() -> None:
    texto_ocr = "\n".join(
        [
            "MERCADONA",
            "MANZANA",
            "2,15",
            "ENVIO",
            "3,99",
            "IVA 10% 2,15 0,22",
            "TOTAL",
            "2,37",
        ]
    )

    json_generado = parsear_a_productos_json(texto_ocr)

    assert json_generado == '[{"name":"MANZANA","price":2.15}]'
