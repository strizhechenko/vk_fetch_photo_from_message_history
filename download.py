import os
from vk_requests import create_api
from urllib import urlretrieve

USER_LOGIN = os.environ.get('USER_LOGIN')
USER_PASSWORD = os.environ.get('USER_PASSWORD')
TARGET_USER_ID = os.environ.get('TARGET_USER_ID')

def make_api(login, password):
    return create_api(app_id=4171870, login=login,
                      password=password, scope=4096)


def get_urls(attachments):
    urls = []
    for attach in attachments:
        for item in attach:
            if item.get('photo'):
                photo = item.get('photo')
                max_size = max(int(k.split('_')[1])
                               for k in photo.keys() if k.startswith('photo_'))
                urls.append(photo.get("photo_%d" % (max_size,)))
    print 'got', len(urls), 'urls'
    return urls


def images_save(images, user_id):
    if not os.path.isdir(user_id):
        os.mkdir(user_id)
    total = len(images)
    for n, link in enumerate(images, 1):
        dst = "%s/%s.jpg" % (user_id, str(n).rjust(10, '0'))
        print "%d/%d" % (n, total)
        urlretrieve(link, dst)


def get_messages(api, user_id):
    count = api.messages.getHistory(user_id=user_id, count=0).get('count')
    result = list()
    for offset in range(0, count, 200):
        print 'load %d/%d', (offset, count)
        messages = api.messages.getHistory(user_id=user_id, count=0, offset=offset)
        attachments = [m.get('attachments') for m in messages.get('items') if m.get('attachments')]
        result.extend(attachments)
    print 'got', len(result), 'messages'
    return result


def main(user_id, api=None):
    api = api or make_api(USER_LOGIN, USER_PASSWORD)
    msgs = get_messages(api, user_id)
    images = get_urls(msgs)
    images_save(images, user_id)


if __name__ == '__main__':
    main(TARGET_USER_ID)
