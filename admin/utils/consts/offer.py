from .base import ReprEnum

class StatusT(ReprEnum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    NEW = 'new'
    DRAFT = 'draft'
    LEGAL_REVIEW = 'legal-review'
    LEGAL_DECLINED = 'legal-declined'
    LEGAL_ACCEPTED = 'legal-accepted'
    PUBLISHED = 'published'
    LEGAL_CLOSED = 'legal-closed'
    CLOSED_SUCCESFULLY = 'closed-successfully'
    CLOSED_UNSUCCESFULLY = 'closed-unsuccesfully'
    SOLD = 'sold'
    EXITED = 'exited'


class SecurityT(ReprEnum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value

    NEW = 'equity'
    DRAFT = 'preferred-equity'
    LEGAL_REVIEW = 'debt'
    LEGAL_DECLINED = 'convertible-debt'
    LEGAL_ACCEPTED = 'equity-warrants'
    PUBLISHED = 'convertible-bonds'
    CLOSED_SUCCESFULLY = 'preference-shares'
