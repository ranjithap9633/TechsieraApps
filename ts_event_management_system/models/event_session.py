import logging
from gettext import gettext as _

from odoo import api, fields, models
from odoo.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventSession(models.Model):
    _name = "ts.event.session"
    _description = "Event Sessions"
    _order = "event_name_id"

    name = fields.Char(string="Session Name", required=True)
    event_name_id = fields.Many2one("ts.event.creation", string="")
    agenda = fields.Text(string="")
    start = fields.Datetime(string="", required=True)
    end = fields.Datetime(string="", required=True)
    participant_details_ids = fields.One2many(
        "ts.participant.details", "session_id", string="Participant Details"
    )
    # participant_count = fields.Integer(string="", compute="_compute_participant_count")
    attendance = fields.Char(string="Attended/Total", compute="_compute_attendance")
    attendees = fields.Integer(string="", compute="_compute_attendee_count")
    session_id = fields.Many2one("ts.speaker.management", string="Speaker")
    sponsor_id = fields.Many2one(
        "ts.sponsor.management",
    )
    participant_attendance = fields.One2many(
        "ts.session.attendance", "session_id", string="Info"
    )

    @api.depends("attendees")
    def _compute_attendee_count(self):
        for rec in self:
            rec.attendees = rec.env["ts.session.attendance"].search_count(
                [("session_id", "=", rec.id)]
            )

    def mark_session_attendance(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Mark Attendance",
            "res_model": "ts.session.attendance",
            "view_mode": "form",
            "view_id": self.env.ref(
                "ts_event_management_system.view_ts_session_attendance_form"
            ).id,
            "target": "new",
            "context": {
                "default_session_id": self.id,
                "default_event_id": self.event_name_id.id,
            },
        }

    @api.constrains("start", "end")
    def _check_dates(self):
        for session in self:
            if session.start >= session.end:
                raise ValidationError(
                    _("Session start time should be before session end time.")
                )
            if (
                session.start < session.event_name_id.date_begin
                or session.end > session.event_name_id.date_end
            ):
                raise ValidationError(
                    _("Session date and time must be within the event's date range.")
                )

    @api.depends("event_name_id.participant_count", "attendees")
    def _compute_attendance(self):
        for record in self:
            record.attendance = (
                f"{record.attendees}/{record.event_name_id.participant_count}"
            )

    def info(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Session Wise Participant Attendance",
            "view_type": "form",
            "view_mode": "tree,form",
            "res_model": "ts.session.attendance",
            "target": "new",
            "context": {
                "default_session_id": self.id,
            },
            "domain": [("session_id", "=", self.id)],
        }
