from odoo import api, fields, models


class SpeakerManagement(models.Model):
    _name = "ts.speaker.management"
    _description = "Speaker Management"

    name = fields.Char(string="Speakers", required=True)
    phone = fields.Char(string="Contact", default="+91")
    email = fields.Char(string="")
    website = fields.Char(string="")
    events_ids = fields.Many2many(
        "ts.event.creation",
        "event_speaker_rel",
        "speaker_id",
        "event_id",
        string="Events",
    )

    session_ids = fields.One2many("ts.event.session", "session_id")

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
                self.env["ts.sponsor.management"]._validate_website(record.website)
