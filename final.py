import Tkinter as tkinter
import MySQLdb as mysql
import pyglet
import os
import fnmatch


'''	while   player.playing == True:
		try:
			print '{0:.2f}\r'.format(player.time),
		except KeyboardInterrupt:
			print "ctrl-c"
			sys.exit("song paused")
			break   
'''			
mydb = mysql.connect(host='localhost',user='beni',passwd='password',db='project')
cur = mydb.cursor()
player = pyglet.media.Player()

def move():
	flag=0
	if listbox.get(0)=='TRACKS' or b.lower()=='tracks':
		for i in range(playbox.size()):
			if playbox.get(i)==v or v=='TRACKS':
				flag=1
				break
		if flag==0:
			playbox.insert('end',v)
	elif listbox.get(0)=='ALBUMS' or b.lower()=='albums':
		playbox.delete(0,'end')
		query = "select tracks.name from tracks,albums where tracks.albumid=albums.id and albums.name='%s'"%(v)
		cur.execute(query)
		res = cur.fetchall()
		for i in res:
			playbox.insert('end',i[0])
	elif b.lower()=='genre':
		playbox.delete(0,'end')
		query = "select tracks.name from tracks,genre where tracks.genreid=genre.id and genre.name='%s'"%(v)
		cur.execute(query)
		res = cur.fetchall()
		for i in res:
			playbox.insert('end',i[0])
	elif b.lower()=='artists':
		playbox.delete(0,'end')
		query="select tracks.name from tracks,albums,artists where artists.id=albums.artistid and albums.id=tracks.albumid and artists.name='%s'"%(v)
		cur.execute(query)
		res=cur.fetchall()
		for i in res:
			playbox.insert('end',i[0])		
			


def playinfo(event):
	global pmusic
	widget=event.widget
	items = widget.curselection()
	pmusic = widget.get(items[0])
	ftracks(pmusic)	

def play():
	global d	
	d = 'songs/'
	for i in os.listdir('songs'):
		if fnmatch.fnmatch(i.lower(),(pmusic+'*').lower()):
			d=d+i
			break	

	if not d == 'songs/':
	#	print d
		source = pyglet.media.load(d)
	#	print source
		player.queue(source)
		player.eos_action = player.EOS_LOOP
		player.play()
	#	print player.playing
	else:
		print "no song"

	
def pause():
	player.pause()

def nex():
	
	print pmusic,d
	player.pause()
	play()
	player.next()
	


def dartists():
	listbox.delete(0,'end')
	query = "select albums.name,albums.releasedate from albums,artists where artists.id=albums.artistid and artists.name='%s'"%(v)
	cur.execute(query)
	res = cur.fetchall()
	listbox.insert('end',"ALBUMS")
	listbox.itemconfig('end', {'bg':'red'}) 	
	for i in res:
		value = i[0]
		listbox.insert('end',value)

def dalbums():
	listbox.delete(0,'end')
	query = "select tracks.name from tracks,albums where tracks.albumid=albums.id and albums.name='%s'"%(v)
	cur.execute(query)
	res = cur.fetchall()
	listbox.insert('end',"TRACKS")
	listbox.itemconfig('end', {'bg':'red'}) 	
	for i in res:
		value = i[0]
		listbox.insert('end',value)

def dtracks():
	listbox.delete(0,'end')
	query = "select artists.name,albums.name,albums.releasedate,genre.name from artists,albums,genre,tracks where artists.id=albums.artistid and albums.id=tracks.albumid and genre.id=tracks.genreid and tracks.name='%s'"%(v)
	cur.execute(query)
	res = cur.fetchall()
	listbox.insert('end',"TRACK DETAILS")
	listbox.itemconfig('end', {'bg':'pink'}) 	
	listbox.insert('end','Track Name : '+v)
	for i in res:
		value = 'Artist : '+i[0]
		listbox.insert('end',value)
		value = 'Album : '+i[1]
		listbox.insert('end',value)
		value = 'Album Releasedate : '+str(i[2])
		listbox.insert('end',value)
		value = 'Genre : '+i[3]
		listbox.insert('end',value)

