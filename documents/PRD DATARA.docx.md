

**PRODUCT REQUIREMENTS DOCUMENT**

# **DATARA**

Data Analitik dan Rekomendasi untuk Pertumbuhan UMKM 

| Version | v1.2 |
| :---- | :---- |
| **Date** | 9 Agustus 2026 |
| **Team** | Pisang \- Agil Kurniawan, Syarif Hidayatullah, Raifa Aziz F. P. H. |
| **Product Owner** | \[haswa\] |
| **Client / Stakeholder** | UMKM |
| **Status** | Draft  |

**PART 1: PROBLEM, OBJECTIVES & SCOPE**

# **1\.  Problem Statement**

### **1.1  Background & Context**

Usaha mikro di sektor makanan dan minuman menghasilkan data transaksi dan biaya operasional setiap hari, tetapi sebagian pemilik usaha masih menentukan harga, mengelola stok, dan mengevaluasi kinerja produk berdasarkan perkiraan atau pengalaman. Keterbatasan pemahaman terhadap HPP, margin keuntungan, dan pola penjualan membuat data yang sebenarnya tersedia belum dimanfaatkan secara optimal dalam pengambilan keputusan bisnis. Kondisi tersebut dapat menyebabkan kesalahan penetapan harga, risiko kelebihan atau kekurangan stok, serta keputusan bisnis yang kurang tepat dan berpotensi menurunkan profitabilitas usaha. 

### **1.2  Problem Statement**

Pemilik usaha mikro makanan dan minuman tidak dapat mengambil keputusan bisnis secara optimal karena belum mampu mengolah data penjualan, HPP, biaya, stok, dan profitabilitas menjadi informasi yang dapat digunakan, sehingga penetapan harga, pengelolaan persediaan, dan evaluasi kinerja produk masih banyak bergantung pada perkiraan dan berisiko menurunkan keuntungan usaha. 

### **1.3  Who is Affected**

* **Pemilik UMKM makanan dan minuman skala mikro (Primary User)**  
  Merupakan pemilik usaha yang telah memiliki transaksi harian tetapi belum memanfaatkan data penjualan dan biaya secara optimal untuk mengambil keputusan. Mereka kesulitan memahami hubungan antara penjualan, HPP, biaya, stok, margin, dan laba sehingga masih mengandalkan pengalaman atau perkiraan dalam menentukan harga, mengelola persediaan, dan mengevaluasi produk. Keterbatasan pengetahuan analitik dan keterbatasan waktu membuat mereka sulit mengolah data bisnis secara mandiri.

* **Karyawan atau pengelola operasional usaha (Secondary Affected Group)**  
  Membantu pemilik dalam menjalankan kegiatan operasional seperti pencatatan transaksi, pengelolaan stok, dan pengadaan bahan. Ketidakjelasan mengenai kondisi persediaan dan performa produk dapat membuat aktivitas operasional kurang terarah dan keputusan pengadaan masih bergantung pada instruksi atau perkiraan pemilik.

* **Usaha itu sendiri (Indirect Stakeholder)**  
  Ketidakmampuan mengubah data bisnis menjadi dasar keputusan dapat menyebabkan kesalahan penetapan harga, pengelolaan stok yang kurang optimal, dan evaluasi produk yang tidak tepat, sehingga berpotensi menghambat profitabilitas dan pertumbuhan usaha.


# **2\.  Objectives**

### **2.1  Business Objectives**

| \# | Objective | Why it matters | Success indicator |
| :---: | ----- | ----- | ----- |
| **1** | Membantu pemilik UMKM memahami kondisi keuangan dan operasional bisnis berdasarkan data penjualan, HPP, biaya, stok, dan profitabilitas.  | Pemilik membutuhkan gambaran kondisi bisnis yang lebih jelas sebelum mengambil keputusan.  | Minimal **90% data bisnis utama** yang tersedia dapat diolah menjadi indikator bisnis pada dashboard.  |
| **2** | Mengubah hasil analisis bisnis menjadi rekomendasi keputusan yang relevan dan dapat dipahami oleh pemilik UMKM.  | Data dan grafik saja belum cukup jika pengguna tetap harus melakukan interpretasi secara manual.  | Minimal **80% rekomendasi yang dihasilkan** memiliki alasan dan data pendukung yang dapat ditelusuri.  |
| **3** | Membantu pemilik UMKM melakukan evaluasi dan perencanaan bisnis berdasarkan hasil keputusan yang telah diterapkan.  | UMKM perlu mengetahui apakah keputusan yang diambil memberikan perkembangan yang sesuai dengan tujuan bisnis.  | Sistem mampu mencatat dan menampilkan **100% keputusan/rekomendasi yang diterapkan melalui sistem** beserta perkembangan indikator bisnisnya.  |

