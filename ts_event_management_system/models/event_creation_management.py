import logging

from odoo import api, fields, models
from odoo.tools import format_datetime

from odoo.addons.base.models.res_partner import _tz_get

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventCreationManagement(models.Model):
    _name = "ts.event.creation"
    _inherit = "mail.thread"
    _description = "Event Creation And Management"

    name = fields.Char(string="Event Name")
    ts_event_type_id = fields.Many2one("ts.event.type", string="Event Type")
    date_tz = fields.Selection(
        _tz_get,
        string="Event Timezone",
        required=True,
        compute="_compute_date_tz",
        precompute=True,
        readonly=False,
        store=True,
    )
    date_begin = fields.Datetime(string="Start Date", required=True, tracking=True)
    date_end = fields.Datetime(string="End Date", required=True, tracking=True)
    date_begin_located = fields.Char(
        string="Start Date Located", compute="_compute_date_begin_tz"
    )
    date_end_located = fields.Char(
        string="End Date Located", compute="_compute_date_end_tz"
    )
    default_timezone = fields.Selection(
        _tz_get, string="Timezone", default=lambda self: self.env.user.tz or "UTC"
    )

    status = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirmed")], default="draft", string="status"
    )
    address = fields.Text(string="", tracking=True)
    location = fields.Char(string="", tracking=True)
    district = fields.Char(string="", tracking=True)
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one("res.country", string="Country")

    sponsor_ids = fields.Many2many(
        "ts.sponsor.management",
        "event_sponsor_rel",
        "event_id",
        "sponsor_id",
        string="Sponsors",
    )

    speaker_ids = fields.Many2many(
        "ts.speaker.management",
        "event_speaker_rel",
        "event_id",
        "speaker_id",
        string="Speakers",
    )

    session_ids = fields.One2many("ts.event.session", "event_name_id")

    participant_count = fields.Integer(string="", compute="_compute_participant_count")

    ts_participant_ids = fields.One2many(
        "ts.participant.details", "event_registration_id"
    )

    @api.depends("date_tz", "date_begin")
    def _compute_date_begin_tz(self):
        for event in self:
            if event.date_begin:
                event.date_begin_located = format_datetime(
                    self.env, event.date_begin, tz=event.date_tz, dt_format="medium"
                )
            else:
                event.date_begin_located = False

    @api.depends("date_tz", "date_end")
    def _compute_date_end_tz(self):
        for event in self:
            if event.date_end:
                event.date_end_located = format_datetime(
                    self.env, event.date_end, tz=event.date_tz, dt_format="medium"
                )
            else:
                event.date_end_located = False

    @api.depends("ts_event_type_id")
    def _compute_date_tz(self):
        for event in self:
            if event.ts_event_type_id.default_timezone:
                event.date_tz = event.ts_event_type_id.default_timezone
            if not event.date_tz:
                event.date_tz = self.env.user.tz or "UTC"

    def action_confirm(self):
        self.status = "confirm"

    @api.depends("participant_count")
    def _compute_participant_count(self):
        for rec in self:
            rec.participant_count = rec.env["ts.participant.details"].search_count(
                [("event_registration_id", "=", rec.id)]
            )

    def unlink(self):
        for event in self:
            sessions = self.env["ts.event.session"].search(
                [("event_name_id", "=", event.name)]
            )
            participants = self.env["ts.participant.details"].search(
                [("event_registration_id", "=", event.name)]
            )
            sessions.unlink()
            participants.unlink()
        return super(EventCreationManagement, self).unlink()

    def open_participant_details_wizard(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Create Participant Details",
            "res_model": "ts.participant.details",
            "view_mode": "form",
            "view_id": self.env.ref(
                "ts_event_management_system.view_ts_participant_details_form"
            ).id,
            "target": "new",
            "context": {
                "default_event_registration_id": self.id,
            },
        }
