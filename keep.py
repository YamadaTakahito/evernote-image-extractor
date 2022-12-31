import gkeepapi

def save_file(title, text, time):
    f = open(f"text/private/{title}.txt", 'w')
    f.write(time + "\n" + text)
    f.close()


src_keep = gkeepapi.Keep()
src_success = src_keep.login('', '')

src_gnotes = src_keep.all()
for idx, src_gnote in enumerate(src_gnotes):
    save_file(str(idx).zfill(3) + src_gnote.title, src_gnote.text, src_gnote.timestamps.created.strftime('%Y-%m-%d %H:%M:%S'))
