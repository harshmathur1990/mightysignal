# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, validates, ValidationError, validates_schema, validate


class ScrapeRequestSchema(Schema):
    app_name = fields.Str(required=True)
    app_store_url = fields.URL(required=True)

    @validates('app_store_url')
    def validate_app_store_url(self, value):
        if not value.startswith(u'https://itunes.apple.com/'):
            raise ValidationError(u'only itunes URLs are allowed')


class ScrapeRequestData(Schema):

    data = fields.Nested(
        ScrapeRequestSchema,
        validate=validate.Length(
           min=1,
           error='Field may not be an empty list'
        ),
        required=True,
        many=True
    )