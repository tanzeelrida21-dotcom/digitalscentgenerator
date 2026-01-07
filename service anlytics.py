class AnalyticsService:
    def __init__(self, db):
        self.db = db

    def get_usage_stats(self):
        return self.db.execute_query("SELECT COUNT(*) FROM GeneratedFormulas")