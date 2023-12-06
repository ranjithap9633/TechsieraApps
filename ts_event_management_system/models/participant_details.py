import base64
import logging
import re
import uuid
from gettext import gettext as _
from io import BytesIO

import qrcode
from PIL import Image, ImageDraw, ImageFont

from odoo import api, fields, models
from odoo.exceptions import ValidationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParticipantDetailsWizard(models.Model):
    _name = "ts.participant.details"
    _description = "Details of participants"
    _order = "registration_date desc"

    event_registration_id = fields.Many2one(
        "ts.event.creation", string="Event Registered"
    )
    name = fields.Char(string="", required=True)
    institution = fields.Text(string="")
    phone = fields.Char(string="", default="+91 ")
    email = fields.Char(string="", required=True)
    address = fields.Text(string="")
    district = fields.Char(string="")
    state = fields.Many2one("res.country.state", string="")
    country = fields.Many2one("res.country", string="")
    registration_date = fields.Datetime(
        string="Created Date", default=lambda self: fields.Datetime.now()
    )
    session_id = fields.Many2one("ts.event.session", string="Event Session")
    even_participant_ids = fields.One2many("ts.session.attendance", "participant_id")
    qr_code_image = fields.Binary(string="QR Code Image", attachment=True)
    qr_code_report = fields.Binary(string="QR Code Image Report", attachment=True)
    uniq_qr_id = fields.Char(string="Unique QR ID")

    def generate_image_report(self):
        logo_data = self.env["res.company"].browse(self.env.company.id).logo
        company_name = self.env["res.company"].browse(self.env.company.id).name
        event_name = self.event_registration_id.name
        qr_code_image = self.generate_qr_code()
        qr_code_id = self.uniq_qr_id
        participant_name = self.name

        width, height = 600, 800  # Adjust the width and height of the image as needed
        background_color = (255, 255, 255)  # White color
        text_color = (0, 0, 0)  # Black color
        font_path = (
            "/var/lib/update-notifier/package-data-downloads/partial/arialbi.ttf"
        )

        img = Image.new("RGB", (width, height), background_color)
        draw = ImageDraw.Draw(img)

        font = ImageFont.load_default()
        font2 = ImageFont.truetype(font_path, 15)
        font3 = ImageFont.truetype(font_path, 20)

        event_name_width, event_name_height = draw.textsize(event_name, font=font2)
        center_x_event = self.calculate_x_position(img.width, event_name_width)
        draw.text((center_x_event, 225), event_name, fill=text_color, font=font2)

        qr_id_width, qr_id_height = draw.textsize(qr_code_id, font=font)
        center_x_qr = self.calculate_x_position(img.width, qr_id_width)
        draw.text((center_x_qr, 245), f"ID: {qr_code_id}", fill=text_color, font=font)

        qr_code_img = Image.open(BytesIO(base64.b64decode(qr_code_image)))
        resized_qr_code_img = qr_code_img.resize((200, 200))

        # Paste the resized QR code image onto img
        img.paste(resized_qr_code_img, (200, 255))

        participant_name_width, participant_name_height = draw.textsize(
            participant_name, font=font2
        )
        center_x_participant = self.calculate_x_position(
            img.width, participant_name_width
        )
        draw.text(
            (center_x_participant, 445), participant_name, fill=text_color, font=font2
        )

        # Adding company logo to the generated image
        if logo_data:
            logo_image = Image.open(BytesIO(base64.b64decode(logo_data)))
            center_x_logo = self.calculate_x_position(img.width, logo_image.width)
            img.paste(logo_image, (center_x_logo, 50))
        if company_name:
            company_name_width, company_name_height = draw.textsize(
                company_name, font=font3
            )
            center_x_company = self.calculate_x_position(img.width, company_name_width)
            draw.text(
                (center_x_company, 200), company_name, fill=text_color, font=font3
            )

        # Saving the image to a buffer
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        img_binary = img_buffer.getvalue()

        self.write({"qr_code_report": base64.b64encode(img_binary)})

    def generate_qr_code(self):
        unique_id = str(uuid.uuid4())
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(
            f"Participant: {self.name}, "
            f"Event: {self.event_registration_id.name}, "
            f"Institution: {self.institution}, "
            f"Date of Registration: {self.registration_date}, "
            f"id: {unique_id}"
        )

        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        self.uniq_qr_id = unique_id
        return base64.b64encode(img_byte_array.getvalue()).decode()

    def calculate_x_position(self, image_width, element_width):
        return (image_width - element_width) // 2

    def action_save(self):
        logger.info("Participant Details action_save method is being called")
        for rec in self:
            if rec.event_registration_id:
                registration = rec.event_registration_id
                registration.participant_count += 1
                rec.event_registration_id._compute_participant_count()

                qr_code_data = rec.generate_qr_code()
                rec.qr_code_image = qr_code_data
                rec.generate_image_report()

                logger.info("Sending confirmation email to: %s", rec.name)
                template = self.env.ref(
                    "ts_event_management_system.ts_event_remainder_id"
                )
                template.with_context(object=rec).send_mail(rec.id, force_send=True)

    @api.constrains("email")
    def _check_valid_email(self):
        for record in self:
            if record.email:
                self._validate_email(record.email)

    @staticmethod
    def _validate_email(email):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise ValidationError(_("Invalid email address: %s") % email)

    @api.constrains("phone")
    def _check_phone_number(self):
        for record in self:
            if record.phone:
                record._validate_phone(record.phone)

    @staticmethod
    def _validate_phone(phone):
        phone_pattern = r"^\+91\s?\d{10}$"
        if not re.match(phone_pattern, phone):
            raise ValidationError(
                f"Invalid phone number: {phone}. "
                f"Please use a valid format, e.g., '+91 1234567890'."
            )


_sql_constraints = [
    (
        "unique_email_per_event",
        "UNIQUE (event_registration_id, email)",
        "Participant with this email already registered for this event!",
    ),
]
