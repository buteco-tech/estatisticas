import traceback

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Filter,
    FilterExpression,
    Metric,
    OrderBy,
    RunReportRequest,
)

TTL = 1 * 60 * 60


def cache(ttl=None):
    dummy = object()
    cache = {}

    def wrapper(fn):
        def inner_wrapper(*args, **kwargs):
            # TODO: include arguments in the key
            # key = fn.__qualname__ + args + kwargs
            key = fn.__qualname__

            # cache hit?
            if key in cache:
                value, time = cache[key]

                # ttl valid?
                if (time + timedelta(seconds=ttl)) < datetime.now():
                    value = dummy
            else:
                value = dummy

            if value is dummy:
                value = fn(*args, **kwargs)
                cache[key] = (value, datetime.now())

            return value

        return inner_wrapper

    return wrapper


class GoogleAnalyticsMetrics:
    def __init__(self, property_id, credentials_path):
        self.property_id = property_id
        self.client = BetaAnalyticsDataClient.from_service_account_json(credentials_path)

    def _run_report(self, **kwargs):
        try:
            request = RunReportRequest(property=f"properties/{self.property_id}", **kwargs)
            response = self.client.run_report(request)
        except Exception as e:
            traceback.print_exc()

            return {
                "dimensions": [],
                "metrics": [],
            }

        return {
            "dimensions": [row.dimension_values[0].value for row in response.rows],
            "metrics": [row.metric_values[0].value for row in response.rows],
        }

    @cache(ttl=TTL)
    def get_pageviews(self):
        now = datetime.now()
        end_date = now - timedelta(days=now.day)
        start_date = now - relativedelta(months=6, days=now.day - 1)

        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="yearMonth")],
            date_ranges=[DateRange(start_date=start_date.strftime("%Y-%m-%d"), end_date=end_date.strftime("%Y-%m-%d"))],
            order_bys=[OrderBy(dimension=OrderBy.DimensionOrderBy(dimension_name="yearMonth"), desc=False)],
        )

    @cache(ttl=TTL)
    def get_top_pages(self):
        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="pagePath")],
            date_ranges=[DateRange(start_date="90daysAgo", end_date="yesterday")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            dimension_filter=FilterExpression(
                not_expression=FilterExpression(
                    filter=Filter(
                        field_name="pagePath",
                        string_filter=Filter.StringFilter(match_type=Filter.StringFilter.MatchType.EXACT, value="/"),
                    ),
                )
            ),
            limit=15,
        )

    @cache(ttl=TTL)
    def get_acquisition(self):
        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="sessionDefaultChannelGroup")],
            date_ranges=[DateRange(start_date="90daysAgo", end_date="yesterday")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        )

    @cache(ttl=TTL)
    def get_top_contries(self):
        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="country")],
            date_ranges=[DateRange(start_date="90daysAgo", end_date="yesterday")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=10,
        )

    @cache(ttl=TTL)
    def get_top_oses(self):
        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="operatingSystem")],
            date_ranges=[DateRange(start_date="90daysAgo", end_date="yesterday")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=10,
        )

    @cache(ttl=TTL)
    def get_top_browsers(self):
        return self._run_report(
            metrics=[Metric(name="sessions")],
            dimensions=[Dimension(name="browser")],
            date_ranges=[DateRange(start_date="90daysAgo", end_date="yesterday")],
            order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
            limit=10,
        )
