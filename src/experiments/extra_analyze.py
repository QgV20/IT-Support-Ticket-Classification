# Phan tich bo sung tren du lieu va ket qua san co cua repo.
# Chay tu thu muc goc cua repo:  python phan_tich_bo_sung.py
import json, numpy as np, pandas as pd, joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score
ROOT=Path("."); DATA,RES=ROOT/"data",ROOT/"results"
OUT=Path("extra_out"); OUT.mkdir(exist_ok=True)
train=pd.read_csv(DATA/"train.csv"); test=pd.read_csv(DATA/"test.csv")
c=pd.read_csv(RES/"baseline_llm_comparison_400.csv")
sm=pd.read_csv(DATA/"test_sample.csv"); assert (c.Topic_group.values==sm.Topic_group.values).all(); c["Document"]=sm.Document.values  # hai tep cung thu tu
c["lp"]=c.llm_prediction.fillna("__ERROR__")
labs=sorted(c.Topic_group.unique()); R={}
mf=lambda y,p: f1_score(y,p,labels=labs,average="macro",zero_division=0)
y=c.Topic_group.values; pb=c.baseline_prediction.values; pl=c.lp.values
# 1. Bootstrap + McNemar
rng=np.random.default_rng(42); n=len(c); B=10000
A=np.zeros((B,2)); F=np.zeros((B,2))
for i in range(B):
    ix=rng.integers(0,n,n); A[i]=[(pb[ix]==y[ix]).mean(),(pl[ix]==y[ix]).mean()]
    F[i]=[mf(y[ix],pb[ix]),mf(y[ix],pl[ix])]
q=lambda a:[round(float(np.percentile(a,2.5)),4),round(float(np.percentile(a,97.5)),4)]
R["boot_acc_base"]=q(A[:,0]);R["boot_acc_llm"]=q(A[:,1]);R["boot_f1_base"]=q(F[:,0]);R["boot_f1_llm"]=q(F[:,1])
R["boot_acc_diff"]=q(A[:,0]-A[:,1]);R["boot_f1_diff"]=q(F[:,0]-F[:,1])
b=int(((pb==y)&(pl!=y)).sum()); d=int(((pb!=y)&(pl==y)).sum())
from scipy.stats import chi2, binomtest
R["mcnemar_b"]=b;R["mcnemar_c"]=d
R["mcnemar_chi2"]=round((abs(b-d)-1)**2/(b+d),2); R["mcnemar_p_exact"]=float(binomtest(min(b,d),b+d,0.5).pvalue)
# 2. Do dai phieu
c["words"]=c.Document.str.split().str.len()
bins=[0,10,20,40,80,10**6]; names=["<=10","11-20","21-40","41-80",">80"]
c["bin"]=pd.cut(c.words,bins=bins,labels=names)
g=c.groupby("bin",observed=True).apply(lambda s:pd.Series({"n":len(s),"acc_base":(s.baseline_prediction==s.Topic_group).mean(),"acc_llm":(s.lp==s.Topic_group).mean()}))
g.to_csv(OUT/"len_bins.csv"); R["len_bins"]=g.round(4).reset_index().to_dict("records")
R["len_corr_base"]=round(float(np.corrcoef(c.words,(pb==y))[0,1]),3);R["len_corr_llm"]=round(float(np.corrcoef(c.words,(pl==y))[0,1]),3)
# 3. Duong cong hoc Baseline
sizes=[200,500,1000,2000,5000,10000,20000,len(train)]; rows=[]
for s in sizes:
    for seed in (0,1,2):
        sub=train.sample(n=s,random_state=seed) if s<len(train) else train
        if s==len(train) and seed>0: continue
        m=Pipeline([("tfidf",TfidfVectorizer(ngram_range=(1,2),min_df=2 if s>=1000 else 1,max_features=50000,sublinear_tf=True)),("clf",LogisticRegression(max_iter=1000,class_weight="balanced"))])
        m.fit(sub.Document,sub.Topic_group); p=m.predict(test.Document)
        rows.append((s,seed,accuracy_score(test.Topic_group,p),f1_score(test.Topic_group,p,average="macro")))
lc=pd.DataFrame(rows,columns=["n","seed","acc","mf1"]); lcs=lc.groupby("n").agg(acc=("acc","mean"),acc_sd=("acc","std"),mf1=("mf1","mean")).reset_index()
lcs.to_csv(OUT/"learning_curve.csv",index=False); R["learning_curve"]=lcs.round(4).to_dict("records")
# 4. Chuyen phieu theo do tin cay
m=joblib.load(RES/"baseline_tfidf_lr.joblib")
Pt=m.predict_proba(test.Document); conf_t=Pt.max(1); pt=m.classes_[Pt.argmax(1)]; ok_t=(pt==test.Topic_group.values)
th=[0.3,0.4,0.5,0.6,0.7,0.8,0.9]; cov=[]
for t in th:
    k=conf_t>=t; cov.append({"t":t,"coverage":round(float(k.mean()),4),"acc_covered":round(float(ok_t[k].mean()),4),"acc_rest":round(float(ok_t[~k].mean()),4) if (~k).any() else None})
R["conf_test_full"]=cov
Pc=m.predict_proba(c.Document); conf=Pc.max(1); R["conf_mean_correct"]=round(float(conf[pb==y].mean()),3);R["conf_mean_wrong"]=round(float(conf[pb!=y].mean()),3)
casc=[]
for t in th:
    k=conf>=t; comb=np.where(k,pb,pl); casc.append({"t":t,"to_llm":int((~k).sum()),"acc_base_on_rest":round(float((pb[~k]==y[~k]).mean()),4) if (~k).any() else None,"acc_llm_on_rest":round(float((pl[~k]==y[~k]).mean()),4) if (~k).any() else None,"acc_cascade":round(float((comb==y).mean()),4)})
R["cascade"]=casc
# 5. Vi du loi
ex=c[(c.Topic_group!=c.baseline_prediction)|(c.Topic_group!=c.lp)].copy(); ex["words"]=ex.Document.str.split().str.len()
def pick(df,k): return df.head(k)
sets={"chi_llm_dung":c[(pb!=y)&(pl==y)],"cung_sai_cung_nhan":c[(pb!=y)&(pl!=y)&(pb==pl)],"chi_llm_sai_admin":c[(pb==y)&(pl!=y)&(y=="Administrative rights")],"chi_llm_sai_hw":c[(pb==y)&(pl!=y)&(y=="Hardware")],"chi_llm_sai_hr":c[(pb==y)&(pl!=y)&(y=="HR Support")]}
ex_rows=[]
for k,df in sets.items():
    for _,r in df[df.words<=45].head(2).iterrows():
        ex_rows.append({"nhom":k,"that":r.Topic_group,"base":r.baseline_prediction,"llm":r.lp,"doc":r.Document[:230]})
pd.DataFrame(ex_rows).to_csv(OUT/"examples.csv",index=False)
json.dump(R,open(OUT/"results.json","w"),ensure_ascii=False,indent=1,default=str)
print(json.dumps({k:v for k,v in R.items() if k not in("learning_curve",)},ensure_ascii=False,indent=1,default=str))
print(lcs.to_string())