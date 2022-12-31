import glob
import os

from evernote.api.client import EvernoteClient
from evernote.edam.type.ttypes import Note


def create_note(note_store, title, body, guid):
    note = Note()

    note.title = title
    note.content = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    note.content += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
    note.content += f"<en-note>{body}</en-note>"
    note.notebookGuid = guid

    note_store.createNote(os.environ.get("ACCESS_TOKEN"), note)

client = EvernoteClient(
    token=os.environ.get("ACCESS_TOKEN"),
    sandbox=False
)

store = client.get_note_store()

filenames = glob.glob('text/private/*.txt')
filenames.sort()
for filename in reversed(filenames):
    title = filename.split("/")[-1].split(".")[0][3:]
    f = open(filename, 'r')
    body = f.read()
    f.close()
    title = title.replace(" ", "")
    title = title.replace("\n", "")
    if title == "":
        title = body.split("\n")[0]

    print(title)
    try:
        create_note(store, title, body, "")
    except:
        print(f"ERROR {title}")