### **2.2  User Objectives**

| Actor | What they need to accomplish | What stops them today |
| ----- | ----- | ----- |
| Pemilik UMKM makanan dan minuman skala mikro  | Memahami kondisi keuangan dan operasional usaha berdasarkan data penjualan, HPP, biaya, stok, dan profitabilitas.  | Data bisnis masih tersebar dan belum mudah diolah menjadi informasi yang menggambarkan kondisi usaha secara menyeluruh.  |
| Pemilik UMKM makanan dan minuman skala mikro  | Menentukan harga jual dan melakukan evaluasi produk berdasarkan biaya, margin, dan performa penjualan.  | Keterbatasan pemahaman terhadap HPP dan margin membuat penentuan harga serta evaluasi produk masih banyak bergantung pada perkiraan.  |
| Pemilik UMKM makanan dan minuman skala mikro  | Menentukan keputusan terkait persediaan dan tindakan bisnis berdasarkan kondisi serta pola penjualan.  | Pemilik kesulitan memperkirakan kebutuhan stok dan menentukan tindakan yang perlu dilakukan dari data penjualan yang tersedia.  |
| Pemilik UMKM makanan dan minuman skala mikro  | Memantau hasil keputusan bisnis dan perkembangan usaha dari waktu ke waktu.  | Belum terdapat proses yang terstruktur untuk menghubungkan keputusan yang telah diambil dengan perubahan indikator bisnis.  |

# **3\.  Success Metrics**

| Metric | Baseline (now) | Target (3 months) | How it is measured |
| ----- | :---: | :---: | ----- |
| Keberhasilan menghasilkan rekomendasi yang dapat dijelaskan  | Belum tersedia, diukur melalui baseline testing  | ≥ **90% rekomendasi** memiliki alasan dan data pendukung yang dapat ditelusuri  | Pengujian output Decision Engine dan pemeriksaan setiap rekomendasi terhadap data bisnis yang menjadi dasar  |
| Akurasi perhitungan indikator bisnis  | Belum tersedia, diukur melalui baseline testing  | ≥ **95% hasil perhitungan** sesuai dengan hasil perhitungan pembanding  | Pengujian otomatis terhadap perhitungan HPP, omzet, laba, margin, dan indikator terkait menggunakan dataset uji  |
| Keberhasilan pengguna menyelesaikan proses pengambilan keputusan  | Belum tersedia, diukur melalui baseline usability testing  | ≥ **80% pengguna uji** berhasil menyelesaikan skenario pengambilan keputusan tanpa bantuan  | Usability testing dengan skenario seperti menentukan harga jual, mengevaluasi produk, dan menentukan kebutuhan restock  |

# **4\.  Scope**

### **4.1  In Scope & Out of Scope (MVP)**

