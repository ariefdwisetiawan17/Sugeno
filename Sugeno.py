#Nama   : Arief Dwi Setiawan
#NIM    : 191011401937
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : Permintaan Pencucian Sepeda Motor

#Kecepatan Debit Air : min 4 liter/detik dan max 8 liter/detik.
#Banyaknya Sepeda Motor  : sedikit 2 dan banyak 10.
#Tingkat Kekotoran Sepeda Motor : rendah 20, sedang 50, dan 100 tinggi.

from socket import MSG_TRUNC


def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Motor():
    minimum = 2
    maximum = 10

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kotor():
    minimum = 20
    medium = 50
    maximum = 100

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Debit():
    minimum = 4
    maximum = 8
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_Motor, jumlah_kotor):
        mtr = Motor()
        ktr = Kotor()
        result = []
        
        # [R1] Jika Motor SEDIKIT, dan Kotor RENDAH, 
        #     MAKA Debit = 4
        α1 = min(mtr.sedikit(jumlah_Motor), ktr.rendah(jumlah_kotor))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Motor SEDIKIT, dan Kotor SEDANG, 
        #     MAKA Debit = 10 * jumlah_kotor + 100
        α2 = min(mtr.sedikit(jumlah_Motor), ktr.sedang(jumlah_kotor))
        z2 = 1 * jumlah_kotor + 100
        result.append((α2, z2))

        # [R3] Jika Motor SEDIKIT, dan Kotor TINGGI, 
        #     MAKA Debit = 8 * jumlah_kotor + 15
        α3 = min(mtr.sedikit(jumlah_Motor), ktr.tinggi(jumlah_kotor))
        z3 = 8 * jumlah_kotor + 15
        result.append((α3, z3))

        # [R4] Jika Motor BANYAK, dan Kotor RENDAH,
        #     MAKA Debit = 2 * jumlah_Motor + 10 * jumlah_kotor
        α4 = min(mtr.banyak(jumlah_Motor), ktr.rendah(jumlah_kotor))
        z4 = 2 * jumlah_Motor + 10 * jumlah_kotor
        result.append((α4, z4))

        # [R5] Jika Motor BANYAK, dan Kotor SEDANG,
        #     MAKA Debit = 5 * jumlah_Motor + 4 * jumlah_kotor + 100
        α5 = min(mtr.banyak(jumlah_Motor), ktr.sedang(jumlah_kotor))
        z5 = 5 * jumlah_Motor + 4 * jumlah_kotor + 100
        result.append((α5, z5))

        # [R6] Jika Motor BANYAK, dan Kotor TINGGI,
        #     MAKA Debit = 5 * jumlah_Motor + 5 * jumlah_kotor + 20
        α6 = min(mtr.banyak(jumlah_Motor), ktr.tinggi(jumlah_kotor))
        z6 = 5 * jumlah_Motor + 5 * jumlah_kotor + 20
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_Motor, jumlah_kotor):
        inferensi_values = self.inferensi(jumlah_Motor, jumlah_kotor)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])
