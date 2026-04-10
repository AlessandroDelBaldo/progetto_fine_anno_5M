import os
p = r'C:\Users\Utente\progetto_fine_anno_5M\video-app\instance\board_games.sqlite'
try:
    if os.path.exists(p):
        os.remove(p)
        print('DELETED')
    else:
        print('NOT FOUND')
except Exception as e:
    import traceback
    print('ERROR')
    traceback.print_exc()
