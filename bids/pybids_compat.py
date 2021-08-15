import bids.schema as bs
import bids.query as qr


class BIDSLayout:
    def __init__(self, ds_dir: str):
        sc = bs.Schema()
        self.dataset = sc.load_dataset(ds_dir)
        self.query_exec = qr.QueryExecutor(self.dataset, sc)

    def _query(self, expr: str):
        qry = qr.Query(expr)
        qry_result = self.query_exec.execute(qry)
        return qry_result.result

    def get_subjects(self):
        return self._query('//bids:subjects/@name')

    def get_sessions(self):
        return self._query('//bids:sessions/@name')

    def get_tasks(self):
        tasks = self._query('//bids:entities[@key = "task"]/@value')
        tasks = list(set(tasks))
        return tasks
