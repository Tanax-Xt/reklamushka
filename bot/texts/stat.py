where_get_grafana = """С визуализированной статистикой вы можете ознакомиться в сервисе Grafana http://0.0.0.0:3000"""

to_stat = """Пришлите мне ID {model}, чтобы получить статистику"""

to_stat_daily = """Пришлите мне ID {model}, чтобы получить статистику по дням"""

successful_get_stat = """Статистика по {name} получена:
ID {name}: `{id}`

`impressions_count`: {impressions_count},
`clicks_count`: {clicks_count},
`conversion`: {conversion},
`spent_impressions`: {spent_impressions},
`spent_clicks`: {spent_clicks},
`spent_total`: {spent_total}"""


def generate_daily_stat_text(name: str, id: str, response: list):
    out_text = [f"Ежедневная статистика по {name} получена:", f"ID {name}: `{id}`"]

    for data in response:
        out_text.extend(
            [
                f"\n------ Дата: `{data['date']}` ------",
                f"`impressions_count`: {data['impressions_count']}",
                f"`clicks_count`: {data['clicks_count']}",
                f"`conversion`: {data['conversion']}",
                f"`spent_impressions`: {data['spent_impressions']}",
                f"`spent_clicks`: {data['spent_clicks']}",
                f"`spent_total`: {data['spent_total']}",
            ]
        )

    return "\n".join(out_text)
