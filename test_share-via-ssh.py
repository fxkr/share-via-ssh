import datetime
import imp


# "share-via-ssh" is not a valid module name, so we can't use "import"
share_via_ssh = imp.load_source('share_via_ssh', 'share-via-ssh')
parse_expiration = share_via_ssh.parse_expiration


def test_parse_expiration():
    now = datetime.datetime(2001, 2, 3, 11, 22, 33)

    assert None == parse_expiration("never")
    assert None == parse_expiration("none")
    assert None == parse_expiration("")

    assert datetime.datetime(2001, 2, 3, 11, 22, 33) == parse_expiration("now", now)
    assert datetime.datetime(2001, 2, 3, 23, 59, 59) == parse_expiration("today", now)
    assert datetime.datetime(2001, 2, 4, 23, 59, 59) == parse_expiration("tomorrow", now)

    assert datetime.datetime(2001, 2, 4, 11, 22, 33) == parse_expiration("20010204112233")
    assert datetime.datetime(2001, 2, 4, 11, 22, 33) == parse_expiration("2001-02-04 11:22:33")
    assert datetime.datetime(2001, 2, 4, 11, 22, 00) == parse_expiration("2001-02-04 11:22")
    assert datetime.datetime(2001, 2, 4, 11, 00, 00) == parse_expiration("2001-02-04 11")
    assert datetime.datetime(2001, 2, 4, 00, 00, 00) == parse_expiration("2001-02-04")
    assert datetime.datetime(2001, 2, 1, 00, 00, 00) == parse_expiration("2001-02")
    assert datetime.datetime(2001, 1, 1, 00, 00, 00) == parse_expiration("2001")
    assert datetime.datetime(2001, 2, 3, 17, 18, 19) == parse_expiration("17:18:19", now)
    assert datetime.datetime(2001, 2, 3, 17, 18, 00) == parse_expiration("17:18", now)
    assert datetime.datetime(2001, 2, 3, 17, 00, 00) == parse_expiration("17", now)

    assert datetime.datetime(2001, 2, 3, 11, 22, 33) == parse_expiration("0s", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59s", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59sec", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59secs", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59second", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59seconds", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59 s", now)
    assert datetime.datetime(2001, 2, 3, 11, 23, 32) == parse_expiration("59 seconds", now)

    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2m", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2min", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2mins", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2minute", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2minutes", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2 m", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2 min", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2 mins", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2 minute", now)
    assert datetime.datetime(2001, 2, 3, 11, 24, 33) == parse_expiration("2 minutes", now)

    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20h", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20hr", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20hrs", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20hour", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20hours", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20 h", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20 hr", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20 hrs", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20 hour", now)
    assert datetime.datetime(2001, 2, 4, 7, 22, 33) == parse_expiration("20 hours", now)

    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4w", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4wk", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4wks", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4week", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4weeks", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4 w", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4 wk", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4 wks", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4 week", now)
    assert datetime.datetime(2001, 3, 3, 11, 22, 33) == parse_expiration("4 weeks", now)

    try:
        parse_expiration("bad date")
    except ValueError:
        pass
    else:
        assert False

