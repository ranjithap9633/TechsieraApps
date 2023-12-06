import re
from gettext import gettext as _

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SponsorManagement(models.Model):
    _name = "ts.sponsor.management"
    _description = "Sponsor Management"

    name = fields.Char(string="Sponsor", required="True")
    phone = fields.Char(string="Contact", default="+91 ")
    email = fields.Char(string="")
    website = fields.Char(string="")
    event_ids = fields.Many2many(
        "ts.event.creation",
        "event_sponsor_rel",
        "sponsor_id",
        "event_id",
        string="Events",
    )
    session_ids = fields.One2many("ts.event.session", "sponsor_id")

    @api.constrains("email")
    def _check_valid_email(self):
        for record in self:
            if record.email:
                self.env["ts.participant.details"]._validate_email(record.email)

    @api.constrains("phone")
    def _check_valid_phone(self):
        for record in self:
            if record.phone:
                self.env["ts.participant.details"]._validate_phone(record.phone)

    @api.constrains("website")
    def _check_valid_website(self):
        for record in self:
            if record.website:
                self._validate_website(record.website)

    @staticmethod
    def _validate_website(website):
        if not re.match(r"^(www\.[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", website):
            raise ValidationError(_("Invalid website URL: %s") % website)
