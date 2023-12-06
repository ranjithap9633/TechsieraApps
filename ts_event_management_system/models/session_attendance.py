import logging

from odoo import api, fields, models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SessionAttendance(models.Model):
    _name = "ts.session.attendance"
    _description = "Session Attendance"
    _order = "event_id desc"

    event_id = fields.Many2one("ts.event.creation", string="Event Name")
    session_id = fields.Many2one("ts.event.session", string="Event Session")
    participant_id = fields.Many2one(
        "ts.participant.details", string="Participant", required=True
    )
    attended = fields.Boolean(string="")

    @api.depends("session_id")
    def action_save(self):
        logger.info("Save button is triggering..")
        for rec in self:
            if rec.session_id:
                registration = rec.session_id
                registration.attendees += 1
                rec.session_id._compute_attendee_count()

    _sql_constraints = [
        (
            "unique_attendance",
            "UNIQUE(participant_id, event_id, session_id)",
            "Attendance already marked.",
        )
    ]
