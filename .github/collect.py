import json,os,sys,urllib.request,datetime
T=os.environ['GH_TOKEN']
def g(u):
    r=urllib.request.Request('https://api.github.com'+u,headers={'Authorization':'Bearer '+T,'Accept':'application/vnd.github+json'})
    with urllib.request.urlopen(r,timeout=30) as x: return json.load(x)
U={}
for n in ('LucaPRATA','langacorp'):
    d=g('/users/'+n);U[n]={k:d[k] for k in ('public_repos','followers','created_at')}
R=g('/orgs/langacorp/repos?type=public&sort=pushed&per_page=100')
K=('name','html_url','description','language','pushed_at','archived','fork')
data={'users':U,'repos':[{k:r.get(k) for k in K} for r in R],'repos_page_full':len(R)==100}
out=open(os.environ.get('GITHUB_OUTPUT','/dev/stdout'),'a')
try: old=json.load(open('data.json'))
except FileNotFoundError: old={}
now=datetime.datetime.now(datetime.timezone.utc)
prev=old.get('generated_at')
age_h=(now-datetime.datetime.fromisoformat(prev.replace('Z','+00:00'))).total_seconds()/3600 if prev else 1e9
if {k:old.get(k) for k in data}==data and age_h<20:
    print('unchanged, age',round(age_h,1),'h');out.write('changed=0\n');sys.exit(0)
data['generated_at']=now.strftime('%Y-%m-%dT%H:%M:%SZ')
with open('data.json','w') as f: json.dump(data,f,indent=1,sort_keys=True)
print('written',data['generated_at'],len(data['repos']),'repos');out.write('changed=1\n')
