from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/content_page')
def content_page():
    likes = get_likes(request.args.get('count_post'))
    users = get_user_data()

    return render_template('content_page.html', likes=likes, users=users)


def exec_api(method, params):
    init = {
        'access_token': '486a446f486a446f486a446fab481aa93b4486a486a446f16e569472a84f996a20a18c5',
        'v': 5.103,
        'owner_id': '-157243877'
    }
    init.update(params)

    return requests.get(f'https://api.vk.com/method/{method}', params=init).json()


def get_likes(count_post):
    id_like_dict = dict()
    likes_get_list = list()
    posts = exec_api('wall.get', {'count': count_post})['response']['items']
    for post in posts:
        likes_get_list.extend(exec_api('likes.getList', {'type': 'post', 'item_id': post['id']})['response']['items'])

    for id_user in likes_get_list:
        id_like_dict[id_user] = id_like_dict.get(id_user, 0) + 1

    list_users = list()

    list_keys = list(id_like_dict.keys())
    list_keys.sort()
    for i in list_keys:
        list_users.append(str(id_like_dict[i]) + ' ' + str(i))

    result = sorted(list_users)[::-1][:5]

    return result


def get_user_data():
    all_username = list()
    all_user_id = get_likes(request.args.get('count_post'))
    for user_ids in all_user_id:
        user_data = exec_api('users.get', {'user_ids': user_ids[1:]})['response']
        for first_last_name in user_data:
            all_username.append(first_last_name['first_name'] + ' ' + first_last_name['last_name'])

    return all_username


if __name__ == '__main__':
    app.run()