| ✅  IN Scope (MVP) | ❌  OUT of Scope (v1) |
| ----- | ----- |
| **Business Dashboard** untuk menampilkan omzet, laba, HPP, margin, transaksi, dan indikator kesehatan bisnis  | **What-If Simulator**, simulasi dampak perubahan harga, HPP, atau volume penjualan  |
| **Smart Business Analytics** untuk menganalisis penjualan, performa produk, HPP, laba, margin, dan biaya operasional  | **Smart Alert** untuk memberikan peringatan otomatis terkait kondisi bisnis  |
| **Sales Forecasting** untuk memprediksi penjualan berdasarkan riwayat transaksi dan menjadi salah satu dasar pengambilan keputusan persediaan  | **Action Center** sebagai daftar tindakan bisnis yang diprioritaskan  |
| **Smart Pricing** untuk memberikan rekomendasi harga berdasarkan HPP, biaya, kondisi penjualan, dan target margin  | **Business Assistant** untuk tanya jawab menggunakan bahasa natural  |
| **Smart Restock** untuk memberikan rekomendasi waktu dan jumlah restock berdasarkan kondisi stok, riwayat penjualan, dan hasil Sales Forecasting  | Integrasi dengan layanan eksternal seperti marketplace, payment gateway, atau platform POS pihak ketiga  |
| **Product Profitability** untuk mengidentifikasi produk yang menguntungkan, potensial, dan perlu dievaluasi  | Otomatisasi operasional bisnis secara langsung, seperti melakukan pemesanan stok atau mengubah harga secara otomatis  |
| **Decision Engine & Explainable Recommendation** untuk menghasilkan rekomendasi keputusan beserta alasan dan data pendukung  |  |
| **Monitoring & Progress** untuk memantau perkembangan indikator bisnis setelah keputusan diterapkan dan data bisnis baru tersedia  |  |
| **Business Growth Roadmap** untuk mengevaluasi perkembangan usaha berdasarkan indikator bisnis dan memberikan arah menuju target pertumbuhan berikutnya  |  |

### **4.2  Assumptions & Constraints**

| Type | Description |
| ----- | ----- |
| **Assumption** | Pengguna merupakan pemilik UMKM makanan dan minuman skala mikro yang telah memiliki transaksi harian dan bersedia memasukkan data bisnis ke dalam sistem.  |
| **Assumption** | Pengguna memiliki data dasar berupa produk, harga jual, transaksi, biaya, dan informasi persediaan yang dapat digunakan untuk proses analisis.  |
| **Assumption** | Data yang dimasukkan pengguna dianggap cukup akurat untuk digunakan sebagai dasar perhitungan dan rekomendasi sistem.  |
| **Assumption** | Pengguna memiliki pemahaman dasar mengenai aktivitas bisnis seperti penjualan, biaya, stok, dan harga produk, tetapi belum terbiasa melakukan analisis data bisnis secara mandiri.  |
| **Constraint** | Pengembangan difokuskan pada fitur **MVP** yang telah ditetapkan dalam scope dan memiliki keterbatasan waktu pengerjaan untuk kebutuhan kompetisi GEMASTIK.  |
| **Constraint** | Sistem membutuhkan data bisnis yang memadai agar analisis dan rekomendasi dapat dihasilkan; kualitas rekomendasi bergantung pada kelengkapan dan kualitas data yang dimasukkan pengguna.  |
| **Constraint** | Sistem memberikan rekomendasi sebagai **decision support**, bukan keputusan otomatis yang mengubah harga, melakukan pembelian stok, atau menjalankan tindakan bisnis tanpa persetujuan pengguna.  |
| **Constraint** | Data bisnis pengguna harus disimpan dan diproses dengan memperhatikan keamanan serta perlindungan data yang digunakan oleh sistem.  |

**PART 2: FUNCTIONAL REQUIREMENTS & WORKFLOWS**

# **5\.  Functional Requirements**

### **5.1  FR Table: Pemilik UMKM** 

