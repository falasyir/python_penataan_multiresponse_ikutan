import pandas as pd
import numpy as np



def get_other_multirespon(dataset, first_multi_respon, include_first=True):
    """
    Mendapatkan kolom multirespon lain dari kolom pertamanya
    
    Parameter
    ----------------
    dataset : tabel dataset
    first_multi_respon : kolom pertama pada daftar kolom multirespon yang ingin didapatkan. kolom pertama harus di-inputkan dalam bentuk list.
    include_first : mengikutsertakan kolom pertama pada hasil pencarian kolom muultiresopn
        True --> kolom pertama disertakan
        False --> kolom pertama tidak diikutsertakan
    
    Return
    ----------------
    kolom_multi_respon : array yang di dalamnya terdapat list kolom multiresspon
    list_kolom_multi_respon : daftar list kolom multirespon
    """

    list_kolom = dataset.columns

    # Mendapatkan kolom multirespon
    kolom_multi_respon = []
    
    
    # mengecek apakah kolom pertama multirespon sudah dalam bentuk list atau belum, jika belum akan dikonversi ke bentuk list
    if isinstance(first_multi_respon, list)==False:
        first_multi_respon = [first_multi_respon]
    
    for i in range(len(first_multi_respon)):

        # Mendapatkan index kolom multirespon pertama
        idx_first = dataset.columns.to_list().index(first_multi_respon[i])

        klm_multi_respon = []
        prev_column = None

        # Looping dari kolom multirespon pertama sampai nama kolom berbeda
        for i in range(idx_first, len(list_kolom)-1):

            # Syarat skip jika kolom multirespon pertama tidak disertakan
            if i==idx_first and include_first==False:
                continue

            # mendapatkan nama kolom dengan menghilangkan label pertanyaan dan nomor multirespon
            nama_kolom_ = list_kolom[i].split("_")
            nama_kolom_ = "_".join(nama_kolom_[1:3])

            
            if prev_column==None:
                prev_column=nama_kolom_

            # jika nama kolom berbeda dari prev_column, berhenti
            elif prev_column!=None and prev_column!=nama_kolom_:
                break
                
            klm_multi_respon.append(list_kolom[i])
            
        # gabungkan data kolom multirespon yang didapatkan
        kolom_multi_respon.append(klm_multi_respon)
        
    # mengonversi list dalam array menjadi list tunggal
    list_kolom_multi_respon = np.unique(kolom_multi_respon).tolist()
        
    return kolom_multi_respon, list_kolom_multi_respon




