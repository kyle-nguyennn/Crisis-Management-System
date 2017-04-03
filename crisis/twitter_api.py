import twitter


def post_on_twitter(message):
    """
    Post the given message on twitter

    :param message: The message to be tweeted
    :return: None
    """
    api = twitter.Api(consumer_key='tTVdIiKSNfNjCPZBxqoj8SmKz',
                      consumer_secret='OJmIkCOBf8oio31uCvIjKt1yjAPlLsIFlAjSHAz2NT6pY3ufJ8',
                      access_token_key='848440381591011329-7jT0wZAmOMbgwkCpDDeGzyWdvMFrdxJ',
                      access_token_secret='SS6JEUvZHc7zOiG8atc0RqLX44wAmKgq26hRssgis4ymF')
    api.PostUpdate(message)
