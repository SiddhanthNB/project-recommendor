from invoke import Collection, task

from utils.migrations.mongo_to_sheets import run_migration


@task()
def migrate_mongo_docs_into_gsheets(ctx):
    """One-time migration helper to push existing Mongo docs into Sheets."""
    run_migration()


one_time_tasks_ns = Collection("one_time_tasks")
one_time_tasks_ns.add_task(migrate_mongo_docs_into_gsheets, "migrate_mongo_docs_into_gsheets")
