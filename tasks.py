from invoke.collection import Collection
from utils.tasks.one_time_tasks import one_time_tasks_ns

ns = Collection()
ns.add_collection(one_time_tasks_ns)