| FR ID | Actor | The system shall… | Condition / Trigger | Priority | MoSCoW |
| ----- | :---: | ----- | ----- | :---: | :---: |
| **FR-001** | pemilik UMKM | Sistem harus menampilkan ringkasan kondisi bisnis yang mencakup omzet, laba, HPP, margin, jumlah transaksi, dan indikator kesehatan bisnis.  | Ketika Pemilik membuka dashboard bisnis atau memilih periode tertentu.  | High | M |
| **FR-002** | pemililk UMKM  | Sistem harus menghitung HPP berdasarkan komponen biaya produk dan biaya yang tersedia.  | Ketika data produk dan komponen biaya tersedia atau diperbarui.  | High | M |
| **FR-003** | pemilik UMKM | Sistem harus menampilkan analisis performa penjualan berdasarkan periode dan produk.  | Ketika Pemilik membuka analisis bisnis atau memilih periode tertentu.  | High | M |
| **FR-004** | pemilik UMKM | Sistem harus menghitung dan menampilkan profitabilitas setiap produk berdasarkan pendapatan, HPP, biaya, laba, dan margin.  | Ketika data transaksi, produk, dan biaya yang diperlukan tersedia.  | High | M |
| **FR-005** | pemilik UMKM | Sistem harus menghasilkan rekomendasi harga jual berdasarkan HPP, biaya, kondisi penjualan, dan target margin.  | Ketika data produk, biaya, penjualan, dan target margin yang diperlukan tersedia.  | High | M |
| **FR-006**  | Pemilik UMKM  | Sistem harus menghasilkan prediksi penjualan berdasarkan riwayat transaksi yang tersedia.  | Ketika data historis penjualan yang memenuhi kebutuhan minimum forecasting tersedia.  | High | M |
| **FR-007** | Pemilik UMKM  | Sistem harus menghasilkan rekomendasi waktu dan jumlah restock berdasarkan kondisi persediaan, riwayat penjualan, dan hasil prediksi penjualan.  | Ketika data stok dan data yang diperlukan untuk Sales Forecasting tersedia.  | High  | M |
| **FR-008** | Pemilik UMKM | Sistem harus memberikan alasan dan data pendukung untuk setiap rekomendasi bisnis yang dihasilkan.  | Ketika sistem menghasilkan rekomendasi harga atau restock.  | High  | M |
| **FR-009**  | Pemilik UMKM  | Sistem harus memungkinkan Pemilik mencatat rekomendasi atau keputusan bisnis yang dipilih untuk diterapkan.  | Ketika Pemilik memilih rekomendasi yang ingin diterapkan.  | Medium  | S |
| **FR-010**  | Pemilik UMKM  | Sistem harus memantau perubahan indikator bisnis setelah keputusan diterapkan dan data bisnis baru tersedia.  | Ketika terdapat keputusan yang telah dicatat dan tersedia data bisnis setelah keputusan tersebut diterapkan.  | Medium  | S |
| **FR-011** | Pemilik UMKM  | Sistem harus mengevaluasi perkembangan bisnis berdasarkan indikator yang tersedia dan menampilkan posisi perkembangan usaha.  | Ketika data bisnis yang diperlukan untuk evaluasi tersedia.  | Medium  | S |
| **FR-012**  | Pemilik UMKM  | Sistem harus memberikan informasi mengenai target atau langkah yang dapat dilakukan untuk mencapai perkembangan bisnis berikutnya berdasarkan hasil evaluasi.  | Setelah sistem menentukan kondisi atau posisi perkembangan bisnis Pemilik.  | Medium | S |

| MoSCoW reference |
| :---- |
| **M** Must Have: the product does not ship without this. |
| **S** Should Have: significant value, expected in the next sprint or release. |
| **C** Could Have: nice to have; only included when higher-priority items are done. |
| **W** Won't Have (this time): deferred. Write it here so it cannot silently re-enter scope. |

# **6\.  User Workflows**

## **6.1  Workflow: Pencatatan Transaksi Penjualan** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Mencatat transaksi penjualan sehingga data penjualan tersimpan dan dapat digunakan untuk menghitung indikator bisnis, memperbarui persediaan, serta menjadi dasar analisis dan Sales Forecasting.  |
| **FRs covered** | FR-001, FR-003, FR-006, FR-007  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik memilih proses pencatatan transaksi penjualan.  |
| **2** | Sistem menampilkan produk yang tersedia untuk dicatat dalam transaksi.  |
| **3** | Pemilik memilih produk dan memasukkan jumlah produk yang terjual.  |
| **4** | Sistem menghitung nilai transaksi berdasarkan produk dan jumlah yang dimasukkan.  |
| **5** | Pemilik mengonfirmasi transaksi.  |
| **6** | Sistem memvalidasi data transaksi dan ketersediaan persediaan.  |
| **7** | Sistem menyimpan transaksi beserta detail produk dan jumlah yang terjual.  |
| **8** | Sistem memperbarui jumlah persediaan berdasarkan transaksi yang berhasil disimpan.  |
| **9** | Sistem memperbarui data penjualan yang digunakan untuk analisis bisnis dan forecasting.  |
| **10** | Sistem menampilkan konfirmasi bahwa transaksi berhasil dicatat dan data bisnis telah diperbarui.  |

### **Decision Points**

