def detectar_arbitraje(cuotas_dict, monto_total):
    suma_inv = sum(1/cuota for cuota in cuotas_dict.values())
    if suma_inv >= 1:
        return None

    apuestas = {res: round((1/cuota)/suma_inv * monto_total, 2) for res, cuota in cuotas_dict.items()}
    ganancia = round(min([apuestas[res] * cuotas_dict[res] for res in apuestas]) - monto_total, 2)
    porcentaje = round((1 - suma_inv) * 100, 2)

    return {
        "apuestas": apuestas,
        "ganancia": ganancia,
        "porcentaje_arbitraje": porcentaje
    }
