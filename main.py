from Activator import Activator
from SNR_Calculation.preperator import *
from SNR_Calculation.map_generator import *
from SNR_Calculation.map_db import *


def prep_data(base_path):
    image_shape = (1944, 1536)
    header = 0
    M = 19.1262
    watt = 6

    # crop_1
    #crop = slice(500, 1500), slice(600, 1522)

    #crop_2
    crop = slice(500, 1500), slice(900, 1147)

    _str = base_path.split('sgrischagin\\')[1]
    path_to_result = os.path.join(r'C:\Users\Sergej Grischagin\Desktop\Auswertung_MA\SNR', _str, '20211122_without_detectorslices')

    calc_snr = SNRPrepperator(path=base_path, img_shape=image_shape, header=header, magnification=M, crop_area=crop,
                              path_result=path_to_result, watt=watt)
    calc_snr()



def fast_CT():
    stack_range = (50, 100)
    img_shape = (1536, 1944)
    header = 2048

    imgs = r'\\132.187.193.8\junk\sgrischagin\2021-10-04_Sergej_Res-phantom_135kV_1mean_texp195_15proj-per-angle\test_fast_CT'
    darks = r'\\132.187.193.8\junk\sgrischagin\2021-10-04_Sergej_Res-phantom_135kV_1mean_texp195_15proj-per-angle\darks'
    refs = r'\\132.187.193.8\junk\sgrischagin\2021-10-04_Sergej_Res-phantom_135kV_1mean_texp195_15proj-per-angle\refs'

    darks = file.volume.Reader(darks, mode='raw', shape=img_shape, header=header, dtype='u2').load_range((stack_range[0], stack_range[-1]))
    refs = file.volume.Reader(refs, mode='raw', shape=img_shape, header=header, dtype='u2').load_range((stack_range[0], stack_range[-1]))

    list_Ts = []
    list_angles = []
    data = file.volume.Reader(imgs, mode='raw', shape=img_shape, header=header, dtype='<u2').load_all()
    px_map = h.load_bad_pixel_map()

    for i in range(len(data)):
        if darks is None and refs is None:
            T = data[np.where(data > 0)].min()
        else:
            img = (data[i] - darks) / (refs - darks)
            T = img[np.where(img > 0)].min()
        list_Ts.append(T)
        list_angles.append(i)
    a = np.asarray(list_Ts)
    b = np.asarray(list_angles)
    del img, data, refs, darks
    gc.collect()
    return np.vstack([a, b])



def main():
    # =============== RAW DATA PREPERATION ===============
    #   1) calculates SNR spectra from sets of projections, refs and darks
    #   2) saves the calculated spectra as a txt file + final plot in the same directory
    #   :param base_path: must be the directory of the kV folders

    #prep_data(base_path=r'\\132.187.193.8\junk\sgrischagin\2021-11-23-sergej_Al-StepWedge_6W')





    snr_data = r'C:\Users\Sergej Grischagin\Desktop\Auswertung_MA\SNR\2021-11-23-sergej_Al-StepWedge_6W\20211122_without_detectorslices\2021-11-24_SNR'
    T_data = r'C:\Users\Sergej Grischagin\Desktop\Auswertung_MA\SNR\2021-11-23-sergej_Al-StepWedge_6W\20211122_without_detectorslices\2021-11-24_T'
    result = r'C:\Users\Sergej Grischagin\Desktop\Auswertung_MA\SNR\2021-11-23-sergej_Al-StepWedge_6W\20211122_without_detectorslices\EVALUATION'

    acti = Activator(snr_files=snr_data, T_files=T_data, U0=100, snr_user=1.0, ssize=(150, 250))
    acti()


if __name__ == '__main__':
    main()
















'''
def write_data_to_DB(path):
    for file in os.listdir(path):
        if file.endswith('.csv') or file.endswith('.CSV'):
            working_file = os.path.join(path, file)
            d = int(file.split('_mm')[0])
            db = DB(path_DB=path)
            with open(working_file) as f:
                content = f.readlines()
                content = [x.strip() for x in content]
                for _c in range(len(content)):
                    line = content[_c]
                    kV = float(line.split(',')[0])
                    T = float(line.split(',')[1])
                    SNR = float(line.split(',')[2])
                    db.add_data(d, voltage=kV, T=T, SNR=SNR)
'''