Every fork needs both paths written out. The NO path must always land somewhere: an error message, a retry option, or a hard stop.

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| **Data transaksi valid?**  | Sistem melanjutkan proses penyimpanan transaksi.  | Sistem menolak transaksi dan meminta Pemilik memperbaiki data yang tidak valid.  |
| Jumlah persediaan mencukupi?  | Sistem menyimpan transaksi dan memperbarui persediaan.  | Sistem tidak menyimpan transaksi dan memberi tahu Pemilik bahwa persediaan tidak mencukupi.  |
| Transaksi berhasil disimpan?  | Sistem memperbarui persediaan dan data analitik.  | Sistem tidak mengubah persediaan dan memberi tahu Pemilik bahwa transaksi gagal disimpan.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **Data transaksi tidak lengkap**  | Sistem menolak penyimpanan dan menunjukkan data yang harus dilengkapi.  |
| **Stok tercatat tidak mencukupi**  | Sistem tidak membuat jumlah persediaan menjadi negatif dan meminta Pemilik melakukan pengecekan atau penyesuaian stok.  |
| **Gagal menyimpan transaksi**  | Sistem tidak memperbarui persediaan dan memberi tahu Pemilik bahwa transaksi belum berhasil dicatat.  |
| **Produk sudah tidak aktif**  | Sistem tidak mengizinkan produk tersebut digunakan dalam transaksi dan meminta Pemilik memilih produk yang masih aktif.  |

## **6.2  Workflow: Perhitungan HPP dan Profitabilitas Produk** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Pemilik dapat mengetahui biaya produksi, HPP, laba, dan margin setiap produk berdasarkan data bahan dan biaya yang tersedia.  |
| **FRs covered** | FR-002, FR-004, FR-005, FR-008  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik memilih produk yang ingin dianalisis.  |
| **2** | Sistem mengambil data bahan, biaya bahan, harga jual, dan komponen biaya yang terkait dengan produk.  |
| **3** | Sistem menghitung total biaya yang diperlukan untuk menghasilkan produk.  |
| **4** | Sistem menghitung HPP produk berdasarkan komponen biaya yang tersedia.  |
| **5** | Sistem menghitung pendapatan, laba, dan margin berdasarkan harga jual dan data penjualan.  |
| **6** | Sistem membandingkan performa profitabilitas produk dengan indikator bisnis yang relevan.  |
| **7** | Sistem menampilkan HPP, pendapatan, laba, margin, dan status profitabilitas produk.  |
| **8** | Data hasil perhitungan digunakan sebagai salah satu dasar untuk menghasilkan rekomendasi harga dan evaluasi produk.  |

### **Decision Points**

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| Data biaya produk lengkap?  | Sistem melanjutkan perhitungan HPP.  | Sistem meminta Pemilik melengkapi data biaya yang diperlukan.  |
| Harga jual lebih tinggi dari HPP?  | Sistem menghitung laba dan margin produk.  | Sistem menandai produk sebagai kondisi yang perlu diperhatikan dan menampilkan peringatan.  |
| **Data penjualan tersedia?**  | Sistem dapat menghitung profitabilitas berdasarkan performa penjualan.  | Sistem hanya menampilkan informasi biaya/HPP dan memberi tahu bahwa analisis profitabilitas belum dapat dilakukan secara lengkap.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **Data bahan atau biaya belum lengkap**  | Sistem tidak menghasilkan HPP final dan menunjukkan komponen biaya yang belum tersedia.  |
| **HPP sama dengan harga jual**  | Sistem menunjukkan margin 0% dan menandai bahwa produk tidak menghasilkan laba kotor.  |
| **HPP lebih tinggi dari harga jual**  | Sistem menunjukkan kondisi rugi dan menandai produk untuk evaluasi harga atau biaya.  |
| **Produk belum memiliki transaksi**  | Sistem tetap dapat menghitung HPP jika data biaya tersedia, tetapi belum menampilkan analisis profitabilitas berbasis penjualan.  |

