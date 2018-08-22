# -*- coding: utf-8 -*-


from marshmallow import Schema, fields, validates, ValidationError


class ScrapeRequestSchema(Schema):
    app_name = fields.Str(required=True)
    app_store_url = fields.URL(required=True)

    @validates('app_store_url')
    def validate_quantity(self, value):
        if not value.startswith(u'https://itunes.apple.com/'):
            raise ValidationError(u'only itunes URLs are allowed')


class AppsiniOS(Schema):
    languages = fields.List(fields.Str(required=True), required=True)
    app_identifier = fields.Int(required=True)
    name = fields.Str(required=True)
    minimum_version = fields.Str(required=True)