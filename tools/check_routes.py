import sys
from pathlib import Path
# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app

app = create_app()

with app.test_client() as client:
    for path in ['/', '/recipes', '/recipes/create', '/recipes/1']:
        print('\n=== REQUEST', path)
        try:
            resp = client.get(path)
            print('STATUS:', resp.status_code)
            print(resp.get_data(as_text=True)[:1000])
        except Exception as e:
            import traceback
            print('EXCEPTION during request to', path)
            traceback.print_exc()
            break
