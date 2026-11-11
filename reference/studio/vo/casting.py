import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k = Kokoro('models/kokoro-v1.0.onnx', 'models/voices-v1.0.bin')
line = "You didn't become a real estate agent to babysit software. Meet My Realty Vault."
parts = []
for i, (v, sp) in enumerate([('af_heart', 1.05), ('am_michael', 1.05), ('af_bella', 1.05), ('am_fenrir', 1.05)]):
    a, sr = k.create(line, voice=v, speed=sp, lang='en-us'); parts += [a, np.zeros(int(sr * 0.9))]
    print(i + 1, v)
sf.write('out/MRV_Voice_Casting_4_options.wav', np.concatenate(parts), sr)
