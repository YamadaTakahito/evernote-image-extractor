import gkeepapi

def save_file(title, text):
    f = open(f"text/{title}.txt", 'w')
    f.write(text)
    f.close()


src_keep = gkeepapi.Keep()
src_success = src_keep.login('', '')

src_gnotes = src_keep.all()
for src_gnote in src_gnotes:
    save_file(src_gnote.title, src_gnote.text)
