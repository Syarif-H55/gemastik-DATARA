/**
 * Backdrop landing: gradien biru-putih (sama persis dengan halaman
 * login/register, hanya versi terang) + blob biru lembut yang melayang.
 * Teks di atasnya hitam polos sehingga tidak menabrak background.
 */
export function MeshBackground() {
  return (
    <div
      aria-hidden
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-[linear-gradient(120deg,#edf4ff_0%,#f7fbff_22%,#dfeaff_50%,#f2f7ff_78%,#e6efff_100%)] bg-[length:300%_300%] animate-gradient-pan"
    >
      <div className="animate-blob-a absolute -left-24 -top-32 size-[28rem] rounded-full bg-blue-400/25 blur-3xl" />
      <div className="animate-blob-b absolute -right-28 top-1/4 size-[26rem] rounded-full bg-sky-300/25 blur-3xl" />
      <div className="animate-blob-c absolute -bottom-40 left-1/3 size-[24rem] rounded-full bg-indigo-300/20 blur-3xl" />
    </div>
  );
}