def reassign_multirespon_ikutan(dataset, kolom_acuan, kolom_ikutan=[]):
    """
    Melakukan reassign data pada kolom multirespon dengan memperhatikan kolom acuan dan kolom ikutan. Penataan data pada kolom ikutan akan mengikuti pola urutan nomor kolom multirespon pada kolom acuan.
    
    Parameter
    ----------------
    dataset : tabel dataset yang akan ditata ulang nilainya
    kolom_acuan : kolom pertama pada daftar kolom multirespon yang akan digunakan sebagai kolom acuan
    kolom_ikutan : daftar kolom pertama yang ingin ditata ulang mengikuti pola urutan kolom acuan. kolom ikutan bisa lebih dari 1 kolom multirespon.
        default = [] --> secara default, kolom_ikutan tidak aktif, sehingga penataan ulang data hanya akan dilakukkan pada kolom acuan saja
    
    Return
    ----------------
    dataset_reassign : hasil tabel dataset
    """    
    
    # mendapatkan kolom-kolom multirespon
    array_acuan, list_acuan = get_other_multirespon(dataset, kolom_acuan)
    if kolom_ikutan!=[]:
        array_ikutan, list_ikutan = get_other_multirespon(dataset, kolom_ikutan)
    
    # mendapatkan nilai unik dari kolom acuan
    all_data_multirespon = dataset[list_acuan].values
    unik_data_multirespon = np.unique(all_data_multirespon[~np.isnan(all_data_multirespon)])
    
    # membuat dataframe kosong untuk menampung hasil reassign sebelum dikembalikan ke dataset keseluruhan
    temp = pd.DataFrame(index=dataset.index)


    # looping utama akan dilakukan sebanyak jumlah kolom acuan
    for klm in list_acuan:
        nama_kolom_ = klm.split("_")
        
        # nomor pada nama kolom acuan akan digunakan oleh kolom ikutan untuk menentukan kolom yang mana yang akan disamakan penataan datanya
        nomor_acuan_ = nama_kolom_[-1]

        # nama kolom baru untuk kolom-kolom acuan (tanpa nomor multirespon)
        nama_kolom_ = "_".join(nama_kolom_[:-1])

        # looping untuk unik value pada kolom acuan
        for i in range(len(unik_data_multirespon)):
            
            # mendapatkan data pada kolom acuan dan juga index-nya pada unik value ke-i
            value_ = dataset[dataset[klm].isin([unik_data_multirespon[i]])][klm]
            idx_value_ = value_.index

            # menggunakan data unik value sebagai nomor pada kolom data yang baru
            nomor_kolom_ = int(unik_data_multirespon[i])
            new_kolom_ = nama_kolom_ +"_"+ str(nomor_kolom_)

            # memasukkan data 
            temp.loc[idx_value_, new_kolom_] = value_
            
            
            # jika kolom ikutan didefinisikan, blok program berikut akan dieksekusi
            if kolom_ikutan!=[]:
                
                # looping sebanyak jumlah kelompok kolom ikutan
                for j in range(len(array_ikutan)):
                    
                    # membuat nama kolom
                    first_ikutan_ = array_ikutan[j][0]
                    nama_ikutan_ = first_ikutan_.split("_")
                    nama_ikutan_ = "_".join(nama_ikutan_[:-1])

                    # membuat nama kolom baru dengan mengikuti penomoran kolom acuan
                    new_ikutan_ = nama_ikutan_ +"_"+ str(nomor_kolom_)

                    # menentukan kolom target pada dataset masukan yang akan ditata ulang menggunakan acuan nomor multirespon pada kolom acuan
                    target_kolom_ = nama_ikutan_ +"_"+ nomor_acuan_
                    
                    # memasukkan data
                    temp.loc[idx_value_, new_ikutan_] = dataset.loc[idx_value_, target_kolom_]


    # membuat daftar kolom dengan label pertanyaan dari data yang sudah ditata ulang
    temp1 = temp.melt().copy()
    temp1 = temp1.drop(columns='value')
    temp1 = temp1.drop_duplicates(subset='variable')
    temp1['label'] = temp1['variable'].str.split("_").str[0]

    # menedapatkan label pertanyaan pada kolom acuan
    first_acuan = array_acuan[0][0]
    label_acuan = first_acuan.split("_")[0]

    # jika kolom ikutan didefinisikan, array / kelompok list kolom-kolom yang ditata ulang merupakan gabungan dari array kolom acuan dan array kolom ikutan
    if kolom_ikutan!=[]:
        all_array_geser = array_acuan + array_ikutan
    else:
        all_array_geser = array_acuan

    dataset_reassign = dataset.copy()
    
    # looping sebanyak kelompok kolom yang ditata ulang
    for arr in all_array_geser:
        
        # mendapatkan label pertanyaan
        label_ = arr[0].split("_")[0]
        
        # mendapatkan daftar kolom pada satu label pertanyaan
        list_kolom_ = temp1[temp1['label'].isin([label_])]['variable'].to_list()

        # aturan untuk melakukan pencarian nomor index kolom pertama pada kolom-kolom yang ditata ulang
        if label_==label_acuan:
            idx_first = dataset_reassign.columns.to_list().index(first_acuan)        
        else:
            idx_first = dataset_reassign.columns.to_list().index(arr[0])

        # menghapus kolom multirespon yang asli
        dataset_reassign = dataset_reassign.drop(columns=arr)
        
        # menyisipkan hasil reassign / penataan ulang data kolom multirespon pada dataset
        dataset_reassign = pd.concat([dataset_reassign.iloc[:, :idx_first], temp[list_kolom_], 
                                      dataset_reassign.iloc[:, idx_first:]],
                                     axis=1)

    return dataset_reassign