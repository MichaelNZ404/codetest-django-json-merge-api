import json

from django.shortcuts import render

def _makeTootTree():
    toots = json.load(open('data/toots.json'))
    authors = json.load(open('data/authors.json'))
    tags = json.load(open('data/tags.json'))
    taggings = json.load(open('data/taggings.json'))

    taggings = [tagging for tagging in taggings if tagging['tag_id'] is not None]
    for tagging in taggings:
        tagging['tag_name'] = [tag['name'] for tag in tags if tag['id'] == tagging['tag_id']][0]

    for toot in toots:
        toot['author'] = [author['name'] for author in authors if author['id'] == toot['author_id']][0]
        toot['tags'] = [(tagging['tag_id'], tagging['tag_name']) for tagging in taggings if tagging['toot_id'] == toot['id']]
    tree = []

    def find_children(parent_id):
        children = []
        for toot in toots:
            if toot['parent_id'] == parent_id:
                toot['children'] = find_children(toot['id'])
                children.append(toot)

        return children

    for x in toots:
        if x['parent_id'] is not None:
            pass
        else:
            x['children'] = find_children(x['id'])
            tree.append(x)
    return tree

def index(request):
    context = {'toot_list': _makeTootTree()}
    return render(request, 'toots/index.html', context)

def by_author(request, author_id):

    def check_author(toot):
        if toot['author_id'] == author_id:
            return True
        else:
            for x in toot['children']:
                if check_author(x):
                    return True
            return False

    toots = _makeTootTree()
    toots = [toot for toot in toots if check_author(toot)]

    context = {'toot_list': toots}
    return render(request, 'toots/index.html', context)

def by_tag(request, tag_id):
    def check_tag(toot):
        for tag in toot['tags']:
            if tag[0] == tag_id:
                return True
        else:
            for x in toot['children']:
                if check_tag(x):
                    return True
            return False

    toots = _makeTootTree()
    toots = [toot for toot in toots if check_tag(toot)]

    context = {'toot_list': toots}
    return render(request, 'toots/index.html', context)
