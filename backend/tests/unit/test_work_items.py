from app.tools import PermissionLevel
from app.tools.work_items import WorkItemStore


def make_store() -> WorkItemStore:
    return WorkItemStore(":memory:")


def test_permissions_are_tagged_correctly():
    assert WorkItemStore.PERMISSIONS["create"] == PermissionLevel.WRITE
    assert WorkItemStore.PERMISSIONS["get"] == PermissionLevel.READ
    assert WorkItemStore.PERMISSIONS["list"] == PermissionLevel.READ
    assert WorkItemStore.PERMISSIONS["update"] == PermissionLevel.WRITE
    assert WorkItemStore.PERMISSIONS["delete"] == PermissionLevel.DESTRUCTIVE


def test_create_and_get_round_trip():
    store = make_store()
    created = store.create(title="Fix checkout latency", description="Investigate pool size")

    assert created.id is not None
    assert created.title == "Fix checkout latency"
    assert created.status == "open"

    fetched = store.get(created.id)
    assert fetched == created


def test_get_returns_none_for_missing_item():
    store = make_store()
    assert store.get(999) is None


def test_list_filters_by_status():
    store = make_store()
    open_item = store.create(title="Open item")
    done_item = store.create(title="Done item")
    store.update(done_item.id, status="done")

    all_items = store.list()
    open_items = store.list(status="open")
    done_items = store.list(status="done")

    assert {i.id for i in all_items} == {open_item.id, done_item.id}
    assert [i.id for i in open_items] == [open_item.id]
    assert [i.id for i in done_items] == [done_item.id]


def test_update_changes_fields_and_returns_none_for_missing():
    store = make_store()
    item = store.create(title="Original title")

    updated = store.update(item.id, title="New title", status="in_progress")
    assert updated.title == "New title"
    assert updated.status == "in_progress"

    assert store.update(999, title="doesn't exist") is None


def test_delete_removes_item_and_returns_false_for_missing():
    store = make_store()
    item = store.create(title="Temporary")

    assert store.delete(item.id) is True
    assert store.get(item.id) is None
    assert store.delete(item.id) is False
