import json

from django.db.models import JSONField
from django.db.models.fields.json import KeyTransform


class JSONField(JSONField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Some backends (SQLite at least) extract non-string values in their
        # SQL datatypes.
        if isinstance(expression, KeyTransform) and not isinstance(value, str):
            return value
        try:
            return json.loads(value, cls=self.decoder)
        except TypeError:
            return value
        except json.JSONDecodeError:
            return value