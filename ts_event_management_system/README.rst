Event Management System
========================

Introduction
------------
The Event Management System is a web-based application built with Odoo for managing events and registrations. This system allows users to create, manage, and track various events and registrations efficiently.

Features
--------

- **Event Creation**: Create and configure event details, such as event name, date, location, and more.

- **Event Registration**: Users can register for events, providing their information and preferences.

- **Event Types**: Organize events by types (e.g., conferences, workshops) for better categorization.

- **Timezone Support**: Specify timezones for events and registrations to accommodate global audiences.

- **Participant Details**: Events can be in "Draft" or "Confirmed" status, allowing for planning and confirmation stages.

- **Event Session**: Collect and display address, district, state, and country data for events and registrations. Also take attendance by session.

- **Session Attendance**: Track attendance for event sessions or workshops.
  Mark participants' attendance and keep records for future reference.

- **Speaker Management**: Manage details about event speakers and presenters.
  Include speaker bios, contact information, and links to their profiles.

- **Sponsor Management**: Manage sponsors for your events.
  Include sponsor details, logos, and sponsorship levels.

Getting Started
---------------

1. **Installation**: To install the Event Management System, follow these steps:

   - Clone the repository.
   - Install Odoo and its dependencies.
   - Import the module into your Odoo instance.
   - Install additional fonts (if required):
     sudo apt-get install ttf-mscorefonts-installer

2. **Configuration**: Configure the system with your specific settings, such as default timezones and other parameters.

3. **User Access**: Assign proper user access rights to manage events and registrations.

Usage
-----

1. **Create Event**:
   - Log in as an administrator.
   - Go to the "Events" section and click "Create Event."
   - Fill in event details, including name, date, location, and other relevant information.
   - Save the event to create it.

2. **Edit Event**:
   - If you need to make changes to an event, go to the "Events" section and click on the event you want to edit.
   - Update the event details and click "Save" to confirm the changes.

3. **Delete Event**:
   - In case an event is no longer relevant, administrators can delete it.
   - Navigate to the event you wish to remove and click "Delete Event." Confirm the deletion when prompted.

4. **Register for Event**:
   - Users can easily register for events by following these steps:
   - Browse the list of available events.
   - Click on the event they want to attend.
   - Complete the registration form with their details.
   - Click "Register" to confirm their attendance.

5. **View Event Details**:
   - Users can explore an event's details by clicking on the event from the list.
   - The event page displays information about the event, including registered participants and location.

6. **View Registrants**:
   - To view a list of participants who have registered for an event, visit the event page and click "View Registrants."

7. **Manage Speakers**:
   - Administrators can add and manage speakers for events.
   - Navigate to the event management dashboard, and you will find options to add, edit, or delete speakers.

8. **Manage Sponsors**:
   - If an event has sponsors, administrators can manage sponsor information.
   - In the event management section, you can add, edit, or delete sponsors for each event.