## **6.3  Workflow: Sales Forecasting** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Pemilik dapat mengetahui perkiraan penjualan pada periode berikutnya berdasarkan pola penjualan historis sebagai dasar untuk perencanaan persediaan dan keputusan bisnis.  |
| **FRs covered** | FR-003, FR-006, FR-007  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik membuka halaman Sales Forecasting.  |
| **2** | Sistem mengambil data transaksi penjualan historis yang tersedia.  |
| **3** | Sistem melakukan validasi terhadap kelengkapan dan jumlah data historis.  |
| **4** | Sistem melakukan pengolahan data penjualan untuk mengidentifikasi pola penjualan.  |
| **5** | Sistem menjalankan metode forecasting yang digunakan untuk menghasilkan prediksi penjualan periode berikutnya.  |
| **6** | Sistem menghasilkan estimasi jumlah penjualan untuk periode yang diprediksi.  |
| **7** | Sistem menampilkan hasil forecasting beserta periode prediksi dan informasi pendukung yang relevan.  |
| **8** | Sistem menggunakan hasil forecasting sebagai salah satu input dalam proses Smart Restock.  |

### **Decision Points**

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| **Data historis mencukupi?**  | Sistem melanjutkan proses forecasting.  | Sistem memberi tahu Pemilik bahwa data belum mencukupi dan tidak menghasilkan prediksi yang belum dapat dipertanggungjawabkan.  |
| **Data historis valid?**  | Sistem melakukan preprocessing dan forecasting.  | Sistem memberi tahu Pemilik adanya data yang tidak valid atau bermasalah dan meminta data diperbaiki.  |
| **Forecasting berhasil?**  | Sistem menyimpan dan menampilkan hasil prediksi.  | Sistem memberi tahu Pemilik bahwa prediksi belum dapat dihasilkan dan tidak menggunakan hasil tersebut untuk rekomendasi restock.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **Data historis belum mencukupi**  | Sistem tidak menampilkan prediksi sebagai hasil yang dapat digunakan dan memberikan informasi mengenai kebutuhan data tambahan.  |
| **Terdapat data penjualan yang tidak valid**  | Sistem menangani data sesuai aturan preprocessing atau memberi tahu Pemilik apabila data tidak dapat digunakan.  |
| **Penjualan sangat fluktuatif**  | Sistem tetap menampilkan hasil prediksi dengan informasi mengenai tingkat ketidakpastian atau keterbatasan prediksi jika metode yang digunakan mendukungnya.  |
| **Produk belum memiliki riwayat penjualan yang cukup**  | Sistem tidak menghasilkan forecast individual untuk produk tersebut dan menandainya sebagai belum dapat diprediksi.  |

## **6.4  Workflow: Smart Pricing** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Pemilik dapat memperoleh rekomendasi harga jual yang sesuai dengan kondisi biaya, HPP, margin, dan performa penjualan produk.  |
| **FRs covered** | FR-002, FR-004, FR-005, FR-008  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik memilih produk yang ingin dievaluasi harganya.  |
| **2** | Sistem mengambil data HPP, biaya terkait, harga jual saat ini, data penjualan, dan target margin produk.  |
| **3** | Sistem memvalidasi kelengkapan dan konsistensi data yang diperlukan.  |
| **4** | Sistem menghitung margin produk berdasarkan harga jual saat ini.  |
| **5** | Sistem menganalisis hubungan antara biaya, margin, dan performa penjualan produk.  |
| **6** | Sistem menentukan rentang harga yang dapat memenuhi kondisi bisnis dan target margin yang ditetapkan.  |
| **7** | Sistem menghasilkan rekomendasi harga jual.  |
| **8** | Sistem memberikan alasan dan data pendukung yang menjelaskan dasar rekomendasi.  |
| **9** | Pemilik meninjau rekomendasi dan dapat memilih untuk mencatat rekomendasi tersebut sebagai keputusan bisnis.  |

