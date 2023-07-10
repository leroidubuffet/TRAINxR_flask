import gspread
from utils import map_ethnicity
import pandas as pd
import gspread
from datetime import datetime

credentials = {
  "type": "service_account",
  "project_id": "tidy-gravity-349514",
  "private_key_id": "2d2d47fb47ddfb4ec6c2fa7beacdd8fe785f998e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC0Bg21E6axY3fb\nww1iZnNG7zEc0D6Wy3lqsCSgQBnyb6PQcuMfAwK+4ZPDWh0dyGJ3nE6lHnn/IBrg\nsIFxBbUh5oZOwfaN1A9GU2/QDNiUNeJ3i7ba4mN1URqUpixQZFXYJ3jGN1bNJevl\npfkXXMx+9o0qXN5ZHKLso7K36WFZZdzRcWVDtyQskmE6kyVGUAQak/dWY0ZVMYFG\nsa/qnxvfRz57LrowzDFaenv0yp6/6vL5jyACoO/7BuJu36l43QLpDj9dC8dnlgO0\nZt05TjikSEzi/FnGQrK6BBYIZUdwxGqvFMyehbp/KV0YN1d9tvYnc80uSSkUzsYD\n283z6GD1AgMBAAECggEAA44gDKyp7NRkTFJ+i+wuiB7WpzVEmylDCVSXsJN7f7Jt\nN4NhUV43mmnth1za+NjZeve7BN9EdQGfDkNmFwOQF26MRfdmJVhkAdVJfsAWMd0b\njxVTA+EXKjyzC+75LpBAsr9azv1OSUhfr34W3HuAbVx0nrrNSFC8tfQopiGlgsSr\n4MqrHdR+qXaWHof1H4ypYVY8uWSd5bXXJ/H4joNcpyIQ2KyJSpAmhuXEDAu6eaKA\nNwM6w43ModnaP+pWtAoiVSTlnsy5Eaw2c0zCrfqXq83Zft0uZMPRU5IWpYBArV4C\neF7znLal8fyNyAeMbjFQbOq6Xwxm2C+WFUedDUAl+QKBgQD7rcjdFxpCcm7Llsso\nqOIDaKmoXF3dzANciUULJleu1Z+uwXd5caRpStRrgIONZeEqqCHDSLVaU4QHg4nN\nOUA38NBcN4Q/G87n/9Fw+D9AbbYDKTrPFDFgN/KcyyXLnlfY6oNBXeaqhTiIxokD\nHV1m7Xt2monPr5ixt2k9w9maqQKBgQC3HVHQ0NysVHifD7bYw0BsmBRUF/gyhZKm\nvE+3HZnTTNzSlUt1vKUePflyc26S4xFHczZR1zs1/UJztvNusUeRNQTrKv/3xpqg\n+COxb6Kx6pzo6SSjFbdOYFxMEv0WU/HeMODdQahggL1/TIW9T1cc89IB3WwyQ3Nx\nPZ+L0EivbQKBgBB2ksAbpcUY9TRuHcYAHiC49PglaqJ6mPGxrQmIrY2rPbHRx/3y\nuB2HHpQVqQVT18HRk7vRgsNw2R8gtJ/vEctW/lo563WxXPyCGHI6WvDc/F4CkW1A\nVeaEYmNtSoCiT/7JgGKDQPaAlm0kB4xjnFuCR2Q/waoLQ4LEi6bVq+NZAoGAOEOZ\nBQl4FLdrzKv+acIsxHFCJcirqZJjSjooYEKHJmbCny3iXs3VCmLOh70yJ43/nC2p\nbiIs/lzQE1AOol90dwiMd1niBpcOohE8nmOH4RUOm34vlLCyfzGaioF3JGossjHg\nlft7qhNEpp2zpkR/ptTAHXSUrykMiqn9oO8htk0CgYBA3yB9DeatlSe9c3yUhzhe\nBeDEaOtXF7Mu/mR/AEzF4+UMI4g9syIQ40M3uEedBdgw2tmO2+HRl8n8giacLzok\nQJN3AE7zIxaRg4XwZ5XdoYtEgaEHHOA0iQv4uFtOwzyrRnJUHCw8lKcl238Cj1ek\nM7UmX5im0Vs7sDU5KDcv+g==\n-----END PRIVATE KEY-----\n",
  "client_email": "eys-445@tidy-gravity-349514.iam.gserviceaccount.com",
  "client_id": "106310523143023000697",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/eys-445%40tidy-gravity-349514.iam.gserviceaccount.com"
}

# Google Sheets setup
gc = gspread.service_account_from_dict(credentials)
gs = gc.open("ABLExR-DATA")		# open document
wk_rt = gs.get_worksheet(0) 	# reaction time spreadsheet
wk_s = gs.get_worksheet(1) 		# session spreadsheet
wk_f = gs.get_worksheet(2) 		# feedback spreadsheet

def get_last_added_wk(gs):
	worksheets = gs.worksheets()    
	if worksheets:
		return worksheets[-1]
	else:
		return None

def get_wk_by_name(name):
	try:
		return gs.worksheet(name)
	except gspread.exceptions.WorksheetNotFound:
		return None
	
def create_session_wk(id):
	wk = gs.add_worksheet(str(id), 0, 4)
	wk.append_row(["session_id", "ethnicity", "reaction_t", "timeStamp"])
	return wk

def delete_wk(name):
	wk = get_wk_by_name(name)
	if wk is not None:
		gs.del_worksheet(wk)

def get_rt_data():
	records = wk_rt.get_all_records()
	if records:
		return pd.DataFrame(records)
	else:
		return pd.DataFrame(columns=['session_id', 'ethnicity', 'reaction_t', 'timeStamp'])

def get_s_data():
	records = wk_s.get_all_records()
	if records:
		return pd.DataFrame(records)
	else:
		return pd.DataFrame(columns=['session_id', 'ethnicity', 'description'])

def get_f_data():
	records = wk_f.get_all_records()
	if records:
		return pd.DataFrame(records)
	else:
		return pd.DataFrame(columns=['session_id', 'ethnicity', 'feedback'])

df_rt = get_rt_data()
df_s = get_s_data()
df_f = get_f_data()

def add_record(session_id, reaction_t):
	session_id = str(session_id)  # Convert session_id to string
	ethnicity = int(session_id[0])
	id = int(session_id[1:])  # Extract digits 1 to 3 from session_id
	now = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
	record = [id, ethnicity, reaction_t, now]
	
	# Get the worksheet for this session
	wk = get_wk_by_name(session_id)
	
	# If the worksheet doesn't exist, create it
	if wk is None:
		wk = create_session_wk(session_id)
	
	# Add the record to the worksheet
	wk.append_row(record)

def add_session(session_id, session_description):
	ethnicity_code = int(session_id[0])
	ethnicity = map_ethnicity(ethnicity_code)
	print("add_session id: ", session_id) # DEBUG
	record = [session_id, ethnicity, session_description]
	wk_s.append_row(record, value_input_option='USER_ENTERED')

def add_feedback(session_id, feedback):
	try:
		session_id = str(session_id)
		ethnicity = int(session_id[0])
		id = int(session_id[1:])
		record = [id, ethnicity, feedback]
		wk_f.append_row(record, value_input_option='USER_ENTERED')
	except Exception as e:
		app.logger.error('Error when adding feedback: %s', e)