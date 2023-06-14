import aiohttp
import logging

from aiohttp import web
import aiohttp_boilerplate
from aiohttp_boilerplate import models

from utils import consts


class Filer(models.Manager):
    __table__ = 'filer_filers'


class OfferFiler(models.Manager):
    __table__ = 'offer_offer_filers'

# Offer Model
class Offer(models.Manager):
    __table__ = 'offer_offers'

    async def get_company_public_documents(self):
        if not self.id or self.id == '':
            raise Exception("id not set, cannot proceed")

        public_files = []
        try:
            company_files = await OfferFiler(db_pool=self.db_pool, is_list=True).get_by(
                fields='filer_id',
                offer_id=self.id,
                type='company', # ToDo move type to const
            )

            if len(company_files.data) > 0:
                filer_ids = ",".join([str(v.filer_id) for v in company_files.data])

                # ToDo, add check that filer is in public_view group
                temp_res = await Filer(db_pool=self.db_pool, is_list=True).select(
                    fields='url,filename,mime,name,updated_at',
                    where=f"id in ({filer_ids})",
                )
                for file in temp_res.data:
                    public_files.append(file.data)
        except web.HTTPNotFound:
            pass
        except Exception as e:
            logging.error(e)
        return public_files
    
    @staticmethod
    async def get_offer_for_investment(db_pool, slug):
        offer_obj = Offer(db_pool=db_pool)
        return await offer_obj.get_by(
            fields='id,name,price_per_share,total_shares,slug,subscribed_shares',
            slug=slug,
            status=consts.offer.StatusT.PUBLISHED.value,
        )

class Investment(models.Manager):
    __table__ = 'investment_investments'

    AVAILABLE_TO_CANCEL = [
        consts.investment.StatusT.NONE.value,
        consts.investment.StatusT.NEW.value,
        consts.investment.StatusT.CONFIRMED.value,
        consts.investment.StatusT.ESCROW.value,
        consts.investment.StatusT.ESCROW_DECLINED.value,
        consts.investment.StatusT.ESCROW_ERROR.value,
        consts.investment.StatusT.CONF_IN_PROGRESS.value,
        consts.investment.StatusT.KYC_IN_PROGRESS.value,
        consts.investment.StatusT.LEGALLY_CONFIRMED.value,
    ]

    UNCONFIRMED_STATUS = [
        consts.investment.StatusT.NONE.value,
        consts.investment.StatusT.NEW.value,
    ]

    CONFIRMED_STATUS = [
        consts.investment.StatusT.CONFIRMED.value,
        consts.investment.StatusT.ESCROW.value,
        consts.investment.StatusT.ESCROW_DECLINED.value,
        consts.investment.StatusT.ESCROW_ERROR.value,
        consts.investment.StatusT.CONF_IN_PROGRESS.value,
        consts.investment.StatusT.KYC_IN_PROGRESS.value,
        consts.investment.StatusT.LEGALLY_CONFIRMED.value,
    ]

    def can_cancel(self) -> bool:
        return self.status in self.AVAILABLE_TO_CANCEL

class Profile(models.Manager):
    __table__ = 'investment_profiles'

    async def create_stripe_account(self, stripe_secret_key, data: dict) -> dict:
        customer = {}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.stripe.com/v1/customers', data=data,
                auth=aiohttp.BasicAuth(stripe_secret_key,)
            ) as response:
                customer = await response.json()

        if 'error' in customer:
            raise web.HTTPNotFound({'credit_card': [customer['error']]})

        # ToDo
        # Save stripe account data in the database
        await self.update(
            ref_num=customer['id'],
            ref_data=customer,
        )
        return customer

    async def stripe_charge(self, stripe_secret_key, charge_data: dict) -> dict:
        charge = {}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://api.stripe.com/v1/charges', data=charge_data,
                auth=aiohttp.BasicAuth(stripe_secret_key,)
            ) as response:
                charge = await response.json()

        if 'error' in charge:
            raise JSONHTTPError({'credit_card': [charge['error']]})

        if charge['status'] != 'succeeded':
            raise JSONHTTPError({'credit_card': [charge['status']]})
        return charge


