module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {colors:{
      "dark-purple":"#75B9BE",
      "light-white":"rgba(255,255,255,0.18)"}},
  },
  fontFamily: {
    sans: ['Graphik', 'sans-serif'],
    serif: ['Merriweather', 'serif'],
  },
  plugins: [require('daisyui')],
};