def ftracks(boom):
	listbox.delete(0,'end')
	query = "select artists.name,albums.name,albums.releasedate,genre.name from artists,albums,genre,tracks where artists.id=albums.artistid and albums.id=tracks.albumid and genre.id=tracks.genreid and tracks.name='%s'"%(boom)
	cur.execute(query)
	res = cur.fetchall()
	listbox.insert('end',"TRACK DETAILS")
	listbox.itemconfig('end', {'bg':'pink'}) 	
	listbox.insert('end','Track Name : '+boom)
	for i in res:
		value = 'Artist : '+i[0]
		listbox.insert('end',value)
		value = 'Album : '+i[1]
		listbox.insert('end',value)
		value = 'Album Releasedate : '+str(i[2])
		listbox.insert('end',value)
		value = 'Genre : '+i[3]
		listbox.insert('end',value)


def dgenre():
	listbox.delete(0,'end')
	query = "select tracks.name from tracks,genre where tracks.genreid = genre.id and genre.name='%s'"%(v)
	cur.execute(query)
	res = cur.fetchall()
	listbox.insert('end',"TRACKS")
	listbox.itemconfig('end', {'bg':'red'}) 	
	for i in res:
		value = i[0]
		listbox.insert('end',value)


def details():
	table = b.lower()
	global ca
	global cc
	global cg
	if table=='artists':
		cc=0
		cg=0
		if ca==1:
			dartists()
		elif ca==2:
			dalbums()
		elif ca==3:
			dtracks()
	elif table=='albums':
		ca=0
		cg=0
		if cc==1:
			dalbums()
		if cc==2:
			dtracks()
			cc=0
	elif table=='tracks':
		cc=0
		ca=0
		cg=0
		dtracks()
	elif table=='genre':
		cc=0
		ca=0
		if cg==1:
			dgenre()	
		if cg==2:
			dtracks()
			cg=0
def info(event):
	widget=event.widget
	items = widget.curselection()
	global v 
	v = widget.get(items[0])
	print b.lower(),v
	if b.lower()=='genre':
		if v=='TRACKS':
			genre()
		elif v=='TRACK DETAILS':
			temp = (listbox.get(1)).split(': ')[1]
			query = "select name from tracks where genreid=(select genreid from tracks where name = '%s')"%(temp)
			listbox.delete(0,'end')
			cur.execute(query)
			res = cur.fetchall()
			listbox.insert('end',"TRACKS")
			listbox.itemconfig('end', {'bg':'red'}) 	
			for i in res:
				value = i[0]
				listbox.insert('end',value)
	elif b.lower()=='albums':
		if v=='TRACKS':
			album()
		elif v=='TRACK DETAILS':
			temp = (listbox.get(1)).split(': ')[1]
			query = "select name from tracks where albumid=(select albumid from tracks where name = '%s')"%(temp)
			listbox.delete(0,'end')
			cur.execute(query)
			res = cur.fetchall()
			listbox.insert('end',"TRACKS")
			listbox.itemconfig('end', {'bg':'red'}) 	
			for i in res:
				value = i[0]
				listbox.insert('end',value)
	elif b.lower()=='tracks' and v=='TRACK DETAILS':
		listbox.delete(0,'end')
		cur.execute('select name from tracks')
		res=cur.fetchall()
		for i in res:
			value = i[0]
			listbox.insert('end',value)

	elif b.lower()=='artists':
		if v=='ALBUMS':
			artist()
		elif v=='TRACKS':
			temp = listbox.get(1)
			highlight="(select albums.name from albums where albums.id=(select albumid from tracks where name like '%s'))"%(temp)
			cur.execute(highlight)
			hres=cur.fetchall()
			hval=hres[0][0]
			query = " select albums.name from albums where albums.artistid=(select albums.artistid from albums where albums.id= (select albums.id from albums where albums.id=(select albumid from tracks where name like '%s')))"%(temp)
			listbox.delete(0,'end')
			cur.execute(query)
			res = cur.fetchall()
			listbox.insert('end',"ALBUMS")
			listbox.itemconfig('end', {'bg':'red'}) 	
			for i in res:
				value = i[0]
				listbox.insert('end',value)
				if value==hval:
					listbox.selection_set('end')
		elif v=='TRACK DETAILS':
			temp = (listbox.get(1)).split(': ')[1]
			query = "select name from tracks where albumid=(select albumid from tracks where name = '%s')"%(temp)
			listbox.delete(0,'end')
			cur.execute(query)
			res = cur.fetchall()
			listbox.insert('end',"TRACKS")
			listbox.itemconfig('end', {'bg':'red'}) 	
			for i in res:
				value = i[0]
				listbox.insert('end',value)


				
				
	global cc,cg,ca
	if ca>3:
		ca=1
	if cc>2:
		cc=1
	if cg>2:
		cg=1
	cc=cc+1
	cg=cg+1
	ca=ca+1
	#print ca,cc,cg,v
	
	
