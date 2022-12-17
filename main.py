from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

client = EvernoteClient(
    token='YOUR_AUTH_ACCESS_TOKEN',
    sandbox=False
)

store = client.get_note_store()

notebook_list = store.listNotebooks()