### **Decision Points**

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| Data HPP dan biaya lengkap?  | Sistem melanjutkan proses rekomendasi.  | Sistem menandai produk sebagai memiliki data yang belum lengkap dan tidak memberikan hasil profitabilitas yang tidak valid.  |
| Harga saat ini menghasilkan margin yang sesuai target?  | Sistem dapat menyarankan mempertahankan harga atau memberikan alternatif berdasarkan kondisi penjualan.  | Sistem menghitung alternatif harga yang dapat meningkatkan kesesuaian margin terhadap target.  |
| HPP lebih tinggi dari harga jual?  | Tidak berlaku.  | Sistem menandai produk sebagai kondisi rugi dan memberikan rekomendasi harga yang mempertimbangkan kebutuhan menutup HPP serta target margin.  |
| Data penjualan mencukupi untuk dianalisis?  | Sistem menggunakan performa penjualan sebagai salah satu pertimbangan rekomendasi.  | Sistem tetap dapat memberikan rekomendasi berbasis biaya dan margin, tetapi memberikan informasi bahwa data penjualan belum cukup sebagai dasar analisis.  |
| Pemilik menerima rekomendasi?  | Sistem mencatat rekomendasi sebagai keputusan yang dipilih.  | Sistem tidak mencatat rekomendasi sebagai keputusan dan membiarkan Pemilik kembali mengevaluasi produk.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **HPP lebih tinggi dari harga jual**  | Sistem menandai produk sebagai rugi dan menjelaskan bahwa harga saat ini belum menutup HPP.  |
| **Data biaya tidak lengkap**  | Sistem tidak menghasilkan rekomendasi final dan menunjukkan komponen biaya yang perlu dilengkapi.  |
| **Target margin tidak ditentukan**  | Sistem meminta Pemilik menentukan target margin sebelum rekomendasi final diberikan.  |
| **Data penjualan belum mencukupi**  | Sistem dapat menggunakan perhitungan biaya dan margin sebagai dasar, tetapi menampilkan keterbatasan analisis penjualan.  |
| **Harga rekomendasi terlalu jauh dari harga saat ini**  | Sistem menampilkan perubahan harga secara eksplisit agar Pemilik dapat mempertimbangkan dampaknya sebelum mencatat keputusan.  |

## 

## **6.5  Workflow: Smart Restock** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Pemilik dapat mengetahui produk yang perlu direstock serta memperoleh rekomendasi waktu dan jumlah restock berdasarkan kondisi persediaan dan perkiraan kebutuhan penjualan.  |
| **FRs covered** | FR-006, FR-007, FR-008  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik membuka halaman Smart Restock.  |
| **2** | Sistem mengambil data persediaan saat ini dan riwayat penjualan produk.  |
| **3** | Sistem memeriksa ketersediaan hasil Sales Forecasting untuk produk yang dianalisis.  |
| **4** | Sistem menggunakan hasil prediksi penjualan untuk memperkirakan kebutuhan persediaan pada periode berikutnya.  |
| **5** | Sistem membandingkan perkiraan kebutuhan dengan persediaan yang tersedia.  |
| **6** | Sistem menentukan produk yang membutuhkan restock berdasarkan hasil perbandingan.  |
| **7** | Sistem menghitung rekomendasi jumlah restock dan waktu yang disarankan berdasarkan kebutuhan yang diperkirakan.  |
| **8** | Sistem menampilkan rekomendasi restock beserta alasan dan data pendukung.  |
| **9** | Pemilik meninjau rekomendasi dan dapat mencatat rekomendasi tersebut sebagai keputusan bisnis.  |

### **Decision Points**

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| Data forecasting tersedia dan dapat digunakan?  | Sistem melanjutkan analisis kebutuhan persediaan.  | Sistem meminta Pemilik menunggu atau melengkapi data yang diperlukan untuk forecasting.  |
| Perkiraan kebutuhan lebih tinggi dari persediaan tersedia?  | Sistem menandai produk sebagai membutuhkan restock.  | Sistem menunjukkan bahwa persediaan diperkirakan masih mencukupi.  |
| **Jumlah restock dapat dihitung?**  | Sistem memberikan rekomendasi jumlah dan waktu restock.  | Sistem hanya menampilkan status kebutuhan persediaan dan menjelaskan data yang belum tersedia.  |
| **Pemilik menerima rekomendasi?**  | Sistem mencatat rekomendasi sebagai keputusan yang dipilih.  | Sistem tidak mencatatnya sebagai keputusan dan Pemilik dapat kembali mengevaluasi rekomendasi.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **Data penjualan belum cukup untuk forecasting**  | Sistem tidak memberikan rekomendasi restock berbasis forecasting dan menjelaskan kebutuhan data tambahan.  |
| **Stok saat ini 0**  | Sistem memprioritaskan produk sebagai kondisi yang perlu diperhatikan apabila terdapat kebutuhan penjualan berdasarkan forecast.  |
| **Forecast menunjukkan permintaan rendah**  | Sistem tidak secara otomatis merekomendasikan restock dalam jumlah besar dan menampilkan dasar pertimbangannya.  |
| **Forecast sangat fluktuatif**  | Sistem menampilkan hasil prediksi beserta informasi keterbatasan/ketidakpastian jika tersedia dari metode forecasting yang digunakan.  |
| **Persediaan diperkirakan mencukupi**  | Sistem tidak memberikan rekomendasi restock dan menampilkan estimasi periode sampai persediaan diperkirakan perlu ditambah.  |
| **Data stok tidak valid**  | Sistem meminta Pemilik melakukan penyesuaian data sebelum menghasilkan rekomendasi.  |

