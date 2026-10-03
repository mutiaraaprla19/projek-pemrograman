
import streamlit as st
from pathlib import Path
from datetime import datetime, date
import json, csv, re, math
from collections import Counter

# =========================================================
# KONFIGURASI
# =========================================================
st.set_page_config(
    page_title="Ayo Belajar Teks Anekdot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

APP_TITLE = "Ayo Belajar Teks Anekdot"
DATA_DIR = Path("data_app")
USERS_DIR = DATA_DIR / "users"
USERS_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================
# GAYA TAMPILAN
# =========================================================
st.markdown("""
<style>
.block-container {padding-top:1.4rem; padding-bottom:3rem; max-width:1180px;}
.hero {
  padding:1.5rem 1.6rem; border-radius:22px;
  background:linear-gradient(135deg,#f7d7e2,#e8f4ff);
  border:1px solid rgba(0,0,0,.08); margin-bottom:1rem;
}
.hero h1{margin:0;font-size:2.15rem}
.hero p{margin:.55rem 0 0;color:#4b5563;font-size:1.02rem}
.card {
  padding:1rem 1.1rem; border-radius:18px; border:1px solid #e5e7eb;
  background:white; min-height:118px; margin-bottom:.75rem;
  box-shadow:0 4px 16px rgba(0,0,0,.035);
}
.soft {
  padding:.95rem 1rem; border-radius:14px; background:#faf7ff;
  border:1px solid #eee7fb; margin:.55rem 0;
}
.tip {
  padding:.85rem 1rem; border-left:5px solid #ff6b9a;
  background:#fff7fa; border-radius:10px; margin:.7rem 0;
}
.good {padding:.8rem 1rem;border-radius:12px;background:#eefbf3;border:1px solid #caefd7}
.mid  {padding:.8rem 1rem;border-radius:12px;background:#fff9e8;border:1px solid #f5e5a9}
.bad  {padding:.8rem 1rem;border-radius:12px;background:#fff1f1;border:1px solid #f5caca}
.small {font-size:.9rem;color:#6b7280}
div[data-testid="stMetric"]{border:1px solid #e5e7eb;border-radius:16px;padding:.8rem;background:white}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA MATERI
# =========================================================
TUJUAN = """
### 🎯 Tujuan Pembelajaran Teks Anekdot
Di akhir Fase E, peserta didik mampu menulis gagasan, pikiran, pandangan, arahan, atau pesan tertulis untuk berbagai tujuan secara logis, kritis, dan kreatif dalam bentuk teks informasional dan/atau fiksi.

### 🏆 Capaian Pembelajaran
Pada akhir Fase E, peserta didik mampu menulis berbagai teks untuk menyampaikan pendapat dan mempresentasikan serta menanggapi informasi nonfiksi dan fiksi secara kritis dan etis.
"""

PENGANTAR = """
Pada bagian ini, peserta didik mempelajari konsep dasar teks anekdot secara bertahap, meliputi pengertian dan karakteristik teks anekdot, struktur teks, kaidah kebahasaan, serta penerapan konsep melalui contoh dan analisis teks.

Materi dirancang agar peserta didik tidak hanya mengenali unsur kelucuan, tetapi juga mampu memahami kritik, sindiran, pesan, dan makna tersirat yang terdapat dalam teks anekdot.

Setelah mempelajari bagian ini, peserta didik diharapkan mampu:
1. menjelaskan pengertian dan fungsi teks anekdot;
2. mengidentifikasi struktur abstrak, orientasi, krisis/komplikasi, reaksi, dan koda;
3. menemukan kaidah kebahasaan yang digunakan;
4. menganalisis kritik atau sindiran dalam teks; dan
5. memberikan penjelasan dengan bahasa sendiri berdasarkan pemahaman terhadap materi.
"""

PENGERTIAN = """
Menurut Agustina (2019:29), teks anekdot merupakan cerita atau karangan singkat yang memberikan kesan lucu kepada pembaca. Topiknya dapat berasal dari pengalaman hidup seseorang dan dapat berupa sindiran atau kritikan dalam bidang hukum, politik, atau pendidikan.

Teks anekdot dapat dipahami sebagai teks naratif singkat yang mengandung humor serta maksud tertentu di balik kelucuannya. Kelucuan dapat muncul melalui tindakan tokoh, percakapan, situasi tidak terduga, atau peristiwa yang bertentangan dengan kebiasaan atau logika umum.

Kosasih (2014:2) menjelaskan bahwa anekdot berbentuk cerita yang mengandung humor dan kritikan. Anekdot tidak semata-mata menyediakan hal yang lucu, tetapi juga dapat mengandung pesan yang diharapkan memberi pelajaran kepada khalayak.

Dengan demikian, teks anekdot adalah cerita singkat yang mengandung unsur humor dan kritik. Kelucuannya bukan hanya untuk mengundang tawa, melainkan juga dapat menjadi sarana untuk menyampaikan pesan, sindiran, atau pandangan terhadap suatu keadaan.
"""

STRUKTUR = {
"Abstrak": "Bagian awal yang memberi gambaran tentang isi teks atau hal unik yang akan muncul. Sifatnya opsional.",
"Orientasi": "Bagian yang menunjukkan awal kejadian, latar belakang, tokoh, situasi, atau kondisi yang mengarah pada munculnya krisis.",
"Krisis/Komplikasi": "Bagian inti ketika muncul masalah, kejanggalan, ketidakpuasan, atau kejadian tidak biasa yang mengundang perhatian/kelucuan.",
"Reaksi": "Tanggapan atau respons terhadap krisis. Bagian ini dapat berupa penyelesaian, celaan, kelucuan, atau respons yang mengejutkan.",
"Koda": "Bagian akhir yang berisi simpulan, komentar, persetujuan, atau penjelasan atas cerita. Sifatnya opsional."
}

KAIDAH = [
("Kalimat langsung", "Petikan langsung dari dialog tokoh. Anekdot sering memadukan kalimat langsung dan tidak langsung."),
("Nama tokoh utama/orang ketiga tunggal", "Tokoh dapat disebut secara langsung atau disamarkan, misalnya hakim, presiden, jaksa, atau tokoh masyarakat."),
("Keterangan waktu", "Menunjukkan waktu kejadian, misalnya kemarin, sore ini, suatu hari, ketika itu."),
("Kata kiasan/konotasi", "Kata atau ungkapan yang tidak selalu bermakna harfiah."),
("Kalimat sindiran", "Sindiran dapat diungkapkan melalui pengandaian, perbandingan, atau lawan kata."),
("Konjungsi penjelas", "Misalnya kata 'bahwa', sering muncul ketika dialog diubah menjadi kalimat tidak langsung."),
("Kata kerja material", "Menunjukkan aktivitas yang dapat diamati, misalnya mendatangi, menyiapkan, membawa, mencicipi."),
("Kata kerja mental", "Menunjukkan sesuatu yang dipikirkan atau dirasakan, misalnya menyimpulkan dan memutuskan."),
("Konjungsi sebab akibat", "Menunjukkan hubungan sebab-akibat, misalnya maka, sehingga, oleh karena itu."),
("Kalimat imperatif", "Kalimat yang berisi perintah, larangan, atau peringatan."),
("Kalimat seru", "Kalimat untuk menegaskan atau mengungkapkan perasaan, biasanya ditandai tanda seru."),
("Konjungsi temporal", "Menunjukkan urutan waktu, misalnya akhirnya, kemudian, lalu, selanjutnya."),
("Kalimat retoris", "Pertanyaan yang tidak membutuhkan jawaban dan dapat pula digunakan sebagai sindiran."),
]

CONTOH = """**Politikus Sering Berbohong**

Sebuah bus penuh dengan para politikus keluar dari marka jalan. Akhirnya, menabrak sebuah pohon besar di ladang seorang petani tua. Hampir semua penumpang menjadi korban dalam kecelakaan tersebut.

Petani tua segera memberikan bantuan. Namun apa daya, ia tidak bisa berbuat apa pun karena memang para penumpang bus itu dianggap sudah tidak bisa tertolong lagi. Petani tua kemudian menguburkan politikus-politikus itu di kebunnya.

Beberapa hari kemudian petugas dari kepolisian mendatanginya dan menanyakan peristiwa kecelakaan itu, “Apakah benar mereka semua meninggal, Pak?”

Petani tua itu menjawab, “Mereka tampak sudah meninggal, Pak. Memang di antara mereka ada yang masih bergerak-gerak, bahkan beberapa di antara mereka ada yang berkata bahwa mereka belum meninggal. Tapi Anda kan tahu, betapa seringnya politikus itu berbohong. Saya tidak mempercayai perkataan mereka. Oleh karena itu, tetap saya harus menguburkannya!”"""

ANALISIS_CONTOH = {
"Abstrak": "Kecelakaan bus yang mengangkut para politikus menjadi gambaran awal peristiwa utama.",
"Orientasi": "Petani tua berusaha memberi bantuan lalu menguburkan para politikus karena menganggap mereka tidak tertolong.",
"Krisis/Komplikasi": "Polisi datang dan menanyakan apakah benar semua politikus meninggal; muncul kejanggalan karena belum tentu semuanya meninggal.",
"Reaksi": "Petani menjelaskan bahwa beberapa masih bergerak dan berkata belum meninggal, tetapi ia tidak mempercayai mereka.",
"Koda": "Tidak terdapat koda secara eksplisit; cerita ditutup pada reaksi petani."
}

REFERENSI = [
"Sucikaharti, A. (2021). e-Modul Anekdot Bahasa Indonesia.",
"Utama, T. H. F. (2021). Alur Tujuan Pembelajaran Mata Pelajaran Bahasa Indonesia (Fase E).",
"Permatasari, I. A. (2020). Modul Pembelajaran SMA Bahasa Indonesia.",
"Ediawati, R. (2020). E-modul Bahasa dan Sastra Indonesia Kelas X: Makna Tersirat dalam Teks Anekdot. Kemendikbud.",
"Rifai, B. (2020). E-modul Bahasa dan Sastra Indonesia Kelas X: Struktur dan Teks Kebahasaan Anekdot. Kemendikbud.",
"Agustina (2019). Rujukan pengertian teks anekdot sebagaimana digunakan dalam bahan pembelajaran.",
"Kosasih (2014). Rujukan mengenai teks anekdot sebagaimana digunakan dalam bahan pembelajaran."
]

QUIZ = [
{"q":"Cerita lucu (humor) berbeda dengan teks anekdot karena ...","ops":["Humor hanya mengandung kelucuan saja","Humor tidak bisa dikonsumsi oleh semua orang","Humor tidak mengandung manfaat sama sekali","Humor tidak memuat sindiran atau kritik halus","Humor hanya cocok untuk orang dewasa"],"ans":3,"exp":"Teks anekdot umumnya tidak hanya lucu, tetapi juga memuat kritik/sindiran."},
{"q":"Berikut ini yang bukan ciri-ciri teks anekdot adalah ...","ops":["Menggelitik","Berbentuk cerita","Memiliki pesan moral","Struktur terdiri dari abstraksi, reaksi dan koda","Memiliki unsur lucu"],"ans":2,"exp":"Mengacu pada kunci dalam blueprint final."},
{"q":"Bertujuan menghibur, menggambarkan sisi lain orang berpengaruh, membangkitkan tawa, dan menggambarkan karakter secara singkat merupakan ...","ops":["Tujuan anekdot","Manfaat anekdot","Visi anekdot","Struktur anekdot","Kebahasaan anekdot"],"ans":0,"exp":"Pernyataan tersebut merujuk pada tujuan anekdot."},
{"q":"Abstraksi merupakan bagian awal yang memberikan gambaran tentang isi teks dan biasanya menunjukkan ...","ops":["Hal yang unik","Latar belakang peristiwa","Masalah tokoh","Penyelesaian masalah","Fenomena alam"],"ans":0,"exp":"Abstrak memberi gambaran awal, biasanya berupa hal unik yang akan muncul."},
{"q":"“Akhirnya dia menyesal ... dan berjanji menjadi orang yang lebih baik.” termasuk struktur ...","ops":["Orientasi","Krisis","Reaksi","Abstraksi","Koda"],"ans":4,"exp":"Bagian tersebut bersifat penutup/simpulan sehingga termasuk koda."},
{"q":"Kalimat yang bukan menunjukkan peristiwa masa lalu adalah ...","ops":["Pada suatu hari aku berbelanja di pasar","Pada bulan Mei, dia telah berhasil lulus sekolah","Seharusnya, besok menjadi hari bahagia","Ketika itu aku lupa menawarkan diskon","Kemarin, hujan sangat deras"],"ans":2,"exp":"Kata 'besok' mengarah ke waktu yang akan datang."},
{"q":"“Aku turut berduka cita ...” memenuhi maksim ...","ops":["Kearifan","Simpati","Kedermawanan","Kerendahan hati","Pujian"],"ans":1,"exp":"Ungkapan duka menunjukkan simpati."},
{"q":"Kalimat yang menunjukkan konjungsi waktu adalah ...","ops":["Dosen muda lulusan UPI menjadi dosen terbaik","Mahasiswa sedang mengerjakan tugas","Dosen menjelaskan kepada mahasiswa","Saat tiba presentasi, Deny gugup","Kelas kembali online"],"ans":3,"exp":"Kata 'saat' menunjukkan hubungan waktu."},
{"q":"Berikut langkah menganalisis teks anekdot, kecuali ...","ops":["Menemukan kata kias","Menganalisis struktur dan kebahasaan","Memahami teks dengan baik","Mencermati teks dengan sungguh-sungguh","Membaca anekdot dengan saksama"],"ans":1,"exp":"Mengacu pada kunci dalam blueprint final."},
{"q":"Penulisan kalimat langsung yang tepat adalah ...","ops":["Akhirnya, hakim berkata, “Pak, tolong berhenti.","“Pak tolong angkat telefonnya.”: Hakim.","Guru: “Silahkan kumpulkan tugasnya!”","Akhirnya siswa selesai mengerjakan tugas.","“Sel, tolong ambilkan penghapus,” kata guru."],"ans":2,"exp":"Mengacu pada kunci jawaban dalam blueprint final."},
]

ESSAYS = [
{
"q":"Jelaskan pengertian teks anekdot dengan menggunakan bahasamu sendiri!",
"concepts":[
    ["cerita","teks","kisah"],
    ["singkat","pendek"],
    ["lucu","humor","menghibur","kelucuan"],
    ["kritik","sindiran","menyindir"]
],
"required":3,
"hint":"Jawaban ideal menjelaskan bahwa anekdot adalah cerita singkat, lucu/menghibur, dan mengandung kritik atau sindiran."
},
{
"q":"Sebutkan dan jelaskan ciri-ciri teks anekdot!",
"concepts":[
    ["cerita","berbentuk cerita","naratif"],
    ["lucu","humor","menghibur","menggelitik"],
    ["kritik","sindiran"],
    ["pesan","makna","pelajaran"],
    ["tokoh","kejadian","peristiwa"]
],
"required":3,
"hint":"Minimal tiga ciri benar dan sebaiknya diberi penjelasan."
},
{
"q":"Jelaskan fungsi atau tujuan dari teks anekdot!",
"concepts":[
    ["menghibur","hiburan","lucu","humor"],
    ["kritik","mengkritik"],
    ["sindiran","menyindir"],
    ["pesan","pandangan","pelajaran"],
],
"required":3,
"hint":"Intinya mencakup fungsi menghibur serta menyampaikan kritik/sindiran dan pesan."
},
{
"q":"Jelaskan apa yang dimaksud dengan makna tersirat dalam teks anekdot! Berikan contohnya secara singkat.",
"concepts":[
    ["tidak langsung","tersirat","tidak dinyatakan","tersembunyi"],
    ["konteks","isi cerita","dipahami"],
    ["kritik","sindiran","pesan"],
    ["contoh","misalnya"]
],
"required":3,
"hint":"Jelaskan bahwa makna tersirat tidak disampaikan secara langsung, dipahami dari konteks, lalu berikan contoh."
}
]

# =========================================================
# UTILITAS
# =========================================================
def slugify(text):
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-z0-9_-]+","_",text)
    return text.strip("_") or "user"

def user_dir():
    u = st.session_state.get("user")
    if not u: return None
    p = USERS_DIR / slugify(u["nama"])
    p.mkdir(parents=True, exist_ok=True)
    return p

def read_json(path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except:
        pass
    return default

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def add_activity(kind, detail=""):
    p = user_dir()
    if not p: return
    path = p/"activity.json"
    data = read_json(path, [])
    data.append({"waktu":datetime.now().isoformat(timespec="seconds"),"jenis":kind,"detail":detail})
    write_json(path, data[-300:])

def save_chat(q,a):
    p=user_dir()
    if not p:return
    path=p/"chat.json"
    data=read_json(path,[])
    data.append({"waktu":datetime.now().isoformat(timespec="seconds"),"q":q,"a":a})
    write_json(path,data[-100:])

def load_chat():
    p=user_dir()
    return read_json(p/"chat.json",[]) if p else []

def save_quiz(score, correct):
    p=user_dir()
    if not p:return
    path=p/"quiz.json"; data=read_json(path,[])
    data.append({"waktu":datetime.now().isoformat(timespec="seconds"),"score":score,"correct":correct,"total":len(QUIZ)})
    write_json(path,data[-50:]); add_activity("Latihan",f"Skor {score}")

def save_essay(results, answers):
    p=user_dir()
    if not p:return
    path=p/"essay.json"; data=read_json(path,[])
    data.append({"waktu":datetime.now().isoformat(timespec="seconds"),"score":sum(r["score"] for r in results),
                 "results":results,"answers":answers})
    write_json(path,data[-50:]); add_activity("Evaluasi",f"Skor {sum(r['score'] for r in results)}")

def mark_material(name):
    p=user_dir()
    if not p:return
    path=p/"progress.json"; data=read_json(path,{"materi":[]})
    if name not in data["materi"]:
        data["materi"].append(name); write_json(path,data)
    add_activity("Materi",name)

def normalize(t):
    return re.sub(r"\s+"," ",re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]"," ",(t or "").lower())).strip()

def contains_any(text, variants):
    t=normalize(text)
    return any(normalize(v) in t for v in variants)

def evaluate_essay(answer, spec):
    a=normalize(answer)
    if len(a.split()) < 4:
        return {"category":"🔴 Belum sesuai","score":5,"reason":"Jawaban masih terlalu singkat untuk menunjukkan pemahaman konsep.","advice":spec["hint"]}
    hits = sum(1 for group in spec["concepts"] if contains_any(a,group))
    total = len(spec["concepts"])
    ratio = hits/total if total else 0
    # bonus kecil untuk jawaban yang lebih elaboratif
    elaboration = min(len(a.split())/45, 1) * 0.15
    weighted = min(1, ratio*0.85 + elaboration)
    score = round(weighted*25)
    if hits >= spec["required"] and weighted >= .72:
        cat="✅ Sudah sesuai"
        reason=f"Inti jawaban sudah sesuai. {hits} dari {total} unsur konsep utama terdeteksi dan penjelasan cukup relevan."
        advice="Pertahankan cara menjelaskan dengan bahasa sendiri. Kamu bisa memperkuat jawaban dengan contoh atau alasan tambahan."
    elif hits >= max(1, spec["required"]-1):
        cat="🟡 Sebagian sesuai"
        reason=f"Jawaban sudah mengarah benar, tetapi baru mencakup sekitar {hits} dari {total} unsur konsep utama."
        advice=spec["hint"]
    else:
        cat="🔴 Belum sesuai"
        reason=f"Jawaban belum cukup menunjukkan inti konsep. Baru sekitar {hits} dari {total} unsur utama yang terdeteksi."
        advice=spec["hint"]
    return {"category":cat,"score":score,"reason":reason,"advice":advice}

# =========================================================
# TUTOR AI LOKAL
# =========================================================
KB = {
"pengertian": PENGERTIAN,
"tujuan": TUJUAN,
"struktur": "\n".join([f"{k}: {v}" for k,v in STRUKTUR.items()]),
"kaidah": "\n".join([f"{k}: {v}" for k,v in KAIDAH]),
"contoh": CONTOH,
"referensi": "\n".join(REFERENSI),
}

STOP={"apa","yang","dan","di","ke","dari","itu","ini","dengan","untuk","tentang","jelaskan","tolong","dong","ya","aku","saya","kamu","bisa","gimana","bagaimana","kenapa","mengapa","lagi","contoh"}
def keywords(q):
    return [w for w in normalize(q).split() if len(w)>2 and w not in STOP]

def retrieve(q):
    kws=keywords(q)
    scored=[]
    for title,body in KB.items():
        t=normalize(title+" "+body)
        score=sum(t.count(k) for k in kws)
        if any(k in normalize(title) for k in kws): score += 5
        scored.append((score,title,body))
    scored.sort(reverse=True)
    return scored[0] if scored else (0,"","")

def tutor_answer(q, history):
    qn=normalize(q)
    # pertanyaan singkat mengikuti konteks terakhir
    context_q = history[-1]["q"] if history else ""
    search_q = q if len(keywords(q))>=2 else (context_q+" "+q if context_q else q)
    # respons khusus
    if "beda" in qn and "orientasi" in qn and ("krisis" in qn or "komplikasi" in qn):
        return ("Orientasi adalah bagian yang memperkenalkan situasi awal, tokoh, latar, atau keadaan sebelum masalah utama muncul. "
                "Krisis/komplikasi adalah bagian ketika masalah, kejanggalan, atau kejadian tidak biasa mulai terjadi. "
                "Cara gampang mengingatnya: **orientasi = sebelum masalah**, **krisis = masalah mulai muncul**.")
    if "kemudian" in qn and ("apa" in qn or "termasuk" in qn):
        return ("Kata **“kemudian”** termasuk **konjungsi temporal** karena menunjukkan urutan waktu/peristiwa. "
                "Contoh lain: *lalu, akhirnya,* dan *selanjutnya*.")
    if "menyimpulkan" in qn:
        return ("Kata **“menyimpulkan”** termasuk **kata kerja mental** karena berkaitan dengan proses berpikir tokoh.")
    if any(x in qn for x in ["jawaban latihan","kunci latihan","jawaban evaluasi","kunci jawaban"]):
        return ("Aku bantu dengan **petunjuk dulu ya**, supaya kamu tetap belajar. Sebutkan nomor soal atau bagian yang membingungkan, "
                "nanti aku bantu arahkan konsep yang perlu kamu perhatikan.")
    score,title,body=retrieve(search_q)
    if score<=0:
        return ("Aku belum menemukan bagian materi yang paling cocok. Coba tanyakan lebih spesifik tentang **pengertian, struktur, "
                "kaidah kebahasaan, contoh, kritik/sindiran, atau makna tersirat** dalam teks anekdot.")
    # ringkas konteks
    paras=[p.strip() for p in body.split("\n") if p.strip()]
    picked=[]
    kws=keywords(search_q)
    for p in paras:
        if any(k in normalize(p) for k in kws):
            picked.append(p)
        if len(" ".join(picked))>900: break
    if not picked: picked=paras[:2]
    return f"**{title.title()}**\n\n" + "\n\n".join(picked[:4])

# =========================================================
# SESSION
# =========================================================
defaults={"user":None,"menu":"🏠 Beranda","pending_menu":None}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v

MENU = ["🏠 Beranda","🧭 Tutorial Penggunaan AI","📚 Materi","🤖 Tanya AI","🎯 Latihan","✍️ Evaluasi",
        "⭐ Favorit","🗒️ Catatan","📅 Absensi","📈 Progress","🔎 Pencarian","👩‍🏫 Dashboard Guru"]

if st.session_state.pending_menu:
    st.session_state.menu = st.session_state.pending_menu
    st.session_state.pending_menu = None

def goto(name):
    st.session_state.pending_menu = name
    st.rerun()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📚 Ayo Belajar")
    if not st.session_state.user:
        nama=st.text_input("Nama")
        peran=st.selectbox("Peran",["Siswa","Guru"])
        if st.button("Masuk",type="primary",use_container_width=True):
            if nama.strip():
                st.session_state.user={"nama":nama.strip(),"peran":peran}
                add_activity("Login",peran)
                st.rerun()
            else: st.warning("Masukkan nama terlebih dahulu.")
    else:
        st.success(f"Halo, **{st.session_state.user['nama']}** 👋")
        st.caption(st.session_state.user["peran"])
        if st.button("Keluar",use_container_width=True):
            st.session_state.user=None; st.session_state.menu="🏠 Beranda"; st.rerun()

    st.divider()
    current = st.session_state.menu if st.session_state.menu in MENU else MENU[0]
    idx = MENU.index(current)
    choice=st.radio("Navigasi",MENU,index=idx,key="nav_radio")
    if choice != st.session_state.menu:
        st.session_state.menu=choice
        st.rerun()

def need_login():
    if not st.session_state.user:
        st.info("Silakan login dari sidebar untuk menggunakan fitur ini.")
        return False
    return True

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero">
<h1>📚 Ayo Belajar Teks Anekdot</h1>
<p>Belajar santai, tanya sesukamu, latihan, lalu cek seberapa jauh kamu sudah paham ✨</p>
</div>
""", unsafe_allow_html=True)

menu=st.session_state.menu

# =========================================================
# BERANDA
# =========================================================
if menu=="🏠 Beranda":
    st.markdown("## Hai, bestie! 👋")
    st.write("Belajar teks anekdot sekarang lebih santai dan interaktif. Kamu bisa baca materi, tanya AI Tutor, coba latihan, kerjakan evaluasi, dan cek perkembangan belajarmu.")
    st.markdown('<div class="tip"><b>✨ Nggak harus langsung paham.</b><br>Kamu bisa tanya, coba, salah, perbaiki, lalu makin ngerti.</div>',unsafe_allow_html=True)
    c1,c2,c3,c4,c5=st.columns(5)
    if c1.button("📖 Mulai Belajar",use_container_width=True): goto("📚 Materi")
    if c2.button("🤖 Tanya AI",use_container_width=True): goto("🤖 Tanya AI")
    if c3.button("🎯 Coba Latihan",use_container_width=True): goto("🎯 Latihan")
    if c4.button("✍️ Evaluasi",use_container_width=True): goto("✍️ Evaluasi")
    if c5.button("📈 Progress",use_container_width=True): goto("📈 Progress")
    st.divider()
    st.markdown("### Mau mulai dari mana? 🚀")
    a,b,c=st.columns(3)
    with a: st.markdown('<div class="card"><b>📚 Materi</b><br><span class="small">Pelajari konsep dasar secara bertahap.</span></div>',unsafe_allow_html=True)
    with b: st.markdown('<div class="card"><b>🤖 AI Tutor</b><br><span class="small">Tanya dengan bahasa sendiri, termasuk pertanyaan lanjutan.</span></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="card"><b>🎯 Latihan & Evaluasi</b><br><span class="small">Cek pemahaman dan dapatkan feedback.</span></div>',unsafe_allow_html=True)

# =========================================================
# TUTORIAL
# =========================================================
elif menu=="🧭 Tutorial Penggunaan AI":
    st.markdown("## 🧭 Tutorial Penggunaan AI")
    st.caption("Ikuti langkah berikut supaya semua fitur bisa kamu pakai dengan nyaman.")
    steps=[
        ("1️⃣ Login","Masukkan nama, pilih peran Siswa, lalu tekan Masuk. Aktivitas belajar akan tersimpan berdasarkan nama pengguna."),
        ("2️⃣ Baca Materi","Buka menu Materi dan pelajari Tujuan & Capaian, Pengantar, Pengertian, Struktur, Kaidah Kebahasaan, Contoh, dan Referensi."),
        ("3️⃣ Tanya AI","Buka Tanya AI lalu ketik pertanyaan dengan bahasa sendiri. Kamu boleh bertanya lanjutan, misalnya: “Apa itu orientasi?” lalu “Bedanya dengan krisis apa?”"),
        ("4️⃣ Kerjakan Latihan","Latihan berisi soal pilihan ganda. Setelah dikirim, kamu mendapatkan skor dan pembahasan singkat."),
        ("5️⃣ Kerjakan Evaluasi","Jawab soal esai dengan bahasamu sendiri. Jawaban tidak harus sama persis dengan materi; sistem menilai inti makna dan ketepatan konsep."),
        ("6️⃣ Baca Feedback & Progress","Feedback dibagi menjadi Sudah Sesuai, Sebagian Sesuai, atau Belum Sesuai. Progress menampilkan perkembangan belajarmu.")
    ]
    for title,body in steps:
        st.markdown(f'<div class="card"><b>{title}</b><br><span class="small">{body}</span></div>',unsafe_allow_html=True)
    st.info("💡 Tips: kalau belum paham jawaban AI, kamu bisa bilang: “jelaskan lebih sederhana”, “beri contoh lain”, atau “bedanya dengan ... apa?”")

# =========================================================
# MATERI
# =========================================================
elif menu=="📚 Materi":
    if need_login():
        st.markdown("## 📚 Materi Teks Anekdot")
        st.caption("Materi disusun dari tujuan belajar hingga contoh dan analisis. Pilih tab yang ingin dipelajari.")
        tabs=st.tabs(["🎯 Tujuan & Capaian","📝 Pengantar","💡 Pengertian","🧩 Struktur","🗣️ Kaidah","📖 Contoh","📚 Referensi"])
        with tabs[0]:
            st.markdown(TUJUAN); 
            if st.button("Tandai sudah dipelajari",key="m1"): mark_material("Tujuan & Capaian"); st.success("Tersimpan.")
        with tabs[1]:
            st.markdown(PENGANTAR)
            if st.button("Tandai sudah dipelajari",key="m2"): mark_material("Pengantar"); st.success("Tersimpan.")
        with tabs[2]:
            st.markdown("### 💡 Pengertian Teks Anekdot")
            st.markdown('<div class="tip"><b>Inti cepat:</b> Anekdot = cerita singkat + humor + kritik/sindiran/pesan.</div>',unsafe_allow_html=True)
            st.write(PENGERTIAN)
            if st.button("Tandai sudah dipelajari",key="m3"): mark_material("Pengertian"); st.success("Tersimpan.")
        with tabs[3]:
            st.markdown("### 🧩 Struktur Teks Anekdot")
            cols=st.columns(5)
            for i,(k,v) in enumerate(STRUKTUR.items()):
                with cols[i]:
                    st.markdown(f'<div class="card"><b>{i+1}. {k}</b><br><span class="small">{v}</span></div>',unsafe_allow_html=True)
            with st.expander("Lihat penjelasan lebih lengkap"):
                for k,v in STRUKTUR.items(): st.markdown(f"**{k}** — {v}")
            if st.button("Tandai sudah dipelajari",key="m4"): mark_material("Struktur"); st.success("Tersimpan.")
        with tabs[4]:
            st.markdown("### 🗣️ Kaidah Kebahasaan")
            for i,(k,v) in enumerate(KAIDAH,1):
                with st.expander(f"{i}. {k}"): st.write(v)
            if st.button("Tandai sudah dipelajari",key="m5"): mark_material("Kaidah Kebahasaan"); st.success("Tersimpan.")
        with tabs[5]:
            st.markdown("### 📖 Contoh Teks Anekdot")
            st.markdown(CONTOH)
            st.markdown("### 🔎 Analisis Struktur")
            for k,v in ANALISIS_CONTOH.items():
                st.markdown(f'<div class="soft"><b>{k}</b><br>{v}</div>',unsafe_allow_html=True)
            if st.button("Tandai sudah dipelajari",key="m6"): mark_material("Contoh Teks"); st.success("Tersimpan.")
        with tabs[6]:
            st.markdown("### 📚 Referensi")
            for r in REFERENSI: st.write("•",r)
            if st.button("Tandai sudah dipelajari",key="m7"): mark_material("Referensi"); st.success("Tersimpan.")

# =========================================================
# TANYA AI
# =========================================================
elif menu=="🤖 Tanya AI":
    if need_login():
        st.markdown("## 🤖 Tanya AI Tutor")
        st.caption("Tanya apa saja tentang teks anekdot. Riwayat aktif disimpan sampai 100 interaksi per siswa.")
        hist=load_chat()
        for item in hist[-12:]:
            with st.chat_message("user"): st.write(item["q"])
            with st.chat_message("assistant"): st.markdown(item["a"])
        q=st.chat_input("Contoh: Apa bedanya orientasi dan krisis?")
        if q:
            ans=tutor_answer(q,hist)
            save_chat(q,ans); add_activity("Tanya AI",q[:90])
            st.rerun()

# =========================================================
# LATIHAN PG
# =========================================================
elif menu=="🎯 Latihan":
    if need_login():
        st.markdown("## 🎯 Latihan Pilihan Ganda")
        st.caption("Pilih jawaban terbaik untuk setiap soal. Setelah dikirim, skor dan pembahasan akan muncul.")
        with st.form("quiz_form"):
            answers=[]
            for i,q in enumerate(QUIZ):
                st.markdown(f"**{i+1}. {q['q']}**")
                choice=st.radio("Pilih jawaban",range(len(q["ops"])),format_func=lambda x,ops=q["ops"]: f"{chr(65+x)}. {ops[x]}",
                                key=f"quiz_{i}",index=None)
                answers.append(choice)
            submit=st.form_submit_button("Kirim Latihan",type="primary")
        if submit:
            if any(a is None for a in answers):
                st.warning("Masih ada soal yang belum dijawab.")
            else:
                correct=sum(1 for i,a in enumerate(answers) if a==QUIZ[i]["ans"])
                score=round(correct/len(QUIZ)*100)
                save_quiz(score,correct)
                st.metric("Nilai Latihan",score)
                if score>=75: st.success(f"Benar {correct} dari {len(QUIZ)} soal. Nice! 🎉")
                else: st.warning(f"Benar {correct} dari {len(QUIZ)} soal. Coba pelajari lagi bagian yang masih keliru.")
                for i,(a,q) in enumerate(zip(answers,QUIZ),1):
                    ok=a==q["ans"]
                    with st.expander(f"{'✅' if ok else '❌'} Soal {i}"):
                        st.write("Jawabanmu:", q["ops"][a])
                        st.write("Jawaban acuan:", q["ops"][q["ans"]])
                        st.caption(q["exp"])

# =========================================================
# EVALUASI ESAI
# =========================================================
elif menu=="✍️ Evaluasi":
    if need_login():
        st.markdown("## ✍️ Evaluasi Esai")
        st.caption("Gunakan bahasamu sendiri. Sistem menilai inti makna, relevansi, dan ketepatan konsep—bukan kecocokan kalimat.")
        st.info("Setiap soal maksimal 25 poin. Total nilai maksimal 100.")
        with st.form("essay_form"):
            answers=[]
            for i,s in enumerate(ESSAYS,1):
                st.markdown(f"**{i}. {s['q']}**")
                answers.append(st.text_area("Jawabanmu",key=f"essay_{i}",height=120,placeholder="Tulis dengan bahasamu sendiri..."))
            submit=st.form_submit_button("Kirim Evaluasi",type="primary")
        if submit:
            if any(not a.strip() for a in answers):
                st.warning("Semua soal perlu dijawab sebelum evaluasi dikirim.")
            else:
                results=[evaluate_essay(a,s) for a,s in zip(answers,ESSAYS)]
                save_essay(results,answers)
                total=sum(r["score"] for r in results)
                st.metric("Nilai Evaluasi",total)
                for i,r in enumerate(results,1):
                    cls="good" if "Sudah" in r["category"] else ("mid" if "Sebagian" in r["category"] else "bad")
                    st.markdown(f'<div class="{cls}"><b>Soal {i} — {r["category"]} ({r["score"]}/25)</b><br>{r["reason"]}<br><br><b>Saran:</b> {r["advice"]}</div>',unsafe_allow_html=True)

# =========================================================
# FAVORIT
# =========================================================
elif menu=="⭐ Favorit":
    if need_login():
        st.markdown("## ⭐ Favorit")
        options=["Tujuan & Capaian","Pengantar","Pengertian","Struktur","Kaidah Kebahasaan","Contoh Teks","Referensi"]
        p=user_dir(); path=p/"favorites.json"
        fav=read_json(path,[])
        selected=st.multiselect("Pilih bagian materi yang ingin disimpan",options,default=[x for x in fav if x in options])
        if st.button("Simpan Favorit"):
            write_json(path,selected); add_activity("Favorit",", ".join(selected)); st.success("Favorit tersimpan.")
        if selected:
            st.write("Materi favoritmu:",", ".join(selected))

# =========================================================
# CATATAN
# =========================================================
elif menu=="🗒️ Catatan":
    if need_login():
        st.markdown("## 🗒️ Catatan Belajar")
        p=user_dir(); path=p/"notes.json"; notes=read_json(path,[])
        text=st.text_area("Tulis catatan baru",height=120)
        if st.button("Simpan Catatan",type="primary"):
            if text.strip():
                notes.append({"waktu":datetime.now().isoformat(timespec="seconds"),"isi":text.strip()})
                write_json(path,notes[-100:]); add_activity("Catatan",text[:80]); st.rerun()
        for n in reversed(notes[-20:]):
            st.markdown(f'<div class="soft"><span class="small">{n["waktu"]}</span><br>{n["isi"]}</div>',unsafe_allow_html=True)

# =========================================================
# ABSENSI
# =========================================================
elif menu=="📅 Absensi":
    if need_login():
        st.markdown("## 📅 Absensi")
        p=user_dir(); path=p/"attendance.json"; rows=read_json(path,[])
        today=date.today().isoformat()
        if any(r["tanggal"]==today for r in rows):
            st.success("Kamu sudah absen hari ini ✅")
        elif st.button("Absen Hari Ini",type="primary"):
            rows.append({"tanggal":today,"waktu":datetime.now().strftime("%H:%M:%S")})
            write_json(path,rows); add_activity("Absensi",today); st.rerun()
        st.write(f"Total kehadiran tercatat: **{len(rows)} hari**")
        if rows: st.dataframe(rows,use_container_width=True)

# =========================================================
# PROGRESS
# =========================================================
elif menu=="📈 Progress":
    if need_login():
        st.markdown("## 📈 Progress Belajar")
        p=user_dir()
        prog=read_json(p/"progress.json",{"materi":[]})
        quiz=read_json(p/"quiz.json",[])
        essay=read_json(p/"essay.json",[])
        chat=read_json(p/"chat.json",[])
        total_mat=7; done=len(set(prog.get("materi",[])))
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Materi",f"{done}/{total_mat}")
        c2.metric("Pertanyaan AI",len(chat))
        c3.metric("Latihan terakhir",quiz[-1]["score"] if quiz else "-")
        c4.metric("Evaluasi terakhir",essay[-1]["score"] if essay else "-")
        st.progress(done/total_mat if total_mat else 0)
        st.caption(f"Progress materi: {round(done/total_mat*100)}%")
        if prog.get("materi"): st.write("Sudah dipelajari:",", ".join(prog["materi"]))

# =========================================================
# PENCARIAN
# =========================================================
elif menu=="🔎 Pencarian":
    if need_login():
        st.markdown("## 🔎 Pencarian Materi")
        q=st.text_input("Cari kata/topik",placeholder="Contoh: krisis, konjungsi temporal, sindiran")
        if q:
            score,title,body=retrieve(q)
            if score>0:
                st.markdown(f"### Hasil teratas: {title.title()}")
                st.write(body[:3500])
            else: st.info("Belum ada hasil yang cocok.")

# =========================================================
# DASHBOARD GURU
# =========================================================
elif menu=="👩‍🏫 Dashboard Guru":
    if not need_login():
        pass
    elif st.session_state.user["peran"]!="Guru":
        st.warning("Dashboard Guru hanya tersedia untuk pengguna dengan peran Guru.")
    else:
        st.markdown("## 👩‍🏫 Dashboard Guru")
        rows=[]
        for folder in USERS_DIR.iterdir():
            if not folder.is_dir(): continue
            chat=read_json(folder/"chat.json",[])
            quiz=read_json(folder/"quiz.json",[])
            essay=read_json(folder/"essay.json",[])
            prog=read_json(folder/"progress.json",{"materi":[]})
            att=read_json(folder/"attendance.json",[])
            act=read_json(folder/"activity.json",[])
            rows.append({
                "Siswa":folder.name.replace("_"," ").title(),
                "Pertanyaan AI":len(chat),
                "Latihan terakhir":quiz[-1]["score"] if quiz else None,
                "Latihan tertinggi":max([x["score"] for x in quiz],default=None),
                "Evaluasi terakhir":essay[-1]["score"] if essay else None,
                "Progress materi":f"{len(set(prog.get('materi',[])))}/7",
                "Absensi":len(att),
                "Aktivitas terakhir":act[-1]["waktu"] if act else None
            })
        if not rows:
            st.info("Belum ada data siswa.")
        else:
            st.dataframe(rows,use_container_width=True)
            names=[r["Siswa"] for r in rows]
            pick=st.selectbox("Lihat detail siswa",names)
            folder=next(f for f in USERS_DIR.iterdir() if f.name.replace("_"," ").title()==pick)
            chat=read_json(folder/"chat.json",[])
            quiz=read_json(folder/"quiz.json",[])
            essay=read_json(folder/"essay.json",[])
            act=read_json(folder/"activity.json",[])
            t1,t2,t3,t4=st.tabs(["AI Tutor","Latihan","Evaluasi Esai","Aktivitas"])
            with t1:
                if chat:
                    for x in chat[-30:]:
                        st.markdown(f"**Siswa:** {x['q']}\n\n**AI:** {x['a']}\n\n---")
                else: st.caption("Belum ada riwayat.")
            with t2:
                st.dataframe(quiz,use_container_width=True) if quiz else st.caption("Belum ada nilai latihan.")
            with t3:
                if essay:
                    latest=essay[-1]
                    st.metric("Nilai terakhir",latest["score"])
                    for i,(a,r) in enumerate(zip(latest["answers"],latest["results"]),1):
                        st.markdown(f"**Soal {i}**")
                        st.write("Jawaban:",a)
                        st.write("Kategori:",r["category"],"| Skor:",r["score"])
                        st.caption(r["reason"])
                else: st.caption("Belum ada hasil evaluasi.")
            with t4:
                st.dataframe(act[-100:],use_container_width=True) if act else st.caption("Belum ada aktivitas.")

st.divider()
st.caption("Prototype pembelajaran • Ayo Belajar Teks Anekdot")
