from xgboost import XGBClassifier
from time import time
from datetime import datetime as dt
import librosa as lr
import pandas as pd
import os
import soundfile as sf
import shutil


def extract_features(y, len_, part=50, sr=44100):
    '''
        import pandas as pd
        import librosa as lr
        from time import time
    '''
    df = pd.DataFrame()
    time_ = time()
    for j in range(part): 
        x = y[len_*j:len_*(j+1)]

        print('____________------________________________________')

        chromagram = lr.feature.chroma_stft(x, sr=sr, hop_length=512)
        df.loc[j, 'chroma_stft_mean'] = chromagram.mean()
        df.loc[j, 'chroma_stft_var'] = chromagram.var()
        print('##', end='')

        rms = lr.feature.rms(y=x)
        df.loc[j, 'rms_mean'] = rms.mean()
        df.loc[j, 'rms_var'] = rms.var()
        print('##', end='')

        spectral_centroid = lr.feature.spectral_centroid(x, sr=sr)[0]
        df.loc[j, 'spectral_centroid_mean'] = spectral_centroid.mean()
        df.loc[j, 'spectral_centroid_var'] = spectral_centroid.var()
        print('##', end='')

        spectral_bandwidth = lr.feature.spectral_bandwidth(x, sr=sr)[0]
        df.loc[j, 'spectral_bandwidth_mean'] = spectral_bandwidth.mean()
        df.loc[j, 'spectral_bandwidth_var'] = spectral_bandwidth.var()
        print('##', end='')

        rolloff = lr.feature.spectral_rolloff(x, sr=sr)
        df.loc[j, 'rolloff_mean'] = rolloff.mean()
        df.loc[j, 'rolloff_var'] = rolloff.var()
        print('##', end='')

        zero_crossing_rate = lr.feature.zero_crossing_rate(x)
        df.loc[j, 'zero_crossing_rate_mean'] = zero_crossing_rate.mean()
        df.loc[j, 'zero_crossing_rate_var'] = zero_crossing_rate.var()
        print('##', end='')

        y_harm, y_perc = lr.effects.hpss(x)
        df.loc[j, 'harmony_mean'] = y_harm.mean()
        df.loc[j, 'harmony_var'] = y_harm.var()

        df.loc[j, 'perceptr_mean'] = y_perc.mean()
        df.loc[j, 'perceptr_var'] = y_perc.var()
        print('######', end='')

        tempo, _ = lr.beat.beat_track(x, sr=sr)
        df.loc[j, 'tempo'] = tempo
        print('##', end='')

        for k in range(20):
            mfccs = lr.feature.mfcc(x, sr=sr)[k]
            df.loc[j, f'mfcc{k+1}_mean'] = mfccs.mean()
            df.loc[j, f'mfcc{k+1}_var'] = mfccs.var()
            print('##', end='')

        print(f'Complete wav {j}', ' //// ', f'{(time()-time_)/60:.2f} (min)')
    return df


def trim_audio_data(audio_file, save_file=None):
    '''
        import soundfile as sf
    '''
    sr = 44100; sec = 150
    if audio_file[-4:]!='.mp3' and audio_file[-4:]!='.wav': 
        os.rename(audio_file, audio_file+'.mp3')
        y, sr = lr.load(audio_file+'.mp3', sr=sr)
    else:
        y, sr = lr.load(audio_file, sr=sr)
    
    if save_file!=None: sf.write(save_file + '.wav', y, sr, 'PCM_24')
    elif save_file==None: ny = y[:sr*sec]; return ny, sr


def get_file(audio_path='./audio', wav=None):
    '''
        from datetime import datetime as dt
        import shutil
        import os
    '''
    wav_path = audio_path + '/__wav{0}'.format(dt.now().strftime('_%Y%m%d_%H%M'))

    if not os.path.exists(wav_path):        # if directory('wav') doesn't exist
        os.makedirs(wav_path)               # Make directory('wav')
    
    if wav==None: audio_list = [i for i in os.listdir(audio_path) if i[:5]!='__wav']
    elif wav!=None: audio_list = [wav]

    print(audio_list)

    for audio_name in audio_list: 
        print(audio_name)

        audio_file = audio_path + '/' + audio_name
        wav_file = wav_path + '/' + audio_name[:-4]

        if audio_name.find('.wav') == -1:       # file is not WAV
            print(wav_file,'<< wav_file_name')
            trim_audio_data(audio_file, wav_file)
        elif audio_name.find('.wav') != -1:     # file is WAV
            if os.path.exists(wav_path):        # if directory('wav') is already exist
                shutil.move(audio_file, wav_file+'.wav')   # Move audio_file into directory('./wav')
        
    return os.listdir(wav_path), wav_path


def predict_all_genre(model, path='./audio'):
    '''
        from xgboost import XGBClassifier
        from time import time
        import librosa as lr
        import pandas as pd
        import os
    '''    
    kind_of_genre = ['bass', 'chill', 'drumstep', 'drum_and_bass', 'dubstep', 'edm', 
                    'electronic', 'future_house', 'hardstyle', 'house', 'indie', 
                    'melodic_dubstep', 'trap']
    new_xgb_model = XGBClassifier()
    new_xgb_model.load_model(model); print('Model Conn Complete////')

    wav_list, wav_path = get_file(path); print('File\'s Ready to Use....')

    sec = 3
    list_ = []
    for wav in wav_list:
        y, sr = trim_audio_data(wav_path+'/'+wav)
        len_ = sec*sr

        df = extract_features(y, len_)

        predict_result_list = list(new_xgb_model.predict(df)); print('Predict is on processing....')

        print(predict_result_list)
    
        dict_ = {}
        for i in kind_of_genre: dict_[i] = predict_result_list.count(i)
        
        sorted_dict = sorted(dict_.items(), key = lambda item: item[1], reverse = True)[:2]

        if sorted_dict[0][1]==sorted_dict[1][1]: list_.append([sorted_dict[0][1], sorted_dict[1][1]]) 
        else: list_.append(sorted_dict[0][0])

    for i in os.listdir(path):      # Remove every audio files in directory(path) After Predict process is done
        if i[-4]=='.': os.remove(path+'/'+i)

    # now_play(list_)
    # now_(list_)
    with open('media/mp3/__now__/now.txt', 'w', encoding='utf8') as f:
        f.write(list_[0])

    return list_


def now_play(list_):
    path = 'media/mp3'
    l = os.listdir(path)
    for k in l:
        if k[0]=='_': os.rmdir(path+'/'+k)

    i = list_[0]
    os.mkdir(path+'/__now__'+i)


def now_(list_):
    with open('media/mp3/__now__/now.txt', 'w', encoding='utf8') as f:
        f.write(list_[0])



if __name__=='__main__':
    print(predict_all_genre('./audio'))