## 

## **6.6  Workflow: Product Profitability** 

| Actor | Pemilik UMKM  |
| :---- | :---- |
| **Goal** | Pemilik dapat mengetahui produk mana yang memberikan kontribusi keuntungan terbaik, produk yang memiliki potensi untuk dikembangkan, serta produk yang perlu dievaluasi berdasarkan performa penjualan dan profitabilitas.  |
| **FRs covered** | FR-003, FR-004, FR-008  |

### **Ideal Path**

| \# | Step description |
| :---: | ----- |
| **1** | Pemilik membuka halaman Product Profitability.  |
| **2** | Sistem mengambil data penjualan, harga jual, HPP, biaya, laba, dan margin setiap produk.  |
| **3** | Sistem menghitung indikator profitabilitas setiap produk berdasarkan periode yang dipilih.  |
| **4** | Sistem menganalisis hubungan antara performa penjualan dan profitabilitas produk.  |
| **5** | Sistem mengelompokkan produk berdasarkan kondisi performanya.  |
| **6** | Sistem menampilkan produk yang memiliki performa baik, memiliki potensi, atau perlu dievaluasi.  |
| **7** | Sistem menampilkan alasan dan data yang menjadi dasar pengelompokan setiap produk.  |
| **8** | Pemilik menggunakan hasil analisis sebagai dasar untuk mengevaluasi produk dan menentukan tindakan bisnis berikutnya.  |

### **Decision Points**

| Decision Point | YES / Success path | NO / Error path |
| ----- | ----- | ----- |
| **Data penjualan dan biaya tersedia?**  | Sistem melakukan analisis profitabilitas.  | Sistem meminta Pemilik melengkapi data yang diperlukan.  |
| **Produk menghasilkan margin positif?**  | Sistem mengevaluasi performa penjualan dan profitabilitas lebih lanjut.  | Sistem menandai produk sebagai produk yang perlu dievaluasi.  |
| **Penjualan dan profitabilitas menunjukkan performa baik?**  | Sistem mengelompokkan produk sebagai produk yang menguntungkan.  | Sistem melanjutkan evaluasi berdasarkan kombinasi indikator lainnya.  |
| **Produk memiliki penjualan tinggi tetapi profitabilitas rendah?**  | Sistem menandainya sebagai produk yang perlu dievaluasi, terutama dari sisi HPP dan harga jual.  | Sistem melanjutkan klasifikasi berdasarkan indikator yang tersedia.  |

### **Edge Cases**

| Edge Case | What the system must do |
| ----- | ----- |
| **Produk belum memiliki transaksi**  | Sistem tidak melakukan evaluasi performa penjualan dan menampilkan bahwa data penjualan belum tersedia.  |
| **Produk memiliki penjualan tinggi tetapi margin rendah**  | Sistem menandai kondisi tersebut agar Pemilik dapat mengevaluasi HPP atau harga jual.  |
| **Produk memiliki margin tinggi tetapi penjualan rendah**  | Sistem menandai produk sebagai produk yang memiliki potensi tetapi membutuhkan perhatian pada performa penjualan.  |
| **Produk mengalami kerugian**  | Sistem menandai produk sebagai perlu dievaluasi dan menampilkan faktor biaya serta harga yang berkontribusi terhadap kondisi tersebut.  |
| **Data biaya tidak lengkap**  | Sistem tidak memberikan klasifikasi profitabilitas final dan meminta Pemilik melengkapi data biaya.  |

