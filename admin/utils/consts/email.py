from .base import ReprEnum


class StatusT(ReprEnum):
    DRAFT = 'draft'
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    SENT = 'sent'
    CANCELLED = 'cancelled'
    ERROR = 'error'

EMAIL_TEMPLATES = (
  ('user:welcome', 'user/welcome.pug'),
  ('offer:material-change', 'offer/material-change.pug'),
  ('offer:early-completion', 'offer/early-completion.pug'),
  ('offer:legally-closed', 'offer/legally-closed.pug'),
  ('offer:succesfully-closed', 'offer/succesfully-closed.pug'),
  ('investment:canceled-during-investment', 'investment/canceled-during-investment.pug'),
  ('investment:return-funds', 'investment/return-funds.pug'),
  ('investment:failed-to-reconfirm', 'investment/failed-to-reconfirm.pug'),
)
