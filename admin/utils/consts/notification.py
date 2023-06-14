from .base import ReprEnum


class StatusT(ReprEnum):
    UNREAD = 'unread'
    READ = 'read'


class TypeT(ReprEnum):
    GENERAL = 'general'
    INVESTMENT = 'investment'
    DISTRIBUTION = 'distribution'
    SECURITY = 'security'
    SYSTEM = 'system'
