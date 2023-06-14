from .base import ReprEnum

class ProfileT(ReprEnum):
    INDIVIDUAL = 'individual'
    ENTITY = 'entity'
    TRUST = 'trust'
    WINTER = 'sdira'
    SOLO401K = 'solo401k'

class KYCT(ReprEnum):
    NONE = 'none'
    NEW = 'new'
    PENDING = 'pending'
    APPROVED = 'approved'
    DECLINED = 'declined'

class AccreditationT(ReprEnum):
    NONE = 'none'
    NEW = 'new'
    PENDING = 'pending'
    DOCUMENT_REQUIRED = 'document_required'
    INFO_REQUIRED = 'info_required'
    EXPIRED = 'expired'
    APPROVED = 'approved'
    DECLINED = 'declined'
