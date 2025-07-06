import threading

from django import db as django_db
from django.apps import apps as django_apps
from django.utils import timezone
from huey.constants import EmptyData
from huey.storage import BaseStorage, to_bytes, to_blob
from huey.utils import to_timestamp

from .huey import DjangoORMHuey # noqa: F401
from .vars import DEFAULT_PREFIX


class DjangoORMStorage(BaseStorage):
    model_prefix = DEFAULT_PREFIX
    task_model = None
    schedule_model = None
    keystore_model = None
    dequeue_lock = threading.Lock()

    def __init__(self, name='huey', **kwargs):
        super(DjangoORMStorage, self).__init__(name=name, **kwargs)
        self._local = threading.local()

    def _model_string(self, model_name):
        return f'{self.model_prefix}.{model_name}'

    def _get_model(self, model_name):
        return django_apps.get_model(
            self._model_string(model_name),
            require_ready=False,
        )

    def make_aware(self, huey_dt):
        return timezone.datetime.fromtimestaamp(
            to_timestamp(huey_dt),
            tz=timezone.timezone.utc
        )

    @property
    def queue_items(self):
        if self.task_model is None:
            self.task_model = self._get_model("HueyTask")
        return self.task_model.objects.filter(
            queue=self.name,
        ).order_by("-priority", "id")

    @property
    def schedule_tasks(self):
        if self.schedule_model is None:
            self.schedule_model = self._get_model("HueySchedule")
        return self.schedule_model.objects.filter(
            queue=self.name,
        ).order_by("timestamp")

    @property
    def values(self):
        if self.keystore_model is None:
            self.keystore_model = self._get_model("HueyKv")
        return self.keystore_model.objects.filter(
            queue=self.name,
        )

    @django_db.transaction.atomic(durable=False)
    def dequeue(self):
        with self.dequeue_lock:
            qs = self.queue_items.only('data')
            try:
                result = qs.first()
            except self.task_model.DoesNotExist:
                pass
            else:
                if result is not None:
                    data = result.data
                    result.delete()
                    return to_bytes(data)
        return None

    def enqueue(self, data, priority=None):
        if self.task_model is None:
            self.task_model = self._get_model("HueyTask")
        return self.task_model.objects.create(
            queue=self.name,
            data=data,
            priority=priority,
        )

    def queue_size(self):
        return self.queue_items.count()

    def enqueued_items(self, limit=None):
        items = self.queue_items
        if isinstance(limit, int):
            items = items[: limit]
        return [
            to_bytes(i.data)
            for i in items.only('data')
        ]

    def flush_queue(self):
        return self.queue_items.delete()

    def add_to_schedule(self, data, ts):
        if self.schedule_model is None:
            self.schedule_model = self._get_model("HueySchedule")
        return self.schedule_model.objects.create(
            queue=self.name,
            data=to_blob(data),
            timestamp=self.make_aware(ts),
        )

    @django_db.transaction.atomic(durable=False)
    def read_schedule(self, ts):
        scheduled_tasks = self.schedule_tasks.filter(
            timestamp__lte=self.make_aware(ts),
        ).only('id')
        ids = {
            scheduled_task.id
            for scheduled_task in scheduled_tasks
        }
        qs = self.schedule_tasks.filter(id__in=ids)
        data = [
            to_bytes(scheduled_task.data)
            for scheduled_task in qs.only('data')
        ]
        qs.delete()
        return data

    def schedule_size(self):
        return self.schedule_tasks.count()

    def scheduled_items(self, limit=None):
        scheduled_tasks = self.schedule_tasks
        if limit is not None:
            scheduled_tasks = scheduled_tasks[: limit]
        return [
            to_bytes(i.data)
            for i in scheduled_tasks.only('data')
        ]

    def flush_schedule(self):
        self.schedule_tasks.delete()

    def put_data(self, key, value, is_result=False):
        if self.keystore_model is None:
            self.keystore_model = self._get_model("HueyKv")
        return self.keystore_model.objects.create(
            queue=self.name,
            key=key,
            value=to_blob(value),
        )

    def peek_data(self, key):
        return self.pop_data(key, peek=True)

    @django_db.transaction.atomic(durable=False)
    def pop_data(self, key, peek=False):
        try:
            res = self.values.only(
                'key',
                'value',
            ).get(key=key)
        except self.keystore_model.DoesNotExist:
            return EmptyData
        else:
            if res is not None:
                data = to_bytes(res.value)
                if peek is False:
                    t = res.delete()
                    if 1 != t[0]:
                        return EmptyData
                return data
        return EmptyData

    def has_data_for_key(self, key):
        return self.peek_data(key) != EmptyData

    def result_store_size(self):
        return self.values.count()

    def result_items(self):
        return {
            i.key: to_bytes(i.value)
            for i in self.values.only('key', 'value')
        }

    def flush_results(self):
        self.values.delete()


