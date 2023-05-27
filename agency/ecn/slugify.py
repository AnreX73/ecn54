from random import randint


def words_to_slug(words):
    slug_dict = ['a', 'b', 'v', 'g', 'd', 'e', 'zh',
                 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p',
                 'r', 's', 't', 'u', 'f', 'h', 'c', 'ch', 'sh',
                 'shch', '', 'y', '', 'e', 'yu', 'ya'
                 ]

    start_index = ord('а')
    slug = ''
    for w in words.lower():
        if 'а' <= w <= 'я':
            slug += slug_dict[ord(w) - start_index]
        elif w == 'ё':
            slug += 'yo'
        elif w in " !?;:.,":
            slug += '-'
        elif w in '"' :
            slug += '-'
        else:
            slug += w
    while slug.count('--'):
        slug = slug.replace('--', '-')
    suffix1 = chr(randint(97,122))
    suffix2 = chr(randint(97,122))
    slug = slug + suffix1 + suffix2
    return slug




