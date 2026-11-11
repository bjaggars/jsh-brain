# Placeholder music bed (synthesized here; swap for a licensed track): warm pad + soft pulse, 96 BPM, 25 s.
import numpy as np, wave
SR=48000; D=25.0; n=int(SR*D); t=np.arange(n)/SR; bpm=96; beat=60/bpm
def note(m): return 440*2**((m-69)/12)
chords=[[48,55,64,71],[45,52,60,67],[41,48,57,64],[43,50,59,65]]   # Cmaj7 Am7 Fmaj7 G7sus-ish
bar=beat*4; out=np.zeros(n)
for i in range(int(D/bar)+1):
    s=int(i*bar*SR); e=min(n,int((i+1)*bar*SR)+SR//2)
    if s>=n: break
    tt=np.arange(e-s)/SR; env=np.minimum(1,tt/0.6)*np.exp(-np.maximum(0,tt-bar)*4)
    for m in chords[i%4]:
        f=note(m+12); out[s:e]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.3*np.sin(2*np.pi*2*f*tt+0.3)+0.15*np.sin(2*np.pi*f*1.003*tt))
    f=note(chords[i%4][0]-12+12); out[s:e]+=0.07*env*np.sin(2*np.pi*f*tt)
for k in range(int(D/beat)):
    s=int(k*beat*SR); L=int(0.25*SR); tt=np.arange(L)/SR
    if s+L>n: break
    if k>=4: out[s:s+L]+=0.22*np.sin(2*np.pi*(55+70*np.exp(-tt*30))*tt)*np.exp(-tt*14)          # soft kick
    h=int((k+0.5)*beat*SR); L2=int(0.06*SR)
    if k>=8 and h+L2<n: out[h:h+L2]+=0.03*np.random.randn(L2)*np.exp(-np.arange(L2)/SR*60)          # shaker
fade=np.ones(n); fade[:SR]=np.linspace(0,1,SR); fade[-int(2.5*SR):]=np.linspace(1,0,int(2.5*SR))
out=out*fade; out=out/np.max(np.abs(out))*0.7
st=np.stack([out,np.roll(out,240)],1)
with wave.open('music.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
print('ok')
