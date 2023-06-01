from .base import ReprEnum


class StatusT(ReprEnum):
    NONE = 'none'
    NEW = 'new'
    CONFIRMED = 'confirmed'
    ESCROW = 'escrow'
    ESCROW_DECLINED = 'escrow_declined'
    ESCROW_ERROR = 'escrow_error'
    KYC_IN_PROGRESS = 'kyc_in_progress'
    CONF_IN_PROGRESS = 'accreditation_in_progress'
    LEGALLY_CONFIRMED = 'legally_confirmed'
    UNSUCCESFULLY_CLOSE = 'closed_unsucessfully'
    SUCCESSFULLY_CLOSE = 'closed_successfully'
    CANCELED_DURING_INVESTMENT = 'cancelled_during_investment'
    CANCELED_AFTER_INVESTMENT = 'cancelled_after_investment'
    CANCELED_BY_MANAGER = 'cancelled_by_manager'
    SYSTEM_ERROR = 'system_error'


class EscrowT(ReprEnum):
    NONE = 'none'
    NORTH_CAPITAL = 'north_capital'
    PRIME_TRUST = 'prime_trust'
    APEX_GROUP = 'apex_group'


class FundingT(ReprEnum):
    NONE = 'none'
    WIRE = 'wire'
    ACH = 'ach'
    WALLET = 'wallet'


class StepT(ReprEnum):
    NONE = 'none'
    NEW = 'new'
    AMOUNT = 'amount'
    OWNERSHIP = 'ownership'
    SIGNATURE = 'signature'
    FUNDING = 'funding'
    ACCREDITATION = 'accreditation'
    CONFIRMATION = 'confirmation'
    REVIEW = 'review'