class User(models.Manager):
    __table__ = 'user_users'
    profile = {
        'individual': None,
    }

    async def get_or_create_profile(self, ptype: str) -> Profile:
        # for some reason it getting cached between requests
        # if self.profile[ptype]:
        #    return self.profile[ptype]

        if not self.id:
            raise TypeError("user id is None")
        try:
            self.profile[ptype] = await Profile(db_pool=self.sql.db_pool).get_by(
                user_id=self.id,
                type=ptype,
            )
        except aiohttp.web.HTTPNotFound:
            self.profile[ptype] = await Profile(db_pool=self.sql.db_pool).insert(
                user_id=self.id,
                type=ptype,
                kyc_status='none',
                accreditation_status='none',
            )

        return self.profile[ptype]

    async def get_total_investment_amount(self) -> float:
        invest = Investment(db_pool=self.sql.db_pool)
        query = "SELECT sum(amount) FROM investment_investments \
            WHERE user_id={user_id} and status IN ({" \
            + '}, {'.join(invest.CONFIRMED_STATUS) \
            + "})"

        params = {
            'user_id': self.id,
        }

        for v in invest.CONFIRMED_STATUS:
            params[v] = v

        query = invest.sql.prepare_where(query, params)
        res = await invest.sql.execute(
            query=query, params=params, fetch_method=aiohttp_boilerplate.sql.consts.FETCHVAL
        )
        return res
    
    async def get_total_investment_amount_12_months(self) -> float:
        invest = Investment(db_pool=self.sql.db_pool)
         # TODO
         # submited_at заминити на confirmed_at та оновили логіку get_total_investment_amount_12_months
        query = "SELECT sum(amount) FROM investment_investments \
            WHERE user_id={user_id} and status IN ({" \
            + '}, {'.join(invest.CONFIRMED_STATUS) \
            + "}) AND created_at > NOW() - INTERVAL '1 year'"

        params = {
            'user_id': self.id,
        }

        for v in invest.CONFIRMED_STATUS:
            params[v] = v

        query = invest.sql.prepare_where(query, params)
        res = await invest.sql.execute(
            query=query, params=params, fetch_method=aiohttp_boilerplate.sql.consts.FETCHVAL
        )
        return res

    async def get_total_distributions(self) -> float:
        return 0.0

    async def get_avarange_annual(self) -> float:
        return 0.0
    
# UserData Model
class UserData(models.JsonbManager):
    __table__ = 'user_users'
    __key_name__ = 'data'

class Email(models.Manager):
    __table__ = 'email_emails'

    async def create(self, data: dict):
        self.data.update(data)
        if 'user_id' not in self.data and 'recipient_email' not in self.data:
            raise TypeError("you need to set up user_id or recipient_email email")

        if 'user_id' in self.data and 'recipient_email' not in self.data:
            try:
                user = await User(db_pool=self.sql.db_pool).get_by(
                    'id,first_name,last_name,email',
                    id=self.data['user_id'],
                )
                self.data['recipient_email'] = user.email
                self.data['recipient_name'] = f'{user.first_name} {user.last_name}'
            except aiohttp.web.HTTPNotFound:
                logging.exception('cannot find user {}' % self.data['user_id'])
        if 'sender_email' not in self.data:
            self.data['sender_email'] = 'cachealot@gmail.com'
            self.data['sender_name'] = 'Investment Management'
        # we need to remove default id=null
        data = {}
        data.update(self.data)
        del data['id']
        return await self.insert(data)

class ProfileOwnership(models.JsonbManager):
    __table__ = 'investment_profiles'
    __key_name__ = 'data'

class SignatureOwnership(models.JsonbManager):
    __table__ = 'investment_investments'
    __key_name__ = 'signature_data'


class Comment(models.Manager):
    __table__ = 'offer_comments'


class Notification(models.Manager):
    __table__ = 'notification_notifications'

    @staticmethod
    async def create(db_conn, *fields, **kwargs):
        notif = Notification(db_pool=db_conn)
        return await notif.insert(*fields, **kwargs)
