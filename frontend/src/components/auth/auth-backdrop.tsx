/**
 * Backdrop halaman auth (login/register): gradien biru korporat yang
 * berjalan pelan + blob lembut yang melayang (transform/opacity saja,
 * GPU-friendly). Dekoratif semata; animasi dimatikan saat user memilih
 * prefers-reduced-motion (lihat globals.css).
 */
export function AuthBackdrop() {
  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed inset-0 -z-10 overflow-hidden bg-[linear-gradient(120deg,#edf4ff_0%,#f7fbff_22%,#dfeaff_50%,#f2f7ff_78%,#e6efff_100%)] bg-[length:300%_300%] animate-gradient-pan dark:bg-[linear-gradient(120deg,#0d1730_0%,#16213f_25%,#0b1326_50%,#131d3a_75%,#0e1831_100%)]"
    >
      <div className="absolute -left-24 -top-32 size-[28rem] rounded-full bg-blue-400/25 blur-3xl animate-blob-a dark:bg-blue-500/15" />
      <div className="absolute -right-28 top-1/4 size-[26rem] rounded-full bg-sky-300/25 blur-3xl animate-blob-b dark:bg-sky-500/10" />
      <div className="absolute -bottom-40 left-1/3 size-[24rem] rounded-full bg-indigo-300/20 blur-3xl animate-blob-c dark:bg-indigo-500/10" />
    </div>
  );
}
