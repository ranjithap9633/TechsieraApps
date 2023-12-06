from odoo import fields, models


class EventTypeMaster(models.Model):
    _name = "ts.event.type"
    _description = "Event Type Master"

    name = fields.Char(string="Event Type", required=True)
    describe = fields.Text(string="Description")
    default_timezone = fields.Char(string="")
    image = fields.Binary(
        "",
        attachment=True,
        help="This field holds the image used as "
        "image for the event, limited to 1080x720px.",
    )
    status = fields.Selection(
        [("draft", "Draft"), ("confirm", "Confirmed")], default="draft", string="status"
    )
    truncated_description = fields.Char(
        string="Description Inshort", compute="_compute_truncated_description"
    )
    active_id = fields.Boolean(string="", default=True)

    def _compute_truncated_description(self):
        max_length = 18
        for record in self:
            if record.describe and len(record.describe) > max_length:
                record.truncated_description = record.describe[:max_length] + "..."
            else:
                record.truncated_description = record.describe

    def action_confirm(self):
        self.status = "confirm"
        if self.active_id:
            return {
                "name": "Event Creation Form",
                "view_mode": "form",
                "res_model": "ts.event.creation",
                "type": "ir.actions.act_window",
                "target": "current",
                "context": {
                    "default_ts_event_type_id": self.id,
                },
            }

    def action_update(self):
        self.status = "draft"
