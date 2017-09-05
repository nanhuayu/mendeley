# codings=utf8

import os, sys
from mendeley import Mendeley
from mendeley.session import MendeleySession


with open('config','r',encoding='utf8') as f:
    tmp_str = f.read() 
if not tmp_str: tmp_str = 'None'
config = eval(tmp_str)

with open('session','r',encoding='utf8') as f:
    tmp_str = f.read()
if not tmp_str: tmp_str = 'None'
session_state = eval(tmp_str)

mendeley = Mendeley(config['Id'], config['Secret'], config['REDIRECT_URI'])


def get_session():
    auth = mendeley.start_authorization_code_flow()
    os.startfile(auth.get_login_url())
    auth_response = input()
    session = auth.authenticate(auth_response)

    session_state = {'state':auth.state,'auth_response':auth_response,'token':session.token}

    with open('session','w',encoding='utf8') as f:
        f.write(str(session_state))

def get_session_from_state():
    auth = mendeley.start_authorization_code_flow(session_state['state'])
    session = auth.authenticate(session_state['auth_response'])

    session_state['token'] = session_state.token

    with open('session','w',encoding='utf8') as f:
        f.write(str(session_state))

def get_session_from_cookies():
    return MendeleySession(mendeley, session_state['token'])

if not session_state: session = get_session()
else:
    #if not session_state['token']: session = get_session_from_state()
    try:session = get_session_from_cookies()
    except:session = get_session_from_state()


print(session.profiles.me.display_name)


# dir(new)
# abstract, add_note, attach_file, authors, content_type, created, delete, 
# files, group, id, identifiers, keywords, last_modified, move_to_trash, 
# profile, source, title, type, update, year

# dir(tmp)
# abstract, authors, content_type, files, id, identifiers, keywords,
# link, source, title, type, year


# pages : session.documents.list()
def list_doc():
    a = [i for i in session.documents.iter()]
    

# get by id : session.documents.get(id)
def search_doc(doi_str):
    return session.catalog.by_identifier(doi=doi_str)

def create_doc(tmp):
    return session.documents.create(tmp.title,tmp.type,identifiers=tmp.identifiers,
                                abstract=tmp.abstract, authors=tmp.authors,
                                source=tmp.source, keywords=tmp.keywords,
                                id=tmp.id, link=tmp.link, year=tmp.year)


def update_doc(new, tmp):
    return new.update(title=tmp.title, abstract=tmp.abstract, authors=tmp.authors,
           identifiers=tmp.identifiers,source=tmp.source, keywords=tmp.keywords,
           id=tmp.id, link=tmp.link, year=tmp.year)


#print (session.catalog.by_identifier(doi='10.1371/journal.pmed.0020124', view='stats').reader_count)

if __name__ == "__main__":
    doc_str = sys.argv[1]
    print(doc_str)
    a = search_doc(doc_str.replace('@','/'))
    print(a.title)
