# TODO

## User features

- ~~custom 404 page~~

- email event guests
  - ~~form to RSVP to an event~~
  - allow users to store and send from multiple email addresses
  - html email templates
    - ~~single template pulling invitee name, event description, etc (MVP)~~
    - add styling
    - support gifs
    - wysiwyg
  - send follow up emails to invitees who haven't responded
    - schedule followup emails

- create events
  - ~~improve event model (start time, end time, etc)~~
  - ~~description should be textfield~~
  - user-friendly time format
  - create invitations in bulk at same time as event creation in admin

- create contacts
  - ~~refine contact model (how should names be stored, etc)~~
  - ~~support bulk upload of contacts~~
  - support mailing lists

- blog
  - ~~add `is_published` bool and only show published posts~~
  - let author preview post before publishing
  - button to publish
  - ~~author should be read_only and based on the logged in user when post is created~~
  - track updated time

## Tech

- automate DB backups
- create tests
  - contacts csv bulk upload
- update to Django 5.0
