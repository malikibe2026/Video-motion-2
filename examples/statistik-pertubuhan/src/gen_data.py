# Data REKAAN untuk demo video. Tiada data sebenar. Benih tetap.
import json, random, math, datetime
R = random.Random(20261023)
PARL = ['P.114 Kepong','P.115 Batu','P.116 Wangsa Maju','P.117 Segambut','P.118 Setiawangsa','P.119 Titiwangsa','P.120 Bukit Bintang','P.121 Lembah Pantai','P.122 Seputeh','P.123 Cheras','P.124 Bandar Tun Razak']
PW = [6,8,7,9,6,7,12,10,9,8,7]
SEK = {'Perkhidmatan': (['Perdagangan Borong & Runcit','Makanan & Minuman','Pengangkutan & Penyimpanan','Maklumat & Komunikasi','Hartanah','Profesional'], '301', 0.62),
       'Pembuatan': (['Makanan','Elektrik & Elektronik','Logam','Kimia'], '205', 0.18),
       'Pembinaan': (['Bangunan Kediaman','Kejuruteraan Awam','Pertukangan Khas'], '206', 0.14),
       'Perlombongan & Pengkuarian': (['Pengkuarian'], '207', 0.03),
       'Pertanian': (['Tanaman','Ternakan'], '101', 0.03)}
FE = [f'Pegawai {c} (Tetap)' for c in 'ABCDEFGH'] + [f'Pegawai {c} (PMS)' for c in 'JKLM']
FEQ = {f: 0.35 + 0.55 * R.random() for f in FE}   # kecekapan rekaan setiap FE
PENY = ['Penyelia 1', 'Penyelia 2', 'Penyelia 3']
LK = ['14', '21', '23', '25', '33', '41', '52']; KB = ['71', '72', '74', '77']
rows = []
d0 = datetime.date(2026, 6, 1)
for i in range(780):
    sek = R.choices(list(SEK), [v[2] for v in SEK.values()])[0]; subs, kp, _ = SEK[sek]
    fe = FE[i % len(FE)] if R.random() < 0.85 else R.choice(FE); q = FEQ[fe]
    u = R.random()
    if u < 0.62 * q + 0.25: kod = '11'
    elif u < 0.62 * q + 0.25 + 0.10: kod = R.choice(LK)
    elif u < 0.62 * q + 0.25 + 0.15: kod = R.choice(KB)
    else: kod = None
    if kod is None: st = 'Dalam Proses'
    else:
        v = R.random()
        st = 'Selesai' if v < 0.55 + 0.3 * q else ('Semakan SMD' if v < 0.75 + 0.2 * q else ('Semakan DOSM Negeri' if v < 0.9 else 'Pinda Semula - Data tidak lengkap'))
    pmks = R.choices(['Mikro', 'Kecil', 'Sederhana', 'Besar'], [0.45, 0.32, 0.15, 0.08])[0]
    base = {'Mikro': 4e5, 'Kecil': 3e6, 'Sederhana': 2.2e7, 'Besar': 1.5e8}[pmks]
    sem = round(base * math.exp(R.gauss(0, 0.7)))
    g = R.gauss(0.05, 0.18) if R.random() > 0.06 else R.choice([-0.7, -0.6, 0.9, 1.4])
    seb = round(sem / max(0.2, 1 + g))
    exp_ = lambda x: round(x * (0.62 + 0.25 * R.random()))
    pk = max(1, round({'Mikro': 3, 'Kecil': 18, 'Sederhana': 90, 'Besar': 420}[pmks] * math.exp(R.gauss(0, 0.4))))
    tt = (d0 + datetime.timedelta(days=int(min(140, abs(R.gauss(55, 35)))))).isoformat() if kod else None
    rows.append({
        'id': i + 1, 'muat_naik_id': 'demo-1', 'bil': i + 1, 'no_siri': f'{990000000000 + i * 37:012d}', 'no_id': f'D{i + 1:05d}',
        'nama': f'Pertubuhan Contoh {i + 1:04d} Sdn. Bhd.', 'tahun_rujukan': '2025',
        'pegawai_kerja_luar': fe, 'penyelia': PENY[FE.index(fe) % 3], 'negeri': 'W.P. Kuala Lumpur',
        'pejabat_operasi': 'DOSM W.P. Kuala Lumpur', 'daerah_lokasi_semasa': 'W.P. Kuala Lumpur', 'daerah_pos_semasa': 'W.P. Kuala Lumpur',
        'parlimen': R.choices(PARL, PW)[0], 'fasa_be': R.choice(['Fasa 2', 'Fasa 3']), 'tier': R.choices(['Tier 1', 'Tier 2', 'Tier 3'], [0.2, 0.35, 0.45])[0],
        'kod_kp': f'{kp} - {sek}', 'sektor': sek, 'subsektor': R.choice(subs), 'pmks': pmks,
        'status_respon_semasa': kod, 'status_respon_sebelum': R.choice(['11', '11', '11', '21', None]),
        'status_rekod': st, 'cara_terima': R.choices(['e-Survei', 'Lawatan', 'E-mel', 'Telefon'], [0.5, 0.3, 0.15, 0.05])[0] if kod else None,
        'tarikh_terima': tt,
        'pendapatan_semasa': sem, 'pendapatan_sebelum': seb, 'perbelanjaan_semasa': exp_(sem), 'perbelanjaan_sebelum': exp_(seb),
        'pekerja_semasa': pk, 'pekerja_sebelum': max(1, round(pk / (1 + R.gauss(0.03, 0.1)))),
        'gaji_semasa': round(pk * 42000 * math.exp(R.gauss(0, 0.2))), 'gaji_sebelum': round(pk * 40000 * math.exp(R.gauss(0, 0.2))),
        'harta_tetap_semasa': round(sem * 0.4 * math.exp(R.gauss(0, 0.5))), 'harta_tetap_sebelum': round(seb * 0.4 * math.exp(R.gauss(0, 0.5))),
        'tambahan': {}})
json.dump(rows, open('data.json', 'w'))
from collections import Counter
print(len(rows), Counter(r['status_rekod'] for r in rows))
