import os
import pwd

from peewee import *


def get_db_url():
    user = pwd.getpwuid(os.getuid()).pw_name
    url = f'/Users/{user}/Library/Group Containers/' \
          f'JLMPQHK86H.com.culturedcode.ThingsMac/Things Database.thingsdatabase/main.sqlite'
    return url


db = SqliteDatabase(get_db_url())


class BaseModel(Model):
    class Meta:
        database = db

    def as_dict(self):
        return {n: getattr(self, n) for n in self._meta.sorted_field_names}


class Task(BaseModel):
    uuid = TextField(primary_key=True)
    created = TimestampField(db_column='creationDate')
    modified = TimestampField(db_column='userModificationDate')
    trashed = BooleanField(null=True)
    # type: TODO
    title = TextField(null=True)
    notes = TextField(null=True)

    class Meta:
        table_name = 'TMTask'

    @property
    def tags(self):
        return (Tag
                .select()
                .join(TaskTag)
                .join(Task)
                .where(Task.uuid == self.uuid))


class Tag(BaseModel):
    uuid = TextField(primary_key=True)
    title = TextField(null=True)
    used_at = TimestampField(db_column='usedDate')

    class Meta:
        table_name = 'TMTag'


class TaskTag(BaseModel):
    task = ForeignKeyField(Task, field='uuid', db_column='tasks')
    tag = ForeignKeyField(Tag, field='uuid', db_column='tags')

    class Meta:
        table_name = 'TMTaskTag'