def artist():
	global b  
	global ca
	ca=0
	b = button1.config('text')[-1]
	listbox.delete(0,'end')
	value = entry.get()
	query = "select *from artists where name like '"+value+"%'"
	cur.execute(query)
	res= cur.fetchall()
	for i in res:
		value = i[1]
		listbox.insert('end',value)
	entry.delete(0,'end')

def album():
	global b  
	global cc
	cc=0
	b = button2.config('text')[-1]
	listbox.delete(0,'end')
	value = entry.get()
	query = "select *from albums where name like '"+value+"%'"
	cur.execute(query)
	res= cur.fetchall()
	for i in res:
		value = i[2]
		listbox.insert('end',value)
	entry.delete(0,'end')

def track():
	global b  
	b = button3.config('text')[-1]
	listbox.delete(0,'end')
	value = entry.get()
	length = len(value)
	if length<=2:
		query = "select *from tracks where name like '"+value+"%'"
	elif length>2:
		query="SELECT * FROM tracks  WHERE tracks.name REGEXP '[[:<:]]%s[[:>:]]'"%(value)	
	cur.execute(query)
	res= cur.fetchall()
	for i in res:
		value = i[2]
		listbox.insert('end',value)
	entry.delete(0,'end')


def genre():
	global b  
	global cg
	cg=0
	b = button4.config('text')[-1]
	listbox.delete(0,'end')
	value = entry.get()
	query = "select *from genre where name like '%"+value+"%'"
	cur.execute(query)
	res= cur.fetchall()
	for i in res:
		value = i[1]
		listbox.insert('end',value)
	entry.delete(0,'end')

root = tkinter.Tk()
BG='light blue'
BUT='grey'
FG='white'

ca=0
cc=0
cg=0
root.title("DBMS Music Player")
root.geometry("1100x350+200+200")
root.config(bg=BG)
frame1 = tkinter.Frame(root,bg=BG)
label = tkinter.Label(frame1,text='Search:',bg=BUT,fg=FG)
entry = tkinter.Entry(frame1)
label.pack(side='left',anchor='w',pady=4,padx=2)
entry.pack(pady=4)
frame1.pack(pady=12)

frame2= tkinter.Frame(root,bg=BG)
button1 = tkinter.Button(frame2,text='Artists',command=artist,bg=BUT,fg=FG)
button1.pack(side='left',padx=2)
button2 = tkinter.Button(frame2,text='Albums',command=album,bg=BUT,fg=FG)
button2.pack(side='left',padx=2)
button3 = tkinter.Button(frame2,text='Tracks',command=track,bg=BUT,fg=FG)
button3.pack(side='left',padx=2)
button4 = tkinter.Button(frame2,text='Genre',command=genre,bg=BUT,fg=FG)
button4.pack(side='left',padx=2)
frame2.pack()

frame3= tkinter.Frame(root,bg=BG,bd=2,relief='sunken')
listbox = tkinter.Listbox(frame3,width=50,height=10)
listbox.pack(pady=12,padx=2,side='left')
listbox.bind("<<ListboxSelect>>",info)

playbox = tkinter.Listbox(frame3,width=50,height=10)
playbox.pack(pady=12,padx=2,side='right')
playbox.bind("<<ListboxSelect>>",playinfo)
button5 = tkinter.Button(frame3,text='Details',command=details,bg=BUT,fg=FG)
button5.pack(padx=2,side='left')
button6 = tkinter.Button(frame3,text='Move',command=move,bg=BUT,fg=FG)
button6.pack(padx=2,side='right')
frame3.pack(pady=2,padx=2)

frame4 = tkinter.Frame(root,bg=BG,bd=2)
playbutton = tkinter.Button(frame4,text='Play',command=play)
playbutton.pack(padx=2,side='left')
pausebutton = tkinter.Button(frame4,text='Pause',command=pause)
pausebutton.pack(padx=2,side='left')
nextbutton = tkinter.Button(frame4,text='Next',command=nex)
nextbutton.pack(padx=2,side='left')

#progress = ttk.Progressbar(frame3,orient='horizontal',mode='determinate')
#progress.pack()
frame4.pack(pady=2,padx=2,side='bottom')


root.mainloop() 
