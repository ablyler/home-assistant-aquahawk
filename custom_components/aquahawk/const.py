from enum import Enum

DOMAIN = "aquahawk"

CONF_HOSTNAME = "hostname"
CONF_ACCOUNT_NUMBER = "account_number"
CONF_USERNAME = "username"
# trunk-ignore(bandit/B105)
CONF_PASSWORD = "password"


class Period(Enum):
    PERIOD_THIS_YEAR = "this_year"
    PERIOD_TODAY = "today"


ATTR_YEAR_TOTAL_GALLONS = "year_total_gallons"
ATTR_TODAY_TOTAL_GALLONS = "today_total_gallons"
