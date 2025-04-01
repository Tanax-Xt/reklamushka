from src.api.statistics.schemas import DailyStatsSchema, StatsSchema


def join_daily_statistic(
    daily_statistics_impressions: list, daily_statistics_clicks: list
) -> list[tuple[int, int, int, float, float]]:
    daily_statistics = {}

    for date, impressions_count, spent_impressions in daily_statistics_impressions:
        if date is not None:
            daily_statistics[date] = {
                "impressions_count": impressions_count,
                "spent_impressions": spent_impressions,
                "clicks_count": 0,
                "spent_clicks": 0,
            }

    for date, clicks_count, spent_clicks in daily_statistics_clicks:
        if date is not None:
            if date in daily_statistics:
                daily_statistics[date]["clicks_count"] = clicks_count
                daily_statistics[date]["spent_clicks"] = spent_clicks
            else:
                daily_statistics[date] = {
                    "impressions_count": 0,
                    "spent_impressions": 0,
                    "clicks_count": clicks_count,
                    "spent_clicks": spent_clicks,
                }

    result = [
        (date, stats["impressions_count"], stats["clicks_count"], stats["spent_impressions"], stats["spent_clicks"])
        for date, stats in sorted(daily_statistics.items())
    ]

    return result


def metrics_to_schema(
    impressions_count: int, clicks_count: int, spent_impressions: float, spent_clicks: float
) -> StatsSchema:
    conversion = (clicks_count / impressions_count * 100) if impressions_count > 0 else 0.0
    spent_total = spent_impressions + spent_clicks
    return StatsSchema(
        impressions_count=impressions_count,
        clicks_count=clicks_count,
        conversion=conversion,
        spent_impressions=spent_impressions,
        spent_clicks=spent_clicks,
        spent_total=spent_total,
    )


def daily_metrics_to_schema(metrics: list[tuple[int, int, int, float, float]]) -> list[DailyStatsSchema]:
    return [
        DailyStatsSchema(
            date=metric[0],
            impressions_count=metric[1],
            clicks_count=metric[2],
            conversion=(metric[2] / metric[1] * 100) if metric[1] > 0 else 0.0,
            spent_impressions=metric[3],
            spent_clicks=metric[4],
            spent_total=metric[3] + metric[4],
        )
        for metric in metrics
    ]
