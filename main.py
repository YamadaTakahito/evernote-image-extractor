import csv
import os

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec

NOTE_LIMIT = 250 # 一度に検索できるnotebookの数

# https://qiita.com/niwasawa/items/73f1a2b3c21dbd217b4c
client = EvernoteClient(
    token=os.environ.get("ACCESS_TOKEN"),
    sandbox=False
)

store = client.get_note_store()

notebook_list = store.listNotebooks()

for notebook in notebook_list:
    print(f"notebook name: {notebook.name}")
    os.makedirs(f"resources/{notebook.name}", exist_ok=True)
    csv_f = open(f"csv/{notebook.name}.csv", 'w')
    writer = csv.writer(csv_f)
    writer.writerow(["notebook", "note", "filepath", "mime", "created"])

    filter = NoteFilter()
    filter.notebookGuid = notebook.guid
    spec = NotesMetadataResultSpec()
    spec.includeTitle = True
    spec.includeCreated = True
    spec.includeAttributes = True

    offset = 0
    for _ in range(4):
        notes_metadata_list = store.findNotesMetadata(
            filter,
            offset,
            NOTE_LIMIT,
            spec)
        if len(notes_metadata_list.notes) <= 0:
            break

        for note_meta_data in notes_metadata_list.notes:
            note = store.getNote(note_meta_data.guid, False, True, False, False)

            if note.resources is None:
                continue

            os.makedirs(f"resources/{notebook.name}/{note.guid}", exist_ok=True)
            for idx, resource in enumerate(note.resources[:10]):
                if "image" in resource.mime or "video" in resource.mime:
                    filename = f"resources/{notebook.name}/{note.guid}/{note.title}_{idx}.tmp"
                    try:
                        f = open(filename, 'wb')
                        f.write(resource.data.body)
                        f.close()
                    except FileNotFoundError:
                        break
                    writer.writerow([notebook.name, note.title, filename, resource.mime, note.created])

        offset += NOTE_LIMIT

    csv_f.close()
