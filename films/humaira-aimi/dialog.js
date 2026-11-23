// Dialog loghat Terengganu (rekaan, untuk gurauan). H = Humaira (baju kuning, bertopi), A = Aimi (baju merah jambu).
// [mula, tamat, penutur, ayat]  — masa dalam saat, diselaraskan dengan aksi dalam video.
const LINES = [
  [0.30, 2.20, 'A', 'Weh Humaira, angkat tangan! Kite jadi bintang TikTok!'],
  [2.30, 4.20, 'H', 'Gini ke? Mung tengok Humaira, molek dop?'],
  [4.30, 6.05, 'H', 'Hahaha! Humaira comel sangat leaning!'],
  [6.15, 7.90, 'H', 'Aimi, mung pun comel… tapi Humaira lagi comel.'],
  [8.00, 9.50, 'A', 'Eh, perasang sungguh budok ni!'],
  [9.60, 11.20, 'H', 'Eh eh… ombok mari doh!'],
  [11.30, 13.00, 'H', '…Sejuk. Humaira dok suke.'],
  [13.10, 15.40, 'H', 'Abah. Jangan rakam. Humaira tengah serius ni.'],
  [15.50, 17.70, 'A', 'Humaira ni sokmo serius, lagu cikgu disiplin.'],
  [18.00, 19.80, 'A', 'Ombok! Basoh seluar jean Aimi!'],
  [19.90, 21.40, 'A', 'Mok kekgi marah ni…'],
  [21.55, 23.40, 'A', 'Hahaha! Biar la, kite gelak je!'],
  [23.50, 25.10, 'H', 'Mung gelak. Humaira tengok je.'],
  [25.30, 27.40, 'A', 'Humaira, Aimi buak kek pasir. Mung nok?'],
  [27.50, 29.60, 'H', 'Nok. Tapi Humaira dok leh makang.'],
  [29.80, 31.40, 'H', 'Ombok mari lagi! Kek pasir Humaira!'],
  [31.60, 33.20, 'A', 'Rakam Aimi pulok! Sini, sini!'],
  [33.30, 34.80, 'A', 'Lagu mane? Aimi lagi molek, kan?'],
  [34.90, 36.25, 'H', '…Ok. Kite seri.'],
];
const WHO = {
  H: { name: 'HUMAIRA', col: '#ffc531', deep: '#b9800b' },
  A: { name: 'AIMI', col: '#ff7fb0', deep: '#c2426f' },
};
// Approximate head positions (1080x1920 frame) for speech-bubble tails and punch-ins.
function headPos(who, t) {
  const late = clamp((t - 31) / 1.2);
  return who === 'H' ? [lerp(340, 430, late), lerp(700, 760, late)] : [lerp(800, 900, late), lerp(690, 740, late)];
